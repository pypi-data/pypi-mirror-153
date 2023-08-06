"""
    Module that contains random program generators

    Each program generator is a state machine that
    generates one instruction at a time. Each object
    creates a generator which can be iterated over
"""
from six.moves import queue
from six.moves import configparser
import logging

import aapg.utils
import aapg.isa_funcs
import aapg.args_generator
import aapg.asm_templates

import random
import re
import os
import sys

""" Setup the logger """
logger = logging.getLogger(__name__)

class BasicGenerator(object):
    """ Basic Generator to generate random instructions """

    def __init__(self, args, arch, seed, no_use_regs, self_checking):
        logger.debug("Created instance of BasicGenerator")

        # Instantiate local variables
        self.q = queue.Queue()
        self.total_instructions = int(args.get('general', 'total_instructions'))
        self.ref_total_instructions = self.total_instructions
        self.inst_dist = None
        self.inst_dist_nobranch = None
        self.inst_dist_backup = None
        self.inst_dist_nobranch_backup = None
        self.regfile = {}
        self.local_regfile = None
        self.instructions_togen = 0
        self.args = args
        self.end_sections = False
        self.recursion_enabled = args.getboolean('recursion-options', 'recursion-enable')
        self.arch = arch
        self.seed = seed
        self.current_access_section = None
        self.end = False
        self.data_hazards = args.items('data-hazards')
        self.curr_inst_nolabel = False
        self.branch_use_reg = None
        self.no_use_regs = no_use_regs
        self.reg_ignore = None
        self.rec_use_reg1 = None
        self.rec_use_reg2 = None
        self.skip_user_flag = False
        self.csr_sections  = args.get('csr-sections','sections')
        self.branch_block_size = args.get('branch-control','block-size')
        self.delegation_boolean = False
        self.self_checking = self_checking
        try:
            self.del_input = int(args.get('general','delegation'))
            if self.del_input != 0:
                self.delegation_boolean = True
        except:
            logger.warn('Delegation Value not provided, Delegation Not Enabled')
            self.del_input = 0xfff
            self.delegation_boolean = False

        # Create the data_access sections
        access_sections = args.items('access-sections')
        self.access_sections = []
        for item in access_sections:
            bounds = item[1].split(',')
            lower_bound = int(bounds[0], 16)
            upper_bound = int(bounds[1], 16)
            read_write = bounds[2]
            label = item[0]
            self.access_sections.append((lower_bound, upper_bound, read_write, label))

        # Seeding the PRNG generator
        random.seed(self.seed)
        aapg.args_generator.set_seed_args_gen(self.seed)
        aapg.isa_funcs.set_seed_isa_funcs(self.seed)

        # Read the instruction distribution
        try:
            self.compute_instruction_distribution(args.items('isa-instruction-distribution'))
            logger.debug("Instruction distribution received")
            for k in self.inst_dist:
                logger.debug("{0} - {1}".format(k, self.inst_dist[k]))
        except configparser.NoSectionError as e:
            logger.error("Instruction distribution not specified.")
            logger.error("Check if your config file has the [isa-instruction-distribution] section")
            sys.exit(1)

        # Setup the register file
        self.init_regfile(args.get('general', 'regs_not_use'))

        # Add a call to the pre-program macro
        logger.info("Adding pre-program macro")

        # Create Pre-lude
        logger.info("Creating Prelude")
        self.add_prelude(args)

        # Set SP to a legal range
        self.add_memory_instruction(random_gen = False)

        # Log debug messages
        logger.debug("Total instructions: {0}".format(self.total_instructions))
        logger.debug("Total instructions to generate: {0}".format(self.instructions_togen))

        # Branch control
        self.insts_since_last_branch = 0
        if self.branch_ext_selected(self.inst_dist):
            self.branch_bwd_prob = args.get('branch-control', 'backward-probability')
            logger.info("Branch instructions present")

        # Adding this to act as counter for branches
        if self.branch_use_reg!=None:
            self.q.put(('instruction', ['li', 'x{branch_use_reg}'.format(branch_use_reg=self.branch_use_reg), '10']))
        else:
            self.q.put(('instruction', ['li', 'x31', '10']))

        if self.self_checking:
            self.q.put(('instruction_nolabel', ('la', 't0', 'register_swap')))
            self.q.put(('instruction_nolabel', ('csrw', 'mscratch', 't0')))
            self.q.put(('instruction', ['li', 'x5', '0']))

        self.total_instructions += 1

        # Setup the user function call 
        try:
            sci = int(args.get('self-checking','rate'))
        except:
            sci = 100


        self.user_calls_dict = {'user-functions' : args.items('user-functions')}
        self.user_calls_dict['i_cache_thrash'] = ('f', args.getint('i-cache', 'num_calls'))
        if args.getboolean('switch-priv-modes', 'switch_modes') and self.self_checking != True:
            self.user_calls_dict['switchmodes'] = ('m', args.getint('switch-priv-modes', 'num_switches'))

        self.track_chsum = 0
        self.count_chsum = 0
        self.self_checking_interval = sci
        self.total_chsum = args.getint('general','total_instructions')/sci
        
        ecause_filtered = list(filter(lambda x: int(x[1]) > 0, args.items('exception-generation')))

        for ecause in ecause_filtered:
            self.user_calls_dict[ecause[0]] = ('m', int(ecause[1]))

        keys = ' '.join(self.user_calls_dict.keys())

        logger.info('User functions received {}'.format(keys))
        new_dict = {} 

        for key, value in self.user_calls_dict.items():
            if key.startswith('ecause'):
                (mode,number) = value
                for i in range(number):
                    new_key = key+'_{:05d}'.format(i)
                    new_value = ('m',1)
                    new_dict.update({new_key:new_value})
            elif key.startswith('user-functions'):
                for (key_in,value_in) in value:
                    new_key = key_in
                    in_dict = eval(value_in)
                    for k,v in in_dict.items():
                        new_value = ('f',int(k))
                    new_dict.update({new_key:new_value})
            else:
                new_dict.update({key:value})

        self.user_calls_dict = new_dict

        # Add recursion call
        if self.recursion_enabled:
            self.user_calls_dict['.recurse_init'] = ('f', int(args.get(
                    'recursion-options', 'recursion-calls')))

    def __iter__(self):
        return self

    def __next__(self):
        if self.total_instructions != 0:
            self.generate_next_instruction()

        if self.q.empty():
            if not self.end:
                self.q.put(('instruction_nolabel', ('post_program_macro', )))

                if self.args.getboolean('general', 'default_program_exit'):
                    self.q.put(('pseudo', ['j', 'write_tohost']))
                    self.total_instructions += 1
                self.total_instructions += 1
                self.end = True
            elif self.recursion_enabled:
                self.add_recursion_sections(self.args.getint('recursion-options', 'recursion-depth'))
                self.recursion_enabled = False
            else:
                raise StopIteration('Instructions over')

        return self.q.get()
    
    def next(self):
        """Python 2 compat"""
        return self.__next__()

    def generate_next_instruction(self):
        # Check if total number of required instructions have been generated
        if self.total_instructions == 0:
            logger.info("Total number of instructions required generated")
            return

        if self.self_checking:
                self.track_chsum = self.track_chsum + 1

        if self.self_checking:
            if self.track_chsum >= self.self_checking_interval:
                if self.count_chsum < self.total_chsum + 1:
                    self.track_chsum = 0
                    self.count_chsum = self.count_chsum + 1
                    self.q.put(('instruction', ('call', 'write_chsum')))

        # Randomly add a user-defined call
        temp_dict = self.user_calls_dict
        self.user_calls_dict = {x:temp_dict[x] for x in temp_dict if temp_dict[x][1] > 0}
        user_defined_total_calls = sum(map(lambda x: x[1], self.user_calls_dict.values()))
        logger.debug('User calls left {}'.format(user_defined_total_calls))



        if user_defined_total_calls > 0 and random.uniform(0,1) < (user_defined_total_calls/self.instructions_togen) and self.skip_user_flag==False:  #0.84 for 80%
            
            logger.debug('Adding a user call')

            # Select the user call
            user_call = random.choice(list(self.user_calls_dict.keys()))

            # Check if function call or macro
            if self.user_calls_dict[user_call][0] == 'f':
                self.q.put(('instruction', ('call', user_call)))
            else:
                self.q.put(('instruction', (user_call, )))
            self.user_calls_dict[user_call] = (self.user_calls_dict[user_call][0], self.user_calls_dict[user_call][1] - 1)

            self.total_instructions -= 1

            # Check if only user defined calls are left (To avoid grouping at the bottom)
            if self.total_instructions <= user_defined_total_calls or self.instructions_togen == 0:
                logger.warn("Skipping adding user function to test, to maintain even distribution")
                usrfprt = str(self.user_calls_dict)
                logger.warn("Functions Skipped: "+usrfprt)
                self.skip_user_flag = True
                self.total_instructions = 0
                return

            return
            

        # Select a random instruction
        if self.instructions_togen > 0:
            # To keep track if stuck in while loop
            reset_threshold = 0
            next_inst_found = False
            while not next_inst_found:

                # If we have crossed a certain threshold from the
                # previous branch instruction, generate a branch
                # instruction possibly, otherwise omit the key
                if self.branch_ext_selected(self.inst_dist):
                    if self.insts_since_last_branch > self.min_insts_threshold:
                        isa_ext = random.choice(self.branch_exts(self.inst_dist))
                    else:
                        isa_ext = random.choice(list(self.inst_dist_nobranch.keys()))
                else:
                    isa_ext = random.choice(list(self.inst_dist.keys()))

                if self.inst_dist[isa_ext] > 0:
                    next_inst = aapg.isa_funcs.get_random_inst_from_set(isa_ext)
                    self.inst_dist[isa_ext] -= 1

                    if not self.is_branch_ext(isa_ext):
                            self.insts_since_last_branch += 1

                    next_inst_found = True

                reset_threshold = reset_threshold + 1
                # Reset instruction distribution if stuck in while loop
                if reset_threshold > 1000:
                    logger.warn("Error in selecting instruction, Resetting distribution")
                    self.inst_dist = self.inst_dist_backup.copy()
                    self.inst_dist_nobranch = self.inst_dist_nobranch_backup.copy()

            # With a small probablity, write to fcsr register    
            if next_inst[0] in aapg.isa_funcs.float_insts and self.total_instructions > 2 and self.instructions_togen > 2:
                fcsr_prob = random.uniform(0,1)
                if fcsr_prob<0.05:
                    selector = [0,1,2,3,4,5,6,7]
                    choice = random.choice(selector)
                    self.q.put(('instruction', ('fsrmi', 'x0', '{}'.format(str(choice)))))

            # if memory_insts, randomly displace sp
            if next_inst[0] in aapg.isa_funcs.memory_insts and len(self.access_sections) > 0:
                self.add_memory_instruction()
                
                # Choose the offset register
                off_reg = 'sp'

                next_inst = tuple([next_inst[0], next_inst[1], off_reg , next_inst[3]])

                # check data section and replace lw with sw
                if next_inst[0][0] != 'c':
                    if self.current_access_section[2] == 'w':
                        if 'l' in next_inst[0]:
                            next_inst_op = next_inst[0].replace('l', 's', 1)
                            next_inst = (next_inst_op,) + next_inst[1:]
                            logger.debug("Load to write section. Rewriting")
                    if self.current_access_section[2] == 'r':
                        if 's' in next_inst[0]:
                            next_inst_op = next_inst[0].replace('s', 'l', 1)
                            next_inst = (next_inst_op,) + next_inst[1:]
                            logger.debug("Store to read section. Rewriting")
                elif next_inst[0][0] == 'c':
                    if self.current_access_section[2] == 'w':
                        if 'l' in next_inst[0]:
                            next_inst_op = next_inst[0].replace('l', 's', 1)
                            next_inst = (next_inst_op,) + next_inst[1:]
                            logger.debug("Load to write section. Rewriting")
                    if self.current_access_section[2] == 'r':
                        if 's' in next_inst[0] and 'l' not in next_inst[0]:
                            next_inst_op = next_inst[0].replace('s', 'l', 1)
                            next_inst = (next_inst_op,) + next_inst[1:]
                            logger.debug("Store to read section. Rewriting")


            # if control instruction
            if self.is_branch_ext(isa_ext):
                (next_insts,self.reg_ignore) = aapg.args_generator.gen_branch_args(
                        next_inst,
                        self.regfile,
                        self.arch,
                        insts_total = self.ref_total_instructions,
                        insts_left = self.instructions_togen,
                        insts_since = self.insts_since_last_branch,
                        bwd_prob = self.branch_bwd_prob,
                        branch_use_reg = self.branch_use_reg
                )
                
                extra_instructions = []
                self.local_regfile = self.regfile.copy()

                if self.reg_ignore != None:
                    self.reg_ignore = ('x',self.reg_ignore)
                    if self.reg_ignore in self.local_regfile.keys():
                        del self.local_regfile[self.reg_ignore]

                to_temp_remove = [5,6,10,11,12,13,30]
                for i in to_temp_remove:
                    rem = ('x',i)
                    if rem in self.local_regfile.keys():
                        del self.local_regfile[rem]

                no_pre_insts = int(self.branch_block_size) * 2
                comp_string_begin = ['beq','bne','blt','bge','jal','jalr','pre_branch_macro']
                comp_string_end = ['beq','bne','blt','bge','jal','jalr','post_branch_macro']

                
                begin = 0
                if self.reg_ignore!=None:
                    for start in range(len(next_insts)):
                        if next_insts[start][0] == 'la':
                            if next_insts[start][2][0] == 'f':
                                begin = 0
                                break
                        if next_insts[start][0] in comp_string_begin:
                            begin = start
                            break

                end = len(next_insts)
                if self.reg_ignore!=None:
                    for i in range(len(next_insts)-1,-1,-1):
                        if "1:" in next_insts[i][0]:
                            end = len(next_insts)
                            break
                        if next_insts[i][0] in comp_string_end:
                            end = i+1
                            break



                if begin!=0:
                    for i in range(begin):
                        self.q.put(('instruction_nolabel',next_insts[i]))
                for dummy in range(no_pre_insts):

                    isa_ext = random.choice(list(self.inst_dist_nobranch.keys()))
                    next_inst = aapg.isa_funcs.get_random_inst_from_set(isa_ext)

                    
                    if next_inst[0] in aapg.isa_funcs.memory_insts and len(self.access_sections) > 0:
                        self.add_memory_instruction()
                        
                        # Choose the offset register
                        off_reg = 'sp'

                        next_inst = tuple([next_inst[0], next_inst[1], off_reg , next_inst[3]])

                        # check data section and replace lw with sw
                        if next_inst[0][0] != 'c':
                            if self.current_access_section[2] == 'w':
                                if 'l' in next_inst[0]:
                                    next_inst_op = next_inst[0].replace('l', 's', 1)
                                    next_inst = (next_inst_op,) + next_inst[1:]
                                    logger.debug("Load to write section. Rewriting")
                            if self.current_access_section[2] == 'r':
                                if 's' in next_inst[0]:
                                    next_inst_op = next_inst[0].replace('s', 'l', 1)
                                    next_inst = (next_inst_op,) + next_inst[1:]
                                    logger.debug("Store to read section. Rewriting")
                        elif next_inst[0][0] == 'c':
                            if self.current_access_section[2] == 'w':
                                if 'l' in next_inst[0]:
                                    next_inst_op = next_inst[0].replace('l', 's', 1)
                                    next_inst = (next_inst_op,) + next_inst[1:]
                                    logger.debug("Load to write section. Rewriting")
                            if self.current_access_section[2] == 'r':
                                if 's' in next_inst[0] and 'l' not in next_inst[0]:
                                    next_inst_op = next_inst[0].replace('s', 'l', 1)
                                    next_inst = (next_inst_op,) + next_inst[1:]
                                    logger.debug("Store to read section. Rewriting")


                    flag = False
                    if isa_ext == 'rv32a' or isa_ext == 'rv64a':
                        #self.instructions_togen -= 1
                        #self.total_instructions -= 1
                        next_inst_with_args = aapg.args_generator.gen_atomic_args(
                            next_inst,
                            self.local_regfile,
                            self.arch,
                            self.reg_ignore,
                            data_hazards = self.data_hazards
                            )
                        flag = True

                    if flag == False:
                        next_inst_with_args = aapg.args_generator.gen_args(
                            next_inst,
                            self.local_regfile,
                            self.arch,
                            self.reg_ignore,
                            self.csr_sections,
                            total = self.ref_total_instructions,
                            current = self.instructions_togen,
                            data_hazards = self.data_hazards)

                    #Add instruction to branch block
                    extra_instructions.append(('instruction_nolabel', next_inst_with_args))

                #Split the instructions to be before and after the branch instruction
                before = extra_instructions[:len(extra_instructions)//2]
                after = extra_instructions[len(extra_instructions)//2:]

                for i in range(len(before)):
                    self.q.put(before[i])

                temp_list = next_insts[begin:end]
                if end != len(next_insts):
                    temp_list.append(next_insts[-1])
                
                self.q.put(('branch', temp_list))

                for i in range(len(after)):
                    self.q.put(after[i])
                
                if end != len(next_insts):
                    for i in range(end,len(next_insts)-1):
                        self.q.put(('instruction_nolabel', next_insts[i]))

                self.insts_since_last_branch = 0
                self.instructions_togen -= 1
                self.total_instructions -= 1
                self.reg_ignore = None
                self.local_regfile = None
                
                return

            # if atomic instruction
            if isa_ext == 'rv32a' or isa_ext == 'rv64a':
                self.instructions_togen -= 1
                self.total_instructions -= 1
                next_inst_with_args = aapg.args_generator.gen_atomic_args(
                    next_inst,
                    self.regfile,
                    self.arch,
                    self.reg_ignore,
                    data_hazards = self.data_hazards
                    )
                self.q.put(('instruction', next_inst_with_args))

                return

            # Create args for next instruction
            next_inst_with_args = aapg.args_generator.gen_args(
                    next_inst,
                    self.regfile,
                    self.arch,
                    self.reg_ignore,
                    self.csr_sections,
                    total = self.ref_total_instructions,
                    current = self.instructions_togen,
                    data_hazards = self.data_hazards)

            # Put the instruction
            if self.curr_inst_nolabel:
                self.q.put(('instruction_nolabel', next_inst_with_args))
                self.curr_inst_nolabel = False
            else:
                self.q.put(('instruction', next_inst_with_args))

            self.instructions_togen -= 1

        # Decrement total number of instructions
        self.total_instructions -= 1
        return

    def compute_instruction_distribution(self, args):
        """ Function to compute fraction of instructions per ISA extension """

        # Dictionary to store the values of each instruction distribution
        cd = {}

        # Count relative values of instruction set
        # config format - rel_<inst_set>_instructions
        for item in args:
            isa_index = item[0].split('_')[1]
            if float(item[1]) > 0.0:
                cd[isa_index] = float(item[1])

        # Normalize them
        total_sum = sum(list([float(k) for k in cd.values()]))
        for k in cd:
            instr_count = int(cd[k]*self.total_instructions/total_sum)
            cd[k] = int(cd[k]*self.total_instructions/total_sum)

        self.inst_dist = cd
        self.inst_dist_nobranch = {k:cd[k] for k in self.inst_dist if
                (k != 'rv32i.ctrl' and k != 'rvc.ctrl' and k != 'rv32c.ctrl')}
        if self.branch_ext_selected(self.inst_dist):
            num_branch_insts = 0
            if 'rv32i.ctrl' in self.inst_dist:
                num_branch_insts += self.inst_dist['rv32i.ctrl']
            if 'rvc.ctrl' in self.inst_dist:
                num_branch_insts += self.inst_dist['rvc.ctrl']
            if 'rv32c.ctrl' in self.inst_dist:
                num_branch_insts += self.inst_dist['rv32c.ctrl']
            try:
                self.min_insts_threshold = int(sum(self.inst_dist_nobranch.values())/num_branch_insts) - 1
                logger.info("Branch threshold: {}".format(self.min_insts_threshold))
            except:
                logger.error("Number of Instructions too low for branch. Increase Total number of instructions")
                exit(0)
        else:
            self.min_insts_threshold = 0

        self.total_instructions = sum(self.inst_dist.values())
        self.instructions_togen = self.total_instructions
        self.inst_dist_backup = self.inst_dist.copy()
        self.inst_dist_nobranch_backup = self.inst_dist_nobranch.copy()


    def init_regfile(self, not_used_reg_string):
        """ Initialize the register file | reg : (read, write) """
        # not_used_regs for all other instructions
        not_used_regs = [(x[0], int(x[1:])) for x in not_used_reg_string.strip("'").split(',')]
        if self.self_checking:
            not_used_regs.append(('x',5))
        
        # dont_use_regs used for selecting register for branch use
        dont_use_regs = [5,6,10,11,12,13,30] # 6 is for data section load, 10 is branch target

        self.rec_use_reg1 = random.randint(0,5)
        self.rec_use_reg2 = random.randint(0,5)
        while self.rec_use_reg2 == self.rec_use_reg1:
            self.rec_use_reg2 = random.randint(0,5)

        dont_use_regs.append(self.rec_use_reg1)
        dont_use_regs.append(self.rec_use_reg2)

        for i in self.no_use_regs:
            dont_use_regs.append(i)
        

        if self.branch_ext_selected(self.inst_dist):
            while(True):
                branch_use_reg = random.randint(16, 31)
                if ('x',branch_use_reg) not in not_used_regs and branch_use_reg not in dont_use_regs:
                    self.branch_use_reg = branch_use_reg
                    not_used_regs.append(('x', branch_use_reg))
                    break

        for i in range(32):
            reg = ('x', i)
            if reg not in not_used_regs:
                self.regfile[('x', i)] = (0,0)
        
        for i in range(32):
            reg = ('f', i)
            if reg not in not_used_regs:
                self.regfile[('f', i)] = (0,0)

    def add_prelude(self, args):
        """Add the prelude instructions to the queue to be written"""

        # Pre-program macro
        self.q.put(('section', 'main'))
        self.q.put(('instruction_nolabel', ('pre_program_macro', )))
        if args.getboolean('switch-priv-modes', 'switch_modes') and self.self_checking != True:
          self.q.put(('instruction_nolabel', ('la', 't0', 'switch_mode_handler')))
          self.q.put(('instruction_nolabel', ('csrw', 'mtvec', 't0')))
        elif args.getboolean('general', 'custom_trap_handler'):
            if self.delegation_boolean:
                mode = args.get('priv-mode','mode')
                if mode=="m":
                  self.q.put(('instruction_nolabel', ('la', 't0', 'custom_trap_handler')))
                  self.q.put(('instruction_nolabel', ('csrw', 'mtvec', 't0')))
                if mode=="s":
                  self.q.put(('instruction_nolabel', ('la', 't0', 'custom_trap_handler')))
                  self.q.put(('instruction_nolabel', ('csrw', 'mtvec', 't0')))
                  self.q.put(('instruction_nolabel', ('la', 't0', 'custom_trap_handler_s')))
                  self.q.put(('instruction_nolabel', ('csrw', 'stvec', 't0')))
                  self.q.put(('instruction_nolabel', ('li', 't0', '{}'.format(self.del_input))))
                  self.q.put(('instruction_nolabel', ('csrw', 'medeleg', 't0')))
                if mode=="u":
                  self.q.put(('instruction_nolabel', ('la', 't0', 'custom_trap_handler')))
                  self.q.put(('instruction_nolabel', ('csrw', 'mtvec', 't0')))
            else:
                self.q.put(('instruction_nolabel', ('la', 't0', 'custom_trap_handler')))
                self.q.put(('instruction_nolabel', ('csrw', 'mtvec', 't0')))

        self.q.put(('instruction_nolabel', ('test_entry_macro', )))
        self.q.put(('instruction_nolabel', ['123:']))
        self.total_instructions += 2

        # User trap handler
        

    def add_recursion_sections(self, depth):
        """Add user-defined templates"""
        recursion_template_enabled = self.recursion_enabled
        logger.info("Recursion Enabled? {}".format(recursion_template_enabled))

        if recursion_template_enabled:
            recurse_sections = aapg.asm_templates.recurse_sections(depth,self.rec_use_reg1,self.rec_use_reg2)
            for section in recurse_sections:
                self.q.put(('section', '.' + section))
                for instruction in recurse_sections[section]:
                    self.q.put(('pseudo', instruction))

        return

    def add_recursion_call(self):
        """ Add a recursion call """
        recursion_depth = self.args.getint('recursion-options', 'recursion-depth')
        self.q.put(('instruction', ('li', 'a0', str(recursion_depth))))
        self.q.put(('instruction', ('call', '.recurse')))
        self.total_instructions += 2
        logger.debug("Added recursion call")
        return

    def add_memory_instruction(self, random_gen = True):
        """ Add a memory instruction
            With a certain percentage, move the stack pointer within the accepted
            access sections and then check the instruction type and create the
            offset
        """
        if len(self.access_sections) == 0:
            # No access section specified
            return

        if random.random() < 0.2 or random_gen == False:
            # Select a random access section
            access_section = random.choice(self.access_sections)
            sp_address = random.randint(access_section[0] + 2048, access_section[1] - 2048)

            # Align to 64 bits
            sp_address = int(sp_address/8)*8
            self.q.put(('instruction_nolabel', ['la', 'sp', access_section[3]]))
            self.q.put(('instruction_nolabel', ['li', 't1', str(sp_address - access_section[0])]))
            self.q.put(('instruction_nolabel', ['add', 'sp', 'sp', 't1']))
            self.total_instructions += 3
            self.current_access_section = access_section

    def branch_ext_selected(self, inst_dist):
        """ Check if a branch extension is present in supplied inst dist """
        if 'rv32i.ctrl' in inst_dist or 'rvc.ctrl' in inst_dist or 'rv32c.ctrl' in inst_dist:
                return True
        else:
                return False

    def is_branch_ext(self, ext):
        if ext == 'rv32i.ctrl' or ext == 'rvc.ctrl' or ext == 'rv32c.ctrl':
            return True
        else:
            return False

    def branch_exts(self, inst_dist):
        """ Return the exts selected """
        ret = []
        for k in self.inst_dist:
            if k == 'rv32i.ctrl' or k == 'rv32c.ctrl' or k == 'rvc.ctrl':
                ret.append(k)

        return ret

class DataGenerator(object):
    """ Object to generate the data section """

    def __init__(self, size):
        """ Initialize the data generator """
        logger.debug("Data generator instantiated of size %s bytes", size)

        # Upper bound for random value in abs
        self.bounds = {
            '.dword': 1<<64 - 1,
            '.word' : 1<<32 - 1,
            '.half' : 1<<16 - 1,
            '.byte' : 1<<8 - 1
        }

        # Local variables
        if size % 64 == 0:
            # Multiple of 64 bits / dword
            size_prefix = '.dword'
            num_lines = size / 8
        elif size % 32 == 0:
            # Multiple of 32 bits / word
            size_prefix = '.word'
            num_lines = size / 4
        elif size % 16 == 0:
            # Multiple of 16 bits / half
            size_prefix = '.half'
            num_lines = size / 2
        else:
            size_prefix = '.byte'
            num_lines = size

        self.size_prefix = size_prefix
        self.num_lines = num_lines
        logger.debug("Num {}: {}".format(size_prefix, num_lines))

    def __iter__(self):
        return self

    def next(self):
        """Python 2 compat"""
        return self.__next__()

    def __next__(self):
        logger.debug("Lines left: {}".format(self.num_lines))
        if self.num_lines == 0:
            raise StopIteration("Data Section Generated")
        else:
            self.num_lines -= 1
            value = random.randint(0, self.bounds[self.size_prefix])
            address = (self.size_prefix, "{0:#0{1}x}".format(value, 18))
            return address

class ThrashGenerator(object):
    """ Object to generate the data section """

    def __init__(self, cache_type, args):
        """ Initialize the data generator """
        logger.debug("Thrash generator instantiated")

        # Read the args
        self.num_bytes_per_block = int(args.getint(cache_type, 'num_bytes_per_block'))
        self.num_blocks = int(args.getint(cache_type, 'num_blocks'))
        self.num_cycles = int(args.getint(cache_type, 'num_cycles'))
        
        # Log configured args
        logger.info("Cache thrasher type: {}".format(cache_type))
        logger.info("Number of bytes per block: {}".format(self.num_bytes_per_block))
        logger.info("Number of blocks: {}".format(self.num_blocks))
        logger.info("Number of cycles: {}".format(self.num_cycles))

        # Local variables
        self.return_address_moved = False
        self.finished = False

        # Local counters
        self.block_index = 0
        self.byte_index = 0
        self.miss = True

    def __iter__(self):
        return self

    def next(self):
        """Python 2 compat"""
        return self.__next__()

    def __next__(self):
        if self.finished:
            raise StopIteration("Thrashing section generated")

        if not self.return_address_moved:
            self.return_address_moved = True
            # Move the return address from x1 into x31
            insts = [
                ('addi', 'x31', 'x1', '0'),
            ]

            insts_left = int((self.num_bytes_per_block - 8) / 4)
            if insts_left > 0:
                insts.extend([('addi', 'x0', 'x0', '0')] * insts_left)
            return ('instructions', insts)

        # Creating the i-cache instruction
        miss = self.miss
        if self.block_index < (2 * self.num_cycles * self.num_blocks):
            if self.byte_index == 0:
                self.byte_index = 4
                if miss == True:
                    return (
                        'label',
                        'it' + '{0:09x}'.format(self.block_index),
                        ('j', 'it' + '{0:09x}'.format(self.block_index + 1)))
                elif miss == False:
                    return (
                        'label',
                        'it' + '{0:09x}'.format(self.block_index),
                        ('j', 'it' + '{0:09x} + 4'.format(self.block_index -1)))

            elif self.byte_index > 0 and self.byte_index < self.num_bytes_per_block - 4:
                self.byte_index += 4
                nop = ('instruction',('nop',))
                return nop
            elif self.byte_index == self.num_bytes_per_block - 4:
                self.byte_index += 4
                if miss == True:
                    return (
                        'instruction',
                        ('j', 'it' + '{0:09x} + 4'.format(self.block_index +1))
                    )
                elif miss == False:
                    nop = ('instruction',('nop',))
                    return nop
            elif self.byte_index == self.num_bytes_per_block:
                self.byte_index = 0
                self.block_index += 1
                self.miss = not self.miss
        elif self.block_index == 2 * self.num_cycles * self.num_blocks:
            self.finished = True
            return (
                'label_instructions',
                'it' + '{0:09x}'.format(self.block_index),
                [
                    ('jr', 'x31'),
                ])

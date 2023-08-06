'''
    Module to generate the arguments for the instructions
'''
import aapg.isa_funcs
import aapg.mappings
import random
import os
import logging
import sys

logger = logging.getLogger(__name__)

def set_seed_args_gen(seed):
    """ Set the global seed """
    random.seed(seed)

def gen_branch_args(instruction, regfile, arch, *args, **kwargs):
    """ Generate the args for branch instructions """
    instr_name = instruction[0]
    # Forward or backward jump
    backward = random.random() < float(kwargs['bwd_prob'])

    # Taken or not taken
    taken = random.random() < 0.5

    usable_regs = []
    for (j,i) in regfile:
        if j =="x" and i>15:
            usable_regs.append(i)

    # Don't touch registers used elsewhere in aapg
    if 10 in usable_regs:
        usable_regs.remove(10)
    if 6 in usable_regs:
        usable_regs.remove(6)
    if 5 in usable_regs:
        usable_regs.remove(5)
    if 11 in usable_regs:
        usable_regs.remove(11)
    if 12 in usable_regs:
        usable_regs.remove(12)
    if 13 in usable_regs:
        usable_regs.remove(13)
    if 30 in usable_regs:
        usable_regs.remove(30)
    if 1 in usable_regs:
        usable_regs.remove(1)
    if 0 in usable_regs:
        usable_regs.remove(0)
    if 15 in usable_regs:
        usable_regs.remove(15)

    # Find register for comparison with branch 
    try:
        comp_reg = random.choice(usable_regs)
    except:
        logger.error("Unable to find usable register for branch comparison. Remove registers >15 from no use registers. Exitting")
        sys.exit(1)

    # Number of steps to jump
    try:
        num_steps = random.randint(5, kwargs['insts_since'] - 5)
    except ValueError as e:
        logger.error("Number of instructions required for branch threshold to low")
        logger.error("Increase count of non-branch instructions")
        sys.exit(1)

    # if forward and number of insts not sufficient, switch to bwd
    if not backward and num_steps > kwargs['insts_left'] - 5:
        backward = True

    # Generate the args
    offset_string = '{0},{1}'.format('b' if backward else 'f', num_steps)

    if instr_name == 'beq' or instr_name == 'c.beqz':
        pre_insts = []
        if backward:
            if taken:
                pre_insts.append(['li', 'x{comp_reg}'.format(comp_reg=comp_reg), '11'])
                pre_insts.append(['addi', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), '1'])
            else:
                pre_insts.append(['li', 'x{comp_reg}'.format(comp_reg=comp_reg), '0'])
        else:
            if taken:
                pre_insts.append(['li', 'x{comp_reg}'.format(comp_reg=comp_reg), '10'])
            else:
                pre_insts.append(['li', 'x{comp_reg}'.format(comp_reg=comp_reg), '0'])
        pre_insts.append(['pre_branch_macro'])
        pre_insts.append(['beq', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), 'x{comp_reg}'.format(comp_reg=comp_reg), offset_string]) 
        pre_insts.append(['post_branch_macro'])
        pre_insts.append(['li', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), '10'])

        pre_insts.append(offset_string)
        return (pre_insts,comp_reg)
    elif instr_name == 'bne' or instr_name == 'c.bnez':
        pre_insts = []
        if backward:
            if taken:
                pre_insts.append(['li', 'x{comp_reg}'.format(comp_reg=comp_reg), '12'])
                pre_insts.append(['addi', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), '1'])
            else:
                pre_insts.append(['li', 'x{comp_reg}'.format(comp_reg=comp_reg), '10'])
        else:
            if taken:
                pre_insts.append(['li', 'x{comp_reg}'.format(comp_reg=comp_reg), '11'])
                pre_insts.append(['li', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), '10']) 
            else:
                pre_insts.append(['li', 'x{comp_reg}'.format(comp_reg=comp_reg), '10'])
                pre_insts.append(['li', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), '10'])
        pre_insts.append(['pre_branch_macro'])
        pre_insts.append(['bne', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), 'x{comp_reg}'.format(comp_reg=comp_reg), offset_string]) 
        pre_insts.append(['post_branch_macro'])
        pre_insts.append(['li', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), '10'])

        pre_insts.append(offset_string)
        return (pre_insts,comp_reg)
    elif instr_name == 'blt' or instr_name == 'bltu':
        pre_insts = []
        if backward:
            if taken:
                pre_insts.append(['li', 'x{comp_reg}'.format(comp_reg=comp_reg), '12'])
                pre_insts.append(['addi', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), '1'])
            else:
                pre_insts.append(['li', 'x{comp_reg}'.format(comp_reg=comp_reg), '9'])
        else:
            if taken:
                pre_insts.append(['li', 'x{comp_reg}'.format(comp_reg=comp_reg), '12'])
                pre_insts.append(['li', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), '10']) 
            else:
                pre_insts.append(['li', 'x{comp_reg}'.format(comp_reg=comp_reg), '9'])
                pre_insts.append(['li', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), '10'])
        pre_insts.append(['pre_branch_macro'])
        pre_insts.append(['blt', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), 'x{comp_reg}'.format(comp_reg=comp_reg), offset_string]) 
        pre_insts.append(['post_branch_macro'])
        pre_insts.append(['li', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), '10'])

        pre_insts.append(offset_string)
        return (pre_insts,comp_reg)
    elif instr_name == 'bge' or instr_name == 'bgeu':
        pre_insts = []
        if backward:
            if taken:
                pre_insts.append(['li', 'x{comp_reg}'.format(comp_reg=comp_reg), '12'])
                pre_insts.append(['addi', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), '1'])
            else:
                pre_insts.append(['li', 'x{comp_reg}'.format(comp_reg=comp_reg), '9'])
        else:
            if taken:
                pre_insts.append(['li', 'x{comp_reg}'.format(comp_reg=comp_reg), '11'])
                pre_insts.append(['li', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), '10']) 
            else:
                pre_insts.append(['li', 'x{comp_reg}'.format(comp_reg=comp_reg), '9'])
                pre_insts.append(['li', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), '10'])
        pre_insts.append(['pre_branch_macro'])
        pre_insts.append(['bge', 'x{comp_reg}'.format(comp_reg=comp_reg), 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), offset_string]) 
        pre_insts.append(['post_branch_macro'])
        pre_insts.append(['li', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), '10'])
        pre_insts.append(offset_string)
        return (pre_insts,comp_reg)
    elif instr_name == 'jal' or instr_name == 'c.j' or instr_name == 'c.jal':
        pre_insts = []

        target_reg = 'x10'

        if instr_name == 'c.j':
            target_reg = 'x0'
        elif instr_name == 'c.jal':
            target_reg = 'x1'

        if backward:
            if taken:
                pre_insts.append(['li', 'x{comp_reg}'.format(comp_reg=comp_reg), '12'])
                pre_insts.append(['addi', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), '1'])
                pre_insts.append(['beq', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), 'x{comp_reg}'.format(comp_reg=comp_reg), '1f'])
                pre_insts.append(['jal', '{}'.format(target_reg), offset_string])
                pre_insts.append(['1: li x{branch_use_reg}, 10'.format(branch_use_reg=kwargs['branch_use_reg'])])
            else:
                pre_insts.append(['li', 'x{comp_reg}'.format(comp_reg=comp_reg), '10'])
                pre_insts.append(['beq', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), 'x{comp_reg}'.format(comp_reg=comp_reg), '1f'])
                pre_insts.append(['jal', '{}'.format(target_reg), offset_string])
                pre_insts.append(['1: li x{branch_use_reg}, 10'.format(branch_use_reg=kwargs['branch_use_reg'])])
        else:
            pre_insts.append(['jal', '{}'.format(target_reg), offset_string])
        pre_insts.append(offset_string)
        return (pre_insts,comp_reg)
    elif instr_name == 'jalr' or instr_name == 'c.jr' or instr_name == 'c.jalr':
        pre_insts = []

        target_reg = 'x10'

        if instr_name == 'c.jr':
            target_reg = 'x0'
        elif instr_name == 'c.jalr':
            target_reg = 'x1'

        if backward:
            if taken:
                pre_insts.append(['li', 'x{comp_reg}'.format(comp_reg=comp_reg), '12'])
                pre_insts.append(['addi', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), '1'])
                pre_insts.append(['beq', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), 'x{comp_reg}'.format(comp_reg=comp_reg), '1f'])
                pre_insts.append(['la', 'x{comp_reg}'.format(comp_reg=comp_reg), offset_string])
                pre_insts.append(['jalr', '{}'.format(target_reg), 'x{comp_reg}'.format(comp_reg=comp_reg), '0'])
                pre_insts.append(['1: li x{branch_use_reg}, 10'.format(branch_use_reg=kwargs['branch_use_reg'])])
            else:
                pre_insts.append(['li', 'x{comp_reg}'.format(comp_reg=comp_reg), '10'])
                pre_insts.append(['beq', 'x{branch_use_reg}'.format(branch_use_reg=kwargs['branch_use_reg']), 'x{comp_reg}'.format(comp_reg=comp_reg), '1f'])
                pre_insts.append(['la', 'x{comp_reg}'.format(comp_reg=comp_reg), offset_string])
                pre_insts.append(['jalr', '{}'.format(target_reg), 'x{comp_reg}'.format(comp_reg=comp_reg), '0'])
                pre_insts.append(['1: li x{branch_use_reg}, 10'.format(branch_use_reg=kwargs['branch_use_reg'])])
        else:
            pre_insts.append(['la', 'x{comp_reg}'.format(comp_reg=comp_reg), offset_string])
            pre_insts.append(['jalr', '{}'.format(target_reg), 'x{comp_reg}'.format(comp_reg=comp_reg), '0'])
        pre_insts.append(offset_string)
        return (pre_insts,comp_reg)
    else:
        return ([['addi', 'x0', 'x0', '0'], 'f,20'],None)

def gen_memory_inst_offset(instr_name):
    """ Generate load/store offset for the instruction """
    if instr_name in ['ld', 'sd', 'fld', 'fsd']:
        return random.choice(range(-2048, 2047, 8))
    if instr_name in ['lw', 'lwu', 'sw', 'flw', 'fsw']:
        return random.choice(range(-2048, 2047, 4))
    if instr_name in ['lh', 'lhu', 'sh']:
        return random.choice(range(-2048, 2047, 2))
    if instr_name in ['lb', 'lbu', 'sb']:
        return random.choice(range(-2048, 2047))

def incr_rw(reg_tup, read, write):
    fst = reg_tup[0]
    snd = reg_tup[1]

    if read == True:
        fst += 1
    if write == True:
        snd += 1

    return (fst, snd)

def gen_args(instruction, regfile, arch, reg_ignore, csr_sections, *args, **kwargs):
    '''
        Function to generate the args for a given instruction

        Args:
            instruction: tuple of (inst_name, *args)
            regfile: value of the registers

        Returns:
            instruction_with_args: (inst_name, arg_strings)
    '''
    instr_name = instruction[0]
    instr_args = instruction[1:]
    # Creating the registers
    register_mapping = aapg.mappings.register_mapping_int
    register_mapping_float = aapg.mappings.register_mapping_float

    # Filter the registers based on raw / war / waw deps
    data_hazards_dict = {x[0] : x[1] for x in kwargs['data_hazards']}
    num_regs = int(kwargs['data_hazards'][3][1])

    # Generate the highest read and highest written thresholds
    take_reg_set = lambda reg_set, regfile : {
            x : regfile[x] for x in regfile if x[0] == reg_set
    }

    take_reg_set_cmp = lambda reg_set, regfile : {
            x : regfile[x] for x in regfile if x[0] == reg_set and x[1] in range(8,16)}

    reg_reads = lambda reg_set, regfile : [
            regfile[x][0] for x in regfile if x[0] == reg_set]
    reg_writes = lambda reg_set, regfile : [
            regfile[x][1] for x in regfile if x[0] == reg_set]

    reg_reads_filt = lambda reg_set, regfile, thresh : {
            x : regfile[x] for x in regfile if x[0] == reg_set
            and
            regfile[x][0] >= thresh}

    reg_writes_filt = lambda reg_set, regfile, thresh : {
            x : regfile[x] for x in regfile if x[0] == reg_set
            and
            regfile[x][1] >= thresh}

    def inverse(reg_set, regfile):
        reg_ret = {x : regfile[x] for x in regfile if x not in reg_set}
        if len(reg_ret.items()) == 0:
            return regfile
        else:
            return reg_ret

    intersect = lambda a, b : [
            x for x in a if x in b
    ]

    max_read_int_thresh = sorted(reg_reads('x', regfile))[-num_regs] 
    max_read_flt_thresh = sorted(reg_reads('f', regfile))[-num_regs]
    max_read_regs_int = reg_reads_filt('x', regfile, max_read_int_thresh)
    max_read_regs_flt = reg_reads_filt('f', regfile, max_read_flt_thresh)

    max_write_int_thresh = sorted(reg_writes('x', regfile))[-num_regs] 
    max_write_flt_thresh = sorted(reg_writes('f', regfile))[-num_regs] 
    max_write_regs_int = reg_writes_filt('x', regfile, max_write_int_thresh)
    max_write_regs_flt = reg_writes_filt('f', regfile, max_write_flt_thresh)

    # Create the empty registers
    registers_cmp_src = []
    registers_cmp_dst = []

    registers_cmp_flt_src = []
    registers_cmp_flt_dst = []

    registers_src = []
    registers_dst = []

    registers_flt_src = []
    registers_flt_dst = []

    registers_comp = [x for x in regfile if x[1] in range(8,16) and x[0] == 'x']

    registers_comp_float = [x for x in regfile if x[1] in range(8,16) and x[0] == 'f']
    registers_int = [x for x in regfile if x[0] == 'x'] 
    registers_float = [x for x in regfile if x[0] == 'f']

    if random.random() < float(data_hazards_dict['raw_prob']):
        # Generate RAW Hazard. read registers should be
        # the highest written to registers
        registers_src.extend(take_reg_set('x', max_write_regs_int))
        registers_flt_src.extend(take_reg_set('f', max_write_regs_flt))
        registers_cmp_src.extend(take_reg_set_cmp('x', max_write_regs_int))
        registers_cmp_flt_src.extend(take_reg_set_cmp('f', max_write_regs_flt))
    else:
        # RAW not generated, src registers should be the inverse of 
        # max read regs
        registers_src.extend(take_reg_set('x', inverse(max_write_regs_int, regfile)))
        registers_flt_src.extend(take_reg_set('f', inverse(max_write_regs_flt, regfile)))
        registers_cmp_src.extend(take_reg_set_cmp('x', inverse(max_write_regs_int, regfile)))
        registers_cmp_flt_src.extend(take_reg_set_cmp('f', inverse(max_write_regs_flt, regfile)))

    if random.random() < float(data_hazards_dict['war_prob']):
        # Generate WAR hazard. write registers should be
        # the highest read registers
        registers_dst.extend(take_reg_set('x', max_read_regs_int))
        registers_flt_dst.extend(take_reg_set('f', max_read_regs_flt))
        registers_cmp_dst.extend(take_reg_set_cmp('x', max_read_regs_int))
        registers_cmp_flt_dst.extend(take_reg_set_cmp('f', max_read_regs_flt))
    else:
        # WAR not generated. dst registers should be inverse of
        # max read regs
        registers_dst.extend(take_reg_set('x', inverse(max_read_regs_int, regfile)))
        registers_flt_dst.extend(take_reg_set('f', inverse(max_read_regs_flt, regfile)))
        registers_cmp_dst.extend(take_reg_set_cmp('x', inverse(max_read_regs_int, regfile)))
        registers_cmp_flt_dst.extend(take_reg_set_cmp('f', inverse(max_read_regs_flt, regfile)))

    if random.random() < float(data_hazards_dict['waw_prob']):
        # Generate WAW hazard. write registers should be
        # the highest written to registers
        registers_dst.extend(intersect(registers_dst, max_write_regs_int))
        registers_flt_dst.extend(intersect(registers_flt_dst, max_write_regs_flt))
        registers_cmp_dst.extend(intersect(registers_cmp_dst, max_write_regs_int))
        registers_cmp_flt_dst.extend(intersect(registers_cmp_flt_dst, max_write_regs_flt))
    else:
        # WAW not generated, intersect with inverse
        registers_dst.extend(intersect(registers_dst, inverse(max_write_regs_int, regfile)))
        registers_flt_dst.extend(intersect(registers_flt_dst, inverse(max_write_regs_flt, regfile)))
        registers_cmp_dst.extend(intersect(registers_cmp_dst, inverse(max_write_regs_int, regfile)))
        registers_cmp_flt_dst.extend(intersect(registers_cmp_flt_dst, inverse(max_write_regs_flt, regfile)))

    # Iterate over the args
    final_inst = [instr_name,]

    for arg in instr_args:
        if arg == 'rd':
            try:
                register = random.choice(registers_dst)
            except IndexError as e:
                register = random.choice(registers_int)
            regfile[register] = incr_rw(regfile[register], False, True)
            final_inst.append(register_mapping[register])
            continue

        if arg == 'rs1':
            try:
                register = random.choice(registers_src)
            except IndexError as e:
                register = random.choice(registers_int)
            regfile[register] = incr_rw(regfile[register], True, False)
            final_inst.append(register_mapping[register])
            continue

        if arg == 'rs2':
            try:
                register = random.choice(registers_src)
            except IndexError as e:
                register = random.choice(registers_int)
            regfile[register] = incr_rw(regfile[register], True, False)
            final_inst.append(register_mapping[register])
            continue

        if arg in ['imm12', 'uimm12']:

            # Check if memory_inst
            if instr_name in aapg.isa_funcs.memory_insts:
                imm12_val = gen_memory_inst_offset(instr_name)

            else:
                if arg == 'uimm12':
                    if "csr" in instr_name:
                        # Control CSR Access based on config file

                        # Don't write to xstatus, xtvec, xepc, xcause
                        csr_no_use = [0,5,65,66,256,261,321,322,768,773,833,834]
                        valid_ranges = csr_sections.split(',')
                        valid_csrs = []
                        for item in valid_ranges:
                            item = item.replace(' ','')
                            if ':' in item:
                                begin,end = item.split(':')
                                begin = int(begin, 16)
                                end = int(end,16)
                                for int_val in range(begin,end+1):
                                    if int_val not in csr_no_use:
                                        valid_csrs.append(int_val)
                            else:
                                valid_csrs.append(int(item,16))
                        imm12_val = random.choice(valid_csrs)
                    else:
                        imm12_val = random.randint(0,4095)
                else:
                    imm12_val = random.randint(-2048, 2047)

            final_inst.append(str(imm12_val))
            continue

        if arg == 'imm5':
            final_inst.append(str(random.randint(-16, 15)))
            continue

        if arg == 'uimm5':
            final_inst.append(str(random.randint(0,31)))
            continue

        if arg == 'uimm6':
            final_inst.append(str(random.randint(0,63)))
            continue

        if arg == 'imm6':
            final_inst.append(str(random.randint(- 1<<5, 1<<5 - 1)))

        if arg == 'imm20':
            final_inst.append(str(random.randint(0, 1<<20 - 1)))
            continue

        if arg == 'shamt':
            if arch == 'rv32':
                final_inst.append(str(random.randint(0, 31)))
            elif arch == 'rv64':
                final_inst.append(str(random.randint(0, 63)))
            continue

        if arg == 'shamtw':
            final_inst.append(str(random.randint(0, 31)))
            continue

        # Floating point instructions
        if arg == 'rdf':
            try:
                register = random.choice(registers_flt_dst)
            except IndexError as e:
                register = random.choice(registers_float)
            regfile[register] = incr_rw(regfile[register], False, True)
            final_inst.append(register_mapping_float[register])
            continue

        if arg == 'rs1f':
            try:
                register = random.choice(registers_flt_src)
            except IndexError as e:
                register = random.choice(registers_float)
            regfile[register] = incr_rw(regfile[register], True, False)
            final_inst.append(register_mapping_float[register])
            continue

        if arg == 'rs2f':
            try:
                register = random.choice(registers_flt_src)
            except IndexError as e:
                register = random.choice(registers_float)
            regfile[register] = incr_rw(regfile[register], True, False)
            final_inst.append(register_mapping_float[register])
            continue

        if arg == 'rs3f':
            try:
                register = random.choice(registers_flt_src)
            except IndexError as e:
                register = random.choice(registers_float)
            regfile[register] = incr_rw(regfile[register], True, False)
            final_inst.append(register_mapping_float[register])
            continue

        # Compressed
        if arg == 'rdprime':
            try:
                register = random.choice(registers_cmp_dst)
            except IndexError as e:
                register = random.choice(registers_comp)
            regfile[register] = incr_rw(regfile[register], False, True)
            final_inst.append(register_mapping[register])
            continue

        if arg == 'rsprime1':
            try:
                register = random.choice(registers_cmp_src)
            except IndexError as e:
                register = random.choice(registers_comp)
            regfile[register] = incr_rw(regfile[register], True, False)
            final_inst.append(register_mapping[register])
            continue

        if arg == 'rsprime2':
            try:
                register = random.choice(registers_cmp_src)
            except IndexError as e:
                register = random.choice(registers_comp)
            regfile[register] = incr_rw(regfile[register], True, False)
            final_inst.append(register_mapping[register])
            continue

        if arg == 'nzuimm8':
            final_inst.append(str(4*random.randint(0, 1<<8 - 1)))
            continue

        if arg == 's8uimm6':
            final_inst.append(str(8*random.randint(0, 1<<6 - 1)))
            continue

        if arg == 's4uimm6':
            final_inst.append(str(4*random.randint(0, 1<<6 - 1)))
            continue

        if arg == 'imm8':
            final_inst.append(str(random.randint(- 1 << 7, 1 << 7 - 1)))
            continue

        if arg == 'nzimm6':
            final_inst.append(str(random.randint(- 1<<5, 1<<5 - 1)))
            continue

        if arg == 'nzuimm6':
            final_inst.append(str(random.randint(1, 1<<6 - 1)))
            continue

        if arg == 'nzuimm5':
            final_inst.append(str(random.randint(1, 1 << 5 - 1)))
            continue

        if arg == 's16imm6':
            final_inst.append((str(16*random.randint(-1 <<5, 1<<5 - 1))))
            continue

        if arg == 'sp':
            final_inst.append('sp')
            continue

        if arg == 'a0':
            final_inst.append('a0')
            continue

        if arg == 's8uimm5':
            final_inst.append(str(8*random.randint(0, 1<<5 -1)))
            continue 

        if arg == 's4uimm5':
            final_inst.append(str(4*random.randint(0, 1<<5 -1)))
            continue

        if arg == 'rdprimef':
            try:
                register = random.choice(registers_cmp_flt_dst)
            except IndexError as e:
                register = random.choice(registers_comp_float)
            regfile[register] = incr_rw(regfile[register], False, True)
            final_inst.append(register_mapping_float[register])
            continue

        if arg == 'rsprime1f':
            try:
                register = random.choice(registers_cmp_flt_src)
            except IndexError as e:
                register = random.choice(registers_comp_float)
            regfile[register] = incr_rw(regfile[register], True, False)
            final_inst.append(register_mapping_float[register])
            continue

        if arg == 'rsprime2f':
            try:
                register = random.choice(registers_cmp_flt_src)
            except IndexError as e:
                register = random.choice(registers_comp_float)
            regfile[register] = incr_rw(regfile[register], True, False)
            final_inst.append(register_mapping_float[register])
            continue

        if arg == 'rd_rs1_prime':
            try:
                register = random.choice(registers_cmp_dst)
            except IndexError as e:
                register = random.choice(registers_comp)
            regfile[register] = incr_rw(regfile[register], True, True)
            reg_map = register_mapping[register]
            final_inst.append(reg_map)
            final_inst.append(reg_map)
            continue

        if arg == 'rd_rs1':
            try:
                register = random.choice(registers_dst)
            except IndexError as e:
                register = random.choice(registers_int)
            regfile[register] = incr_rw(regfile[register], True, True)
            reg_map = register_mapping[register]
            final_inst.append(reg_map)
            final_inst.append(reg_map)
            continue

        if arg == 'imm11':
            final_inst.append(str(random.randint(- 1<<10, 1<<10 - 1)))
            continue

        if arg == 'x1':
            final_inst.append(register_mapping[('x', 1)])
            continue
        
        if arg == 'x0':
            final_inst.append(register_mapping[('x', 0)])
            continue

        if arg == 'const0':
            final_inst.append('0')
            continue

    if final_inst[0] in aapg.isa_funcs.comp_insts:
        final_inst[0] = aapg.isa_funcs.comp_insts_subs[final_inst[0]]
        
    return tuple(final_inst)

def gen_atomic_args(instruction, regfile, arch, reg_ignore, *args, **kwargs):
    """ Generate args for atomic insts"""

    instr_name = instruction[0]
    instr_args = instruction[1:]

    # Creating the registers
    registers_int = [x for x in regfile if x[0] == 'x'] 
    register_mapping = aapg.mappings.register_mapping_int
    registers_src = []
    registers_dst = []
    
    # Filter the registers based on raw / war / waw deps
    data_hazards_dict = {x[0] : x[1] for x in kwargs['data_hazards']}
    num_regs = int(kwargs['data_hazards'][3][1])

    # Generate the highest read and highest written thresholds
    take_reg_set = lambda reg_set, regfile : {
            x : regfile[x] for x in regfile if x[0] == reg_set
    }

    take_reg_set_cmp = lambda reg_set, regfile : {
            x : regfile[x] for x in regfile if x[0] == reg_set and x[1] in range(8,16)}

    reg_reads = lambda reg_set, regfile : [
            regfile[x][0] for x in regfile if x[0] == reg_set]
    reg_writes = lambda reg_set, regfile : [
            regfile[x][1] for x in regfile if x[0] == reg_set]

    reg_reads_filt = lambda reg_set, regfile, thresh : {
            x : regfile[x] for x in regfile if x[0] == reg_set
            and
            regfile[x][0] >= thresh}

    reg_writes_filt = lambda reg_set, regfile, thresh : {
            x : regfile[x] for x in regfile if x[0] == reg_set
            and
            regfile[x][1] >= thresh}

    def inverse(reg_set, regfile):
        reg_ret = {x : regfile[x] for x in regfile if x not in reg_set}
        if len(reg_ret.items()) == 0:
            return regfile
        else:
            return reg_ret

    intersect = lambda a, b : [
            x for x in a if x in b
    ]

    max_read_int_thresh = sorted(reg_reads('x', regfile))[-num_regs] 
    max_read_regs_int = reg_reads_filt('x', regfile, max_read_int_thresh)

    max_write_int_thresh = sorted(reg_writes('x', regfile))[-num_regs] 
    max_write_regs_int = reg_writes_filt('x', regfile, max_write_int_thresh)

    # Data hazards
    if random.random() < float(data_hazards_dict['raw_prob']):
        # Generate RAW Hazard. read registers should be
        # the highest written to registers
        registers_src.extend(take_reg_set('x', max_write_regs_int))
    else:
        # RAW not generated, src registers should be the inverse of 
        # max read regs
        registers_src.extend(take_reg_set('x', inverse(max_write_regs_int, regfile)))

    if random.random() < float(data_hazards_dict['war_prob']):
        # Generate WAR hazard. write registers should be
        # the highest read registers
        registers_dst.extend(take_reg_set('x', max_read_regs_int))
    else:
        # WAR not generated. dst registers should be inverse of
        # max read regs
        registers_dst.extend(take_reg_set('x', inverse(max_read_regs_int, regfile)))

    if random.random() < float(data_hazards_dict['waw_prob']):
        # Generate WAW hazard. write registers should be
        # the highest written to registers
        registers_dst.extend(intersect(registers_dst, max_write_regs_int))
    else:
        # WAW not generated, intersect with inverse
        registers_dst.extend(intersect(registers_dst, inverse(max_write_regs_int, regfile)))

    final_inst = [instr_name,]

    # Updating the args
    for arg in instr_args:

        if arg == 'rd':
            try:
                register = random.choice(registers_dst)
            except IndexError as e:
                register = random.choice(registers_int)
            regfile[register] = incr_rw(regfile[register], False, True)
            final_inst.append(register_mapping[register])

        if arg == 'rs1':
            if instr_name == 'lr.w' or instr_name == 'lr.d':
                final_inst.append('sp')
            else:
                try:
                    register = random.choice(registers_src)
                except IndexError as e:
                    register = random.choice(registers_int)
                regfile[register] = incr_rw(regfile[register], True, False)
                final_inst.append(register_mapping[register])

        if arg == 'rs2':
            final_inst.append('sp')

    # Iterate over the args

    return final_inst

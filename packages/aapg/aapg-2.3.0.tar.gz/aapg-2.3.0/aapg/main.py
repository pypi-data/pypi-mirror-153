"""
    Automatic Assembly Program Generator (AAPG)

    Main module of AAPG that deals with
        * Parsing command line arguments
        * Reading configuration
        * Initiating the program generation
"""
import logging
import argparse
import os
import io
import sys
import subprocess
import click
import yaml

import aapg.gen_random_program
import aapg.setup_self_check
import aapg.env.templates
import aapg.env.comments
import aapg.env.env_setup
import aapg.utils
from aapg.__init__ import __version__ as version

from multiprocessing import Process

#class TestClass:



# Version read
VERSION = '(' + version + ')' + ' Automated Assembly Program Generator - aapg'

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    if ctx.invoked_subcommand is None:
        click.echo('Please Provide Command')

def setup_logging(log_level):
    """Setup logging

        Verbosity decided on user input

        Args:
            log_level: (str) User defined log level

        Returns:
            None
    """
    numeric_level = getattr(logging, log_level.upper(), None)

    if not isinstance(numeric_level, int):
        print("\033[91mInvalid log level passed. Please select from debug | info | warning | error\033[0m")
        sys.exit(1)

    logging.basicConfig(level = numeric_level)


class myClass:
    def __init__(self,num_programs,config_file,asm_name,setup_dir,output_dir,arch,seed,linker_only,no_headers,self_checking,static_make):
        self.num_programs = num_programs
        self.config_file = config_file
        self.asm_name = asm_name
        self.setup_dir = setup_dir
        self.output_dir = output_dir
        self.arch = arch
        self.seed = seed
        self.linker_only = linker_only
        self.no_headers = no_headers
        self.self_checking = self_checking
        self.static_make = static_make

@cli.command()
@click.option('--num_programs', default=1, help='Number of programs to be generated')
@click.option('--config_file', default ='./config.yaml', help='Configuration file. Default: ./work/config.yaml')
@click.option('--asm_name', default ='out', help='Assembly output file name. Default: out.asm')
@click.option('--setup_dir', default ='work', help='Setup directory of env files. Default ./work')
@click.option('--output_dir', default ='work', help='Output directory for generated programs. Default: ./work/asm')
@click.option('--arch', default ='rv64', help='Target architecture. Default: rv64')
@click.option('--seed', help='Seed to regenerate test.')
@click.option('--linker_only', is_flag='True',help='Generate link.ld only',default='False')
@click.option('--no_headers', is_flag='True',help='Add configuration info in Generated test',default='True')
@click.option('--self_checking', is_flag='True',help='Generate a self Checking Test using spike')
@click.option('--static_make', is_flag='True',help='Fix MakeFile options march=rv64imafdc and ABI = lp64')
def gen(num_programs,config_file,asm_name,setup_dir,output_dir,arch,seed,linker_only,no_headers,self_checking,static_make):
    '''
    Function:   To generate the actuall assembly files
    Usage:      To be run after the `aapg setup` command
                aapg gen --help to understand the arguments
    '''
    args = myClass(num_programs,config_file,asm_name,setup_dir,output_dir,arch,seed,linker_only,no_headers,self_checking,static_make)
    setup_logging('info')
    logger = logging.getLogger()
    logger.handlers = []
    ch = logging.StreamHandler()
    ch.setFormatter(aapg.utils.ColoredFormatter())
    logger.addHandler(ch)
    logger.info("aapg started")
    logger.info(VERSION)
    logger.info("Command received: gen")
    logger.info("Number of programs to generate: {}".format(args.num_programs))
    
    # Self checking test must meet additional constraints
    if args.self_checking:
        eflag = False
        if args.num_programs >1:
            logger.error('Limit number of programs to 1 if self checking test')
            eflag = True
        if args.setup_dir != args.output_dir and args.output_dir != os.path.join(args.setup_dir,"asm"):
            logger.error('Give the same setup directory and output directory if self checking test')
            eflag = True
        if eflag == True:
            sys.exit(0)


    # If linker-only true, then generate linker and quit
    logger.info("Linker script generation started")
    args.seed = aapg.gen_random_program.gen_config_files(args)
    list_of_args = []

    for i in range(args.num_programs):
        list_of_args.append(myClass(num_programs,config_file,asm_name,setup_dir,output_dir,arch,int(args.seed)+i,linker_only,no_headers,self_checking,static_make))

    logger.info("Linker script generation completed")
    if args.linker_only:
        logger.info("linker-only option selected. Exiting aapg")
        sys.exit(0)

    process_list = []
    for index in range(args.num_programs):
        logger.info("Program number: {} started".format(index))
        p = Process(target = aapg.gen_random_program.run, args = (list_of_args[index], index))
        p.start()
        process_list.append(p)
        #args.seed = args.seed+1

    for p in process_list:
        p.join()

    for p in process_list:
        if p.exitcode == 1:
            sys.exit(1)

    if args.self_checking:
        aapg.setup_self_check.add_self_check(args.setup_dir,args.output_dir,args.config_file)
    sys.exit(0)

@cli.command()
@click.option('--setup_dir', default ='work', help='Setup directory of env files. Default ./work')
def setup(setup_dir):
    '''
    Function:   To setup directory structure to generate ASM programs
    Usage:      To be run before the `aapg gen` command
                aapg setup --help to understand the arguments
    '''
    setup_logging('info')
    logger = logging.getLogger()
    logger.handlers = []
    ch = logging.StreamHandler()
    ch.setFormatter(aapg.utils.ColoredFormatter())
    logger.addHandler(ch)
    logger.info("aapg started")
    logger.info(VERSION)
    logger.info("Command received: setup")
    aapg.env.env_setup.setup_build(setup_dir)
    aapg.utils.print_sample_config(setup_dir)
    logger.info("Setup directory built in {}".format(os.path.abspath(setup_dir)))

@cli.command()
def version():
    '''
    Function:   To return the current varsion of AAPG
    '''
    setup_logging('info')
    logger = logging.getLogger()
    logger.info(VERSION)

def yaml_2_yaml(file,logger):
    
    try:
        old_config_yaml = yaml.safe_load(open(file))
    except:
        logger.info('Unable to Load Yaml File')
        exit()
    new_config_yaml = {}
    
    if 'priv-mode' not in old_config_yaml.keys():
        new_config_yaml['priv-mode'] = {'mode':'m'}
    else:
        new_config_yaml['priv-mode'] = old_config_yaml['priv-mode']

    new_config_yaml['general'] = old_config_yaml['general']
    if 'custom_trap_handler' not in old_config_yaml['general'].keys():
        new_config_yaml['general']['custom_trap_handler'] = old_config_yaml['general']['user_trap_handler']
        del new_config_yaml['general']['user_trap_handler']
    if 'delegation' not in old_config_yaml['general'].keys():
        new_config_yaml['general']['delegation'] = False

    new_config_yaml['general']['code_start_address'] = hex(old_config_yaml['general']['code_start_address'])
    new_config_yaml['branch-control'] = old_config_yaml['branch-control']
    if 'block-size' not in old_config_yaml['branch-control'].keys():
        new_config_yaml['branch-control']['block-size'] = 7
    new_config_yaml['isa-instruction-distribution'] = old_config_yaml['isa-instruction-distribution']
    new_config_yaml['recursion-options'] = old_config_yaml['recursion-options']
    new_config_yaml['access-sections'] = old_config_yaml['access-sections']
    if '_test' in old_config_yaml['user-functions'].keys():
        new_config_yaml['user-functions'] = {'func1':"{"+str(old_config_yaml['user-functions']['_test'])+":\"addi x0,x0,0\"}"}
    else:
        new_config_yaml['user-functions'] = old_config_yaml['user-functions']

    if 'switch-priv-modes' in old_config_yaml.keys():
        new_config_yaml['switch-priv-modes'] = old_config_yaml['switch-priv-modes']
    else:
        new_config_yaml['switch-priv-modes'] = {'switch_modes': False, 'num_switches': 0}

    if 'csr-sections' in old_config_yaml.keys():
        new_config_yaml['csr-sections'] = old_config_yaml['switch-priv-modes']
    else:
        new_config_yaml['csr-sections'] = {'sections':'0x000:0xfff'}

    if 'self-checking' in old_config_yaml.keys():
        new_config_yaml['self-checking'] = old_config_yaml['self-checking']
    else:
        new_config_yaml['self-checking'] = {'rate':10, 'test_pass_macro':""" la      sp, begin_signature;\n addi    sp, sp, 2*REGBYTES;\n li      t1, 0xfffff;\n SREG    t1, 0*REGBYTES(sp)""", "test_fail_macro":"add x0,x0,x0"}

    new_config_yaml['i-cache'] = old_config_yaml['i-cache']
    new_config_yaml['d-cache'] = old_config_yaml['d-cache']
    new_config_yaml['exception-generation'] = old_config_yaml['exception-generation']
    new_config_yaml['data-hazards'] = old_config_yaml['data-hazards']

    if 'program-macro' not in old_config_yaml.keys():
        new_config_yaml['program-macro'] =  {'pre_program_macro': 'add x0,x0,x0', 'post_program_macro': 'add x0,x0,x0', 'pre_branch_macro': 'add x0,x0,x0', 'post_branch_macro': 'add x0,x0,x0', 'ecause00':'random', 'ecause01':'random', 'ecause02':'random', 'ecause03':'random', 'ecause04':'random', 'ecause05':'random', 'ecause06':'random', 'ecause07':'random', 'ecause08':'random', 'ecause09':'random', 'ecause10':'random', 'ecause11':'random', 'ecause12':'random', 'ecause13':'random', 'ecause14':'random', 'ecause15':'random'}
    else:
        new_config_yaml['program-macro'] = old_config_yaml['program-macro']
    if 'program-macro' in old_config_yaml.keys():
        if 'ecause00' not in old_config_yaml['program-macro'].keys():
            new_config_yaml['program-macro']['ecause00'] = "random"
        if 'ecause01' not in old_config_yaml['program-macro'].keys():
            new_config_yaml['program-macro']['ecause01'] = "random"
        if 'ecause02' not in old_config_yaml['program-macro'].keys():
            new_config_yaml['program-macro']['ecause02'] = "random"
        if 'ecause03' not in old_config_yaml['program-macro'].keys():
            new_config_yaml['program-macro']['ecause03'] = "random"
        if 'ecause04' not in old_config_yaml['program-macro'].keys():
            new_config_yaml['program-macro']['ecause04'] = "random"
        if 'ecause05' not in old_config_yaml['program-macro'].keys():
            new_config_yaml['program-macro']['ecause05'] = "random"
        if 'ecause06' not in old_config_yaml['program-macro'].keys():
            new_config_yaml['program-macro']['ecause06'] = "random"
        if 'ecause07' not in old_config_yaml['program-macro'].keys():
            new_config_yaml['program-macro']['ecause07'] = "random"
        if 'ecause08' not in old_config_yaml['program-macro'].keys():
            new_config_yaml['program-macro']['ecause08'] = "random"
        if 'ecause09' not in old_config_yaml['program-macro'].keys():
            new_config_yaml['program-macro']['ecause09'] = "random"
        if 'ecause10' not in old_config_yaml['program-macro'].keys():
            new_config_yaml['program-macro']['ecause10'] = "random"
        if 'ecause11' not in old_config_yaml['program-macro'].keys():
            new_config_yaml['program-macro']['ecause11'] = "random"
        if 'ecause12' not in old_config_yaml['program-macro'].keys():
            new_config_yaml['program-macro']['ecause12'] = "random"
        if 'ecause13' not in old_config_yaml['program-macro'].keys():
            new_config_yaml['program-macro']['ecause13'] = "random"
        if 'ecause14' not in old_config_yaml['program-macro'].keys():
            new_config_yaml['program-macro']['ecause14'] = "random"
        if 'ecause15' not in old_config_yaml['program-macro'].keys():
            new_config_yaml['program-macro']['ecause15'] = "random"


    f = open(file, 'w+')
    yaml.dump(new_config_yaml, f, default_flow_style=False,sort_keys=False)
    f.close()

    new_content = ""
    f = open(file,'r')
    for line in f:
        if not line:
            break
        if "code_start_address" in line:
            line = line.replace("'","")
            new_content = new_content + line
        elif "priv-mode:" in line:
            new_content = new_content + aapg.env.comments.priv_mode + line
        elif "general:" in line:
            new_content = new_content + aapg.env.comments.general + line
        elif "isa-instruction-distribution:" in line:
            new_content = new_content + aapg.env.comments.isadist + line
        elif "recursion-options:" in line:
            new_content = new_content + aapg.env.comments.recoptions + line
        elif "access-sections:" in line:
            new_content = new_content + aapg.env.comments.acc_sec + line
        elif "user-functions:" in line:
            new_content = new_content + aapg.env.comments.user_func + line
        elif "switch-priv-modes:" in line:
            new_content = new_content + aapg.env.comments.switching_priv_modes + line
        elif "i-cache:" in line:
            new_content = new_content + aapg.env.comments.i_cache + line
        elif "exception-generation:" in line:
            new_content = new_content + aapg.env.comments.exceptions + line
        elif "data-hazards:" in line:
            new_content = new_content + aapg.env.comments.data_hazards + line
        elif "csr-sections:" in line:
            new_content = new_content + aapg.env.comments.csr_sections + line
        else:
            new_content = new_content + line
    f.close()

    f = open(file,'w+')
    f.write(new_content)
    f.close()

@cli.command()
@click.option('--file', default ='config.yaml', help='Path to old config file. Default ./config.yaml')
def convert(file):
    '''
    Function:   To convert old formats of config files to newer versions
    Usage:      Takes path to old config file as argument and replaces it with the latest version of the config file
                Works with both .ini and .yaml files
    '''
    setup_logging('info')
    logger = logging.getLogger()
    logger.info(VERSION)
    logger.info('Updating existing configuration file')
    if not os.path.isfile(file):
        logger.info("Invalid File path")
        exit()

    name,ext = os.path.splitext(file)
    if ext == '.yaml':
        yaml_2_yaml(file,logger)
    elif ext == '.ini':
        new_filename = name+'.yaml'
        out = """"""
        f = open(file,'r')
        while(True):
            line = f.readline()
            if not line:
                break
            if "#" in line:
                out = out + line
            elif "[" in line:
                line = line.replace("[","")
                line = line.replace("]","")
                line = line[:-1]+":"+line[-1]
                out = out + line
            else:
                line = '  ' + line
                line = line.replace('=',': ')
                out = out + line 
        f.close()

        with open(new_filename, 'w') as outfile:
            outfile.write(out)
        yaml_2_yaml(new_filename,logger)
        

@cli.command()
@click.option('--setup_dir', default ='work', help='Setup directory of env files. Default ./')
@click.option('--output_dir', default ='work', help='Output directory for generated programs. Default: ./asm')
def clean(setup_dir,output_dir):
    '''
    Function:   To clean the directory where tests were generated
    Usage:      Takes path to setup and output directory and removes them
    '''
    setup_logging('info')
    logger = logging.getLogger()
    logger.info(VERSION)
    logger.info('Cleaning setup files....')
    if os.path.isdir(setup_dir):
        os.system('rm -r {setup_dir}'.format(setup_dir=setup_dir))
    else:
        if setup_dir=='work':
            logger.info('The default setup directory "work" does not exist')
        else:
            logger.error('The given setup directory does not exist!')

    if setup_dir != output_dir:
        logger.info('Cleaning gen files....')
        if os.path.isdir(output_dir):
            os.system('rm -r {output_dir}'.format(output_dir=output_dir))
        else:
            logger.warn('Default output directory "work" does not exist. \n Maybe gen command was not run? \n Maybe setup_dir and output_dir are same?')

    logger.info('Finished cleaning')


if __name__ == '__main__':
    cli()

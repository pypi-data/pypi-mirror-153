"""
    Automatic Assembly Program Generator (AAPG)

    Module of AAPG that deals with
        * Checking if signature file is created
        * Parsing signature file
        * Appending parseg signature file to test
        * Appending test function to template.S
"""
import logging
import argparse
import os
import io
import sys
import subprocess
import click
import yaml
import fileinput
from glob import glob

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


def format_sig(sig_file):
    """Format Signature

        Function to parse the generated signature files and return as list
    """
    f = open(sig_file,'r')
    to_write = []
    while(True):
        line = f.readline()
        if not line:
            break
        write_line2,write_line1 = line[0:16],line[16:32]
        write_line1 = '.dword 0x'+write_line1
        write_line2 = '.dword 0x'+write_line2
        to_write.append(write_line1)
        to_write.append(write_line2)
    f.close()
    return to_write

def add_function_call(test_file,x):
    if x == 2:
        for line in fileinput.input(test_file, inplace=True):
            if "post_program_macro" in line:
                if "#" not in line:
                    print("test_pass_macro\n", end='')
                    print(line, end='')
            elif "write_chsum" in line:
                line = line.replace("write_chsum","read_chsum")
                print(line, end='')
            else:
                print(line, end='')

    if x == 1:
        for line in fileinput.input(test_file, inplace=True):
            if "post_program_macro" in line:
                if "#" not in line:
                    print("call write_chsum\n", end='')
                    print(line, end='')
            else:
                print(line, end='')

def change_func_def(template_file):
    for line in fileinput.input(template_file, inplace=True):
        if "la                  sp, end_signature" in line:
            if "#" not in line:
                print("        la                  sp, end_ref_signature\n", end='')
        else:
            print(line, end='')


def add_self_check(setup_dir,output_dir,config_file):
    """Add Self Check

        Function to execute the makefile, extract signature and append to test

        Args:

    """
    setup_logging('info')
    logger = logging.getLogger()

    logger.info('Executing Makefile to generate signature dump \n')


    assembly = [y for x in os.walk(os.path.join(setup_dir,'asm')) for y in glob(os.path.join(x[0], '*.S'))]

    test_file = None
    template_file = None
    for file in assembly:
        if "template.S" not in file:
            test_file = file
        elif "template.S" in file:
            template_file = file

    # Calculate the size of the signature section
    # Still in development. Code to check if Data section is same
    conf = yaml.safe_load(open(os.path.join(setup_dir,config_file)))
    signature_start = None
    signature_end = None
    try:
        signature_section = conf['access-sections']['begin_signature']
        signature = signature_section.split(',')
        signature_start = int(signature[0],16)
        signature_end = int(signature[1],16)
    except:
        logger.error("Can not find `begin_signature` section in config file.")
        sys.exit(0)

    length = int((signature_end - signature_start)/8)
    logger.info("Size of signature section is {}".format(str(length)))
    length = length - 1

    func_to_add = """
.globl check_sign_func        
check_sign_func:
li t0, {}*REGBYTES
loop_label:
  la      sp, begin_signature
  add     sp, sp, t0
  LREG    t1, 0*REGBYTES(sp)

  la      sp, ref_signature
  add     sp, sp, t0
  LREG    t2, 0*REGBYTES(sp)

  bne     t1, t2, fail
  addi    t0, t0, -1*REGBYTES
  bgtz    t0, loop_label
pass:
  la      sp, begin_signature
  addi    sp, sp, 0 
  addi    t1, x0, 1
  SREG    t1, 0*REGBYTES(sp)
  ret
fail:
  la      sp, begin_signature
  addi    sp, sp, 0 
  addi    t1, x0, 0
  SREG    t1, 0*REGBYTES(sp)
  ret
    """.format(str(length))

    func_to_add2 = """
.option push;
.option norvc;
.globl write_chsum        
write_chsum:  
        csrw mscratch,   sp                 # store the sp in mscratch
        la   sp,  register_swap
        SREG x3, 1*REGBYTES(sp)
        SREG x4, 2*REGBYTES(sp)
        SREG x5, 3*REGBYTES(sp)
        SREG x6, 4*REGBYTES(sp)
        SREG x7, 5*REGBYTES(sp)
        SREG x8, 6*REGBYTES(sp)
        SREG x9, 7*REGBYTES(sp)
        SREG x10, 8*REGBYTES(sp)
        SREG x11, 9*REGBYTES(sp)
        SREG x12, 10*REGBYTES(sp)
        SREG x13, 11*REGBYTES(sp)
        SREG x14, 12*REGBYTES(sp)
        SREG x15, 13*REGBYTES(sp)
        SREG x16, 14*REGBYTES(sp)
        SREG x17, 15*REGBYTES(sp)
        SREG x18, 16*REGBYTES(sp)
        SREG x19, 17*REGBYTES(sp)
        SREG x20, 18*REGBYTES(sp)
        SREG x21, 19*REGBYTES(sp)
        SREG x22, 20*REGBYTES(sp)
        SREG x23, 21*REGBYTES(sp)
        SREG x24, 22*REGBYTES(sp)
        SREG x25, 23*REGBYTES(sp)
        SREG x26, 24*REGBYTES(sp)
        SREG x27, 25*REGBYTES(sp)
        SREG x28, 26*REGBYTES(sp)
        SREG x29, 27*REGBYTES(sp)
        SREG x30, 28*REGBYTES(sp)
        SREG x31, 29*REGBYTES(sp)
        SREG x1, 30*REGBYTES(sp)
        SREG x0, 31*REGBYTES(sp)
        csrr x30, mscratch                  # copy orig-sp in x30
        SREG x30, 32*REGBYTES(sp)           # store orig-sp
        li                  t6,  0
        li                  t4,  0
        li                  t3,  33
wnext_sum:
        addi                t4, t4, 1
        beq                 t4, t3, wfinchsum
        LREG                t5,  1*REGBYTES(sp)
        addi                sp, sp, 1*REGBYTES
        add                 t6, t6, t5
        bgt                 t6, t5, wnext_sum
        addi                t6, t6, 1
        beq                 x0, x0, wnext_sum 
wfinchsum:
        addi                t0, t0, -1*REGBYTES
        la                  sp, end_signature
        add                 sp, sp, t0
        SREG                t6, 0*REGBYTES(sp)
        la                  sp,  register_swap
        LREG x3, 1*REGBYTES(sp)
        LREG x4, 2*REGBYTES(sp)
        LREG x6, 4*REGBYTES(sp)
        LREG x7, 5*REGBYTES(sp)
        LREG x8, 6*REGBYTES(sp)
        LREG x9, 7*REGBYTES(sp)
        LREG x10, 8*REGBYTES(sp)
        LREG x11, 9*REGBYTES(sp)
        LREG x12, 10*REGBYTES(sp)
        LREG x13, 11*REGBYTES(sp)
        LREG x14, 12*REGBYTES(sp)
        LREG x15, 13*REGBYTES(sp)
        LREG x16, 14*REGBYTES(sp)
        LREG x17, 15*REGBYTES(sp)
        LREG x18, 16*REGBYTES(sp)
        LREG x19, 17*REGBYTES(sp)
        LREG x20, 18*REGBYTES(sp)
        LREG x21, 19*REGBYTES(sp)
        LREG x22, 20*REGBYTES(sp)
        LREG x23, 21*REGBYTES(sp)
        LREG x24, 22*REGBYTES(sp)
        LREG x25, 23*REGBYTES(sp)
        LREG x26, 24*REGBYTES(sp)
        LREG x27, 25*REGBYTES(sp)
        LREG x28, 26*REGBYTES(sp)
        LREG x29, 27*REGBYTES(sp)
        LREG x30, 28*REGBYTES(sp)
        LREG x31, 29*REGBYTES(sp)
        LREG x1, 30*REGBYTES(sp)
        csrr    sp, mscratch
        ret
.option pop;
    """

    func_to_add3 = """
.option push;
.option norvc;
.globl read_chsum        
read_chsum:       
        csrw                mscratch,   sp
        la                  sp,  register_swap
        SREG x3, 1*REGBYTES(sp)
        SREG x4, 2*REGBYTES(sp)
        SREG x5, 3*REGBYTES(sp)
        SREG x6, 4*REGBYTES(sp)
        SREG x7, 5*REGBYTES(sp)
        SREG x8, 6*REGBYTES(sp)
        SREG x9, 7*REGBYTES(sp)
        SREG x10, 8*REGBYTES(sp)
        SREG x11, 9*REGBYTES(sp)
        SREG x12, 10*REGBYTES(sp)
        SREG x13, 11*REGBYTES(sp)
        SREG x14, 12*REGBYTES(sp)
        SREG x15, 13*REGBYTES(sp)
        SREG x16, 14*REGBYTES(sp)
        SREG x17, 15*REGBYTES(sp)
        SREG x18, 16*REGBYTES(sp)
        SREG x19, 17*REGBYTES(sp)
        SREG x20, 18*REGBYTES(sp)
        SREG x21, 19*REGBYTES(sp)
        SREG x22, 20*REGBYTES(sp)
        SREG x23, 21*REGBYTES(sp)
        SREG x24, 22*REGBYTES(sp)
        SREG x25, 23*REGBYTES(sp)
        SREG x26, 24*REGBYTES(sp)
        SREG x27, 25*REGBYTES(sp)
        SREG x28, 26*REGBYTES(sp)
        SREG x29, 27*REGBYTES(sp)
        SREG x30, 28*REGBYTES(sp)
        SREG x31, 29*REGBYTES(sp)
        SREG x1, 30*REGBYTES(sp)
        SREG x0, 31*REGBYTES(sp)
        csrr x30, mscratch
        SREG x30, 32*REGBYTES(sp)
        li                  t6,  0
        li                  t4,  0
        li                  t3,  33
next_sum:
        addi                t4, t4, 1
        beq                 t4, t3, finchsum
        LREG                t5,  1*REGBYTES(sp)
        addi                sp, sp, 1*REGBYTES
        add                 t6, t6, t5
        bgt                 t6, t5, next_sum
        addi                t6, t6, 1
        beq                 x0, x0, next_sum
finchsum:
        addi                t0, t0, -1*REGBYTES
        la                  sp, end_signature
        add                 sp, sp, t0
        LREG                t2, 0*REGBYTES(sp)
        bne                 t6, t2, chfail
chpass:
        # la      sp, begin_signature
        # addi    sp, sp, 2*REGBYTES
        # li      t1, 0xfff
        # SREG    t1, 0*REGBYTES(sp)
        la                  sp,  register_swap
        LREG x3, 1*REGBYTES(sp)
        LREG x4, 2*REGBYTES(sp)
        LREG x6, 4*REGBYTES(sp)
        LREG x7, 5*REGBYTES(sp)
        LREG x8, 6*REGBYTES(sp)
        LREG x9, 7*REGBYTES(sp)
        LREG x10, 8*REGBYTES(sp)
        LREG x11, 9*REGBYTES(sp)
        LREG x12, 10*REGBYTES(sp)
        LREG x13, 11*REGBYTES(sp)
        LREG x14, 12*REGBYTES(sp)
        LREG x15, 13*REGBYTES(sp)
        LREG x16, 14*REGBYTES(sp)
        LREG x17, 15*REGBYTES(sp)
        LREG x18, 16*REGBYTES(sp)
        LREG x19, 17*REGBYTES(sp)
        LREG x20, 18*REGBYTES(sp)
        LREG x21, 19*REGBYTES(sp)
        LREG x22, 20*REGBYTES(sp)
        LREG x23, 21*REGBYTES(sp)
        LREG x24, 22*REGBYTES(sp)
        LREG x25, 23*REGBYTES(sp)
        LREG x26, 24*REGBYTES(sp)
        LREG x27, 25*REGBYTES(sp)
        LREG x28, 26*REGBYTES(sp)
        LREG x29, 27*REGBYTES(sp)
        LREG x30, 28*REGBYTES(sp)
        LREG x31, 29*REGBYTES(sp)
        LREG x1, 30*REGBYTES(sp)
        csrr sp, mscratch
        ret
chfail:
        la      sp, begin_signature
        addi    sp, sp, 2*REGBYTES
        sub     t0, x0, t0
        li      t1, 1*REGBYTES
        div     t0, t0, t1
        SREG    t0, 0*REGBYTES(sp)
        test_fail_macro
        post_program_macro
        ret
.option pop;
    """

    logger.info("Adding validation function to template file")

    check_function = func_to_add.split("\n")
    f = open(template_file,'a+')
    f.writelines(["%s\n" % item  for item in check_function])
    f.close()

    write_chsum_function = func_to_add2.split("\n")
    f = open(template_file,'a+')
    f.writelines(["%s\n" % item  for item in write_chsum_function])
    f.close()

    read_chsum_function = func_to_add3.split("\n")
    f = open(template_file,'a+')
    f.writelines(["%s\n" % item  for item in read_chsum_function])
    f.close()

    to_write1 = ['\t.data','\t.align 1','\t.globl ref_signature','ref_signature:']
    f = open(test_file,'a+')
    f.writelines(["%s\n" % item  for item in to_write1])
    f.close()
    
    # Execute MakeFile
    os.system("cd {};make".format(setup_dir))

    # Check if signature file exists
    signature = [y for x in os.walk(setup_dir) for y in glob(os.path.join(x[0], '*.dump.sign'))]
    if not signature:
        logger.error("Signature File was not created; Check if signature section is present in config/assembly")
        sys.exit(0)
    to_write = format_sig(signature[0])
    

    logger.info("Adding signature to the test file")

    f = open(test_file,'a+')
    f.writelines(["%s\n" % item  for item in to_write])
    f.close()

    to_write1 = ['\t.data','\t.align 1','\t.globl end_ref_signature','end_ref_signature:']
    f = open(test_file,'a+')
    f.writelines(["%s\n" % item  for item in to_write1])
    f.close()

    logger.info("Adding function call to test file")

    add_function_call(test_file,2)    
    change_func_def(template_file)
    os.system("cd {}; make clean".format(setup_dir))

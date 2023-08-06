"""
    Functions to setup the environment for building the generated asm
"""
import logging
import os

import aapg.env.prelude
import aapg.env.encoding
import aapg.env.linker
import aapg.env.make
import aapg.env.templates
import aapg.env.illegal_perl

logger = logging.getLogger(__name__)

def setup_build(output_dir):
    """ Setup the build directory
        This command does the following steps
        * Create the common directory and put crt.S and encoding.h there
        * Create a top level Makefile to make the programs
    """

    logger.info("Build setup started")
    output_path = os.path.abspath(output_dir)

    dirs = ['common', 'bin', 'log', 'objdump','asm']
    common_dir = os.path.join(output_path, dirs[0])
    out_dir = os.path.join(output_path, dirs[4])

    templates_file = 'templates.S'
    encoding_file = 'encoding.h'
    illegal_list = 'illegal.pl'
    make_file = 'Makefile'

    # Create the common directory 
    for dirname in dirs:
        try:
            os.makedirs(os.path.join(output_path, dirname))
        except FileExistsError as e:
            logger.warning('Folder exists. Not overwriting {}'.format(e))

    # Put the files in common
    with open(os.path.join(common_dir, encoding_file), 'w') as f:
        f.write(aapg.env.encoding.encoding_header.strip('\n'))

    with open(os.path.join(common_dir, illegal_list), 'w') as f:
        f.write(aapg.env.illegal_perl.perl_file.strip('\n'))

    # with open(os.path.join(out_dir, templates_file), 'w') as f:
    #     f.write(aapg.env.templates.templates_asm.strip('\n'))

    # with open(os.path.join(output_path, make_file), 'w') as f:
    #     f.write(aapg.env.make.makefile.strip('\n'))

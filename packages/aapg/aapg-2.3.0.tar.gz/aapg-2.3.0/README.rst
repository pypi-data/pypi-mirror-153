Automated Assembly Program Generator
===================================
Automated Assembly Program Generator (``aapg``) is a tool 
that is intended to generate random RISC-V programs
to test RISC-V cores.

Quick Install
-------------
There are two ways to get started with aapg. The easiest one is via pip.

.. code-block:: python

    pip install aapg

Next, Setup a working directory and build environment,

.. code-block:: bash
    
    aapg setup  

This creates the folders for the outputs of each step that is compiling the assembly to machine code, dumping a disassemly and then running the simulator on spike (riscv-isa-sim). It also creates a sample ``config.yaml`` to configure each ``aapg`` run.

Once the previous steps have been completed, we can run ``aapg``
using the following command.

.. code-block:: bash
    
    aapg gen 

By default, ``aapg`` generates 64 bit programs. To generate 32 bit programs, you have to run,

.. code-block:: bash

    aapg gen --arch rv32

You should find your random program generated in
``work/asm/out_config_00000.S`` in your current directory. By default,
``aapg`` expects the configuration file to be ``config.yaml``
and the output file will be ``work/asm/out_config_00000.S`` in the directory
that ``aapg`` was run in. To build the programs and run them on Spike,

.. code-block:: bash

    make

Alternatively for compiling using the 32-bit toolchain, you can type,

.. code-block:: bash

    make XLEN=32

You can check the logfiles in the ``log`` directory and the disassembled code in ``objdump`` directory.

Example config.yamls with all options can be found in the ```test/ci_cd_templates``` directory. 

To convert configuration files from older versions of aapg (either ``.ini`` or ``.yaml``) to newer versions, use the ``convert`` option,  

.. code-block:: bash

    aapg convert --file=/path/to/oldconfig

Developer Install
-----------------
The other way to install it is by using Git. This allows you to stay updated with the latest developments
and is required when you want to develop ``aapg`` further and push changes. You can follow these steps,

.. code-block:: bash
    
    git clone https://gitlab.com/shaktiproject/tools/aapg
    cd aapg
    python3 setup.py install

This will install aapg on your path.

Wiki
------------
Head to `Wiki 2.2.0 <https://gitlab.com/shaktiproject/tools/aapg/-/wikis/Wiki-AAPG-%5B2.2.0%5D>`_ for detailed information.  
For documentation on the older versions of AAPG, please visit, `Wiki 0.8.0 <https://gitlab.com/shaktiproject/tools/aapg/-/wikis/Wiki>`_ 

License
-------
Copyright (c) 2013-2020, IIT Madras
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

*  Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
*  Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
*  Neither the name of IIT Madras  nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 

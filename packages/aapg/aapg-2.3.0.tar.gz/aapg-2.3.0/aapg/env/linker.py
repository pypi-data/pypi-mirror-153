linker_script = '''
/*======================================================================*/
/* Baremetal Linker Script                                              */
/*======================================================================*/
/* Taken from riscv-tests
/*----------------------------------------------------------------------*/
/* Setup                                                                */
/*----------------------------------------------------------------------*/

/* The OUTPUT_ARCH command specifies the machine architecture where the
   argument is one of the names used in the BFD library. More
   specifically one of the entires in bfd/cpu-mips.c */

OUTPUT_ARCH( "riscv" )
ENTRY(_start)

/*----------------------------------------------------------------------*/
/* Sections                                                             */
/*----------------------------------------------------------------------*/

SECTIONS
{

  /* text: test code section */
  . = <!start_address!>;
  .text.init : { *(.text.init) }
  .text : { *(.text) }

  /* data segment */
  <!data_section!>

  <![tohost]
  . = ALIGN(0x100000);
  .tohost : { *(.tohost) } !>
  .rodata : { *(rodata) }

  /* End of uninitalized data segement */
  _end = .;
}
'''

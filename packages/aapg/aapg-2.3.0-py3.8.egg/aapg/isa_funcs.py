"""
    Module to generate random instruction and args based from a specified instruction set
"""
import random
import os

def set_seed_isa_funcs(seed):
    random.seed(seed)
# Dictionary to store all instructions
# Structure: 
# {
#    'isa-set': {
#         ['instr_template']
#    },
# }
inst_store_by_set = {
    'sys' : [
        'ecall     11..7=0 19..15=0 31..20=0x000 14..12=0 6..2=0x1C 1..0=3',
        'ebreak    11..7=0 19..15=0 31..20=0x001 14..12=0 6..2=0x1C 1..0=3',
        'uret      11..7=0 19..15=0 31..20=0x002 14..12=0 6..2=0x1C 1..0=3',
        'sret      11..7=0 19..15=0 31..20=0x102 14..12=0 6..2=0x1C 1..0=3',
        'mret      11..7=0 19..15=0 31..20=0x302 14..12=0 6..2=0x1C 1..0=3',
        'dret      11..7=0 19..15=0 31..20=0x7b2 14..12=0 6..2=0x1C 1..0=3',
        'sfence.vma 11..7=0 rs1 rs2 31..25=0x09  14..12=0 6..2=0x1C 1..0=3',
        'wfi       11..7=0 19..15=0 31..20=0x105 14..12=0 6..2=0x1C 1..0=3',
    ],
    'sys.csr' : [
        'csrrw     rd      uimm12 rs1      14..12=1 6..2=0x1C 1..0=3',
        'csrrs     rd      uimm12 rs1      14..12=2 6..2=0x1C 1..0=3',
        'csrrc     rd      uimm12 rs1      14..12=3 6..2=0x1C 1..0=3',
        'csrrwi    rd      uimm12   uimm5           14..12=5 6..2=0x1C 1..0=3',
        'csrrsi    rd      uimm12   uimm5           14..12=6 6..2=0x1C 1..0=3',
        'csrrci    rd      uimm12   uimm5           14..12=7 6..2=0x1C 1..0=3',
    ],
    'rv32i.ctrl' : [
        'beq     rs1 rs2 bimm12 14..12=0 6..2=0x18 1..0=3',
        'bne     rs1 rs2 bimm12 14..12=1 6..2=0x18 1..0=3',
        'blt     rs1 rs2 bimm12 14..12=4 6..2=0x18 1..0=3',
        'bge     rs1 rs2 bimm12 14..12=5 6..2=0x18 1..0=3',
        'bltu    rs1 rs2 bimm12 14..12=6 6..2=0x18 1..0=3',
        'bgeu    rs1 rs2 bimm12 14..12=7 6..2=0x18 1..0=3',
        'jalr    rd  rs1 bimm12 14..12=0 6..2=0x19 1..0=3',
        'jal     rd  bimm20              6..2=0x1b 1..0=3',
    ],
    'rv32i.compute': [
        'lui     rd imm20 6..2=0x0D 1..0=3',
        'auipc   rd imm20 6..2=0x05 1..0=3',
        'addi    rd rs1 imm12           14..12=0 6..2=0x04 1..0=3',
        'slti    rd rs1 imm12           14..12=2 6..2=0x04 1..0=3',
        'sltiu   rd rs1 imm12           14..12=3 6..2=0x04 1..0=3',
        'xori    rd rs1 imm12           14..12=4 6..2=0x04 1..0=3',
        'slli    rd rs1 31..25=0  shamtw 14..12=1 6..2=0x04 1..0=3',
        'srli    rd rs1 31..25=0  shamtw 14..12=5 6..2=0x04 1..0=3',
        'srai    rd rs1 31..25=32 shamtw 14..12=5 6..2=0x04 1..0=3',
        'ori     rd rs1 imm12           14..12=6 6..2=0x04 1..0=3',
        'andi    rd rs1 imm12           14..12=7 6..2=0x04 1..0=3',
        'add     rd rs1 rs2 31..25=0  14..12=0 6..2=0x0C 1..0=3',
        'sub     rd rs1 rs2 31..25=32 14..12=0 6..2=0x0C 1..0=3',
        'sll     rd rs1 rs2 31..25=0  14..12=1 6..2=0x0C 1..0=3',
        'slt     rd rs1 rs2 31..25=0  14..12=2 6..2=0x0C 1..0=3',
        'sltu    rd rs1 rs2 31..25=0  14..12=3 6..2=0x0C 1..0=3',
        'xor     rd rs1 rs2 31..25=0  14..12=4 6..2=0x0C 1..0=3',
        'srl     rd rs1 rs2 31..25=0  14..12=5 6..2=0x0C 1..0=3',
        'sra     rd rs1 rs2 31..25=32 14..12=5 6..2=0x0C 1..0=3',
        'or      rd rs1 rs2 31..25=0  14..12=6 6..2=0x0C 1..0=3',
        'and     rd rs1 rs2 31..25=0  14..12=7 6..2=0x0C 1..0=3'
    ],
    'rv32i.data' : [
        'lb      rd rs1       imm12 14..12=0 6..2=0x00 1..0=3',
        'lh      rd rs1       imm12 14..12=1 6..2=0x00 1..0=3',
        'lw      rd rs1       imm12 14..12=2 6..2=0x00 1..0=3',
        'lbu     rd rs1       imm12 14..12=4 6..2=0x00 1..0=3',
        'lhu     rd rs1       imm12 14..12=5 6..2=0x00 1..0=3',
        'sb      rs1 rs2 imm12 14..12=0 6..2=0x08 1..0=3',
        'sh      rs1 rs2 imm12 14..12=1 6..2=0x08 1..0=3',
        'sw      rs1 rs2 imm12 14..12=2 6..2=0x08 1..0=3',
    ],
    'rv32i.fence' : [
        'fence       31..28=ignore pred succ     19..15=ignore 14..12=0 11..7=ignore 6..2=0x03 1..0=3',
        'fence.i     31..28=ignore 27..20=ignore 19..15=ignore 14..12=1 11..7=ignore 6..2=0x03 1..0=3',
    ],
    'rv64i.compute' : [
        'addiw   rd rs1 imm12            14..12=0 6..2=0x06 1..0=3',
        'slliw   rd rs1 31..25=0  shamtw 14..12=1 6..2=0x06 1..0=3',
        'srliw   rd rs1 31..25=0  shamtw 14..12=5 6..2=0x06 1..0=3',
        'sraiw   rd rs1 31..25=32 shamtw 14..12=5 6..2=0x06 1..0=3',
        'addw    rd rs1 rs2 31..25=0  14..12=0 6..2=0x0E 1..0=3',
        'subw    rd rs1 rs2 31..25=32 14..12=0 6..2=0x0E 1..0=3',
        'sllw    rd rs1 rs2 31..25=0  14..12=1 6..2=0x0E 1..0=3',
        'srlw    rd rs1 rs2 31..25=0  14..12=5 6..2=0x0E 1..0=3',
        'sraw    rd rs1 rs2 31..25=32 14..12=5 6..2=0x0E 1..0=3',
        'slli    rd rs1 31..26=0  shamt 14..12=1 6..2=0x04 1..0=3',
        'srli    rd rs1 31..26=0  shamt 14..12=5 6..2=0x04 1..0=3',
        'srai    rd rs1 31..26=16 shamt 14..12=5 6..2=0x04 1..0=3',
    ],
    'rv64i.data' : [
        'ld      rd rs1       imm12 14..12=3 6..2=0x00 1..0=3',
        'lwu     rd rs1       imm12 14..12=6 6..2=0x00 1..0=3',
        'sd      rs1 rs2 imm12 14..12=3 6..2=0x08 1..0=3',
    ],
    'rv32m' : [
        'mul     rd rs1 rs2 31..25=1 14..12=0 6..2=0x0C 1..0=3',
        'mulh    rd rs1 rs2 31..25=1 14..12=1 6..2=0x0C 1..0=3',
        'mulhsu  rd rs1 rs2 31..25=1 14..12=2 6..2=0x0C 1..0=3',
        'mulhu   rd rs1 rs2 31..25=1 14..12=3 6..2=0x0C 1..0=3',
        'div     rd rs1 rs2 31..25=1 14..12=4 6..2=0x0C 1..0=3',
        'divu    rd rs1 rs2 31..25=1 14..12=5 6..2=0x0C 1..0=3',
        'rem     rd rs1 rs2 31..25=1 14..12=6 6..2=0x0C 1..0=3',
        'remu    rd rs1 rs2 31..25=1 14..12=7 6..2=0x0C 1..0=3',
    ],
    'rv64m' : [
        'mulw    rd rs1 rs2 31..25=1 14..12=0 6..2=0x0E 1..0=3',
        'divw    rd rs1 rs2 31..25=1 14..12=4 6..2=0x0E 1..0=3',
        'divuw   rd rs1 rs2 31..25=1 14..12=5 6..2=0x0E 1..0=3',
        'remw    rd rs1 rs2 31..25=1 14..12=6 6..2=0x0E 1..0=3',
        'remuw   rd rs1 rs2 31..25=1 14..12=7 6..2=0x0E 1..0=3',
    ],
    'rv32a' : [
        'amoadd.w    rd rs1 rs2      aqrl 31..29=0 28..27=0 14..12=2 6..2=0x0B 1..0=3',
        'amoxor.w    rd rs1 rs2      aqrl 31..29=1 28..27=0 14..12=2 6..2=0x0B 1..0=3',
        'amoor.w     rd rs1 rs2      aqrl 31..29=2 28..27=0 14..12=2 6..2=0x0B 1..0=3',
        'amoand.w    rd rs1 rs2      aqrl 31..29=3 28..27=0 14..12=2 6..2=0x0B 1..0=3',
        'amomin.w    rd rs1 rs2      aqrl 31..29=4 28..27=0 14..12=2 6..2=0x0B 1..0=3',
        'amomax.w    rd rs1 rs2      aqrl 31..29=5 28..27=0 14..12=2 6..2=0x0B 1..0=3',
        'amominu.w   rd rs1 rs2      aqrl 31..29=6 28..27=0 14..12=2 6..2=0x0B 1..0=3',
        'amomaxu.w   rd rs1 rs2      aqrl 31..29=7 28..27=0 14..12=2 6..2=0x0B 1..0=3',
        'amoswap.w   rd rs1 rs2      aqrl 31..29=0 28..27=1 14..12=2 6..2=0x0B 1..0=3',
        #'lr.w        rd rs1 24..20=0 aqrl 31..29=0 28..27=2 14..12=2 6..2=0x0B 1..0=3',
        #'sc.w        rd rs1 rs2      aqrl 31..29=0 28..27=3 14..12=2 6..2=0x0B 1..0=3',
    ],
    'rv64a' : [
        'amoadd.d    rd rs1 rs2      aqrl 31..29=0 28..27=0 14..12=3 6..2=0x0B 1..0=3',
        'amoxor.d    rd rs1 rs2      aqrl 31..29=1 28..27=0 14..12=3 6..2=0x0B 1..0=3',
        'amoor.d     rd rs1 rs2      aqrl 31..29=2 28..27=0 14..12=3 6..2=0x0B 1..0=3',
        'amoand.d    rd rs1 rs2      aqrl 31..29=3 28..27=0 14..12=3 6..2=0x0B 1..0=3',
        'amomin.d    rd rs1 rs2      aqrl 31..29=4 28..27=0 14..12=3 6..2=0x0B 1..0=3',
        'amomax.d    rd rs1 rs2      aqrl 31..29=5 28..27=0 14..12=3 6..2=0x0B 1..0=3',
        'amominu.d   rd rs1 rs2      aqrl 31..29=6 28..27=0 14..12=3 6..2=0x0B 1..0=3',
        'amomaxu.d   rd rs1 rs2      aqrl 31..29=7 28..27=0 14..12=3 6..2=0x0B 1..0=3',
        'amoswap.d   rd rs1 rs2      aqrl 31..29=0 28..27=1 14..12=3 6..2=0x0B 1..0=3',
        #'lr.d        rd rs1 24..20=0 aqrl 31..29=0 28..27=2 14..12=3 6..2=0x0B 1..0=3',
        #'sc.d        rd rs1 rs2      aqrl 31..29=0 28..27=3 14..12=3 6..2=0x0B 1..0=3',
    ],
    'rv32f' : [
        'flw       rdf rs1 imm12 14..12=2 6..2=0x01 1..0=3',
        'fsw       rs1f rs2 imm12 14..12=2 6..2=0x09 1..0=3',
        'fmadd.s   rdf rs1f rs2f rs3f rm 26..25=0 6..2=0x10 1..0=3',
        'fmsub.s   rdf rs1f rs2f rs3f rm 26..25=0 6..2=0x11 1..0=3',
        'fnmsub.s  rdf rs1f rs2f rs3f rm 26..25=0 6..2=0x12 1..0=3',
        'fnmadd.s  rdf rs1f rs2f rs3f rm 26..25=0 6..2=0x13 1..0=3',
        'fadd.s    rdf rs1f rs2f      31..27=0x00 rm       26..25=0 6..2=0x14 1..0=3',
        'fsub.s    rdf rs1f rs2f      31..27=0x01 rm       26..25=0 6..2=0x14 1..0=3',
        'fmul.s    rdf rs1f rs2f      31..27=0x02 rm       26..25=0 6..2=0x14 1..0=3',
        'fdiv.s    rdf rs1f rs2f      31..27=0x03 rm       26..25=0 6..2=0x14 1..0=3',
        'fsqrt.s   rdf rs1f 24..20=0 31..27=0x0B rm       26..25=0 6..2=0x14 1..0=3',
        'fsgnj.s   rdf rs1f rs2f      31..27=0x04 14..12=0 26..25=0 6..2=0x14 1..0=3',
        'fsgnjn.s  rdf rs1f rs2f      31..27=0x04 14..12=1 26..25=0 6..2=0x14 1..0=3',
        'fsgnjx.s  rdf rs1f rs2f      31..27=0x04 14..12=2 26..25=0 6..2=0x14 1..0=3',
        'fmin.s    rdf rs1f rs2f      31..27=0x05 14..12=0 26..25=0 6..2=0x14 1..0=3',
        'fmax.s    rdf rs1f rs2f      31..27=0x05 14..12=1 26..25=0 6..2=0x14 1..0=3',
        'fcvt.w.s  rd rs1f 24..20=0 31..27=0x18 rm       26..25=0 6..2=0x14 1..0=3',
        'fcvt.wu.s rd rs1f 24..20=1 31..27=0x18 rm       26..25=0 6..2=0x14 1..0=3',
        'fmv.x.w   rd rs1f 24..20=0 31..27=0x1C 14..12=0 26..25=0 6..2=0x14 1..0=3',
        'feq.s     rd rs1f rs2f      31..27=0x14 14..12=2 26..25=0 6..2=0x14 1..0=3',
        'flt.s     rd rs1f rs2f      31..27=0x14 14..12=1 26..25=0 6..2=0x14 1..0=3',
        'fle.s     rd rs1f rs2f      31..27=0x14 14..12=0 26..25=0 6..2=0x14 1..0=3',
        'fclass.s  rd rs1f 24..20=0 31..27=0x1C 14..12=1 26..25=0 6..2=0x14 1..0=3',
        'fcvt.s.w  rdf rs1 24..20=0 31..27=0x1A rm       26..25=0 6..2=0x14 1..0=3',
        'fcvt.s.wu rdf rs1 24..20=1 31..27=0x1A rm       26..25=0 6..2=0x14 1..0=3',
        'fmv.w.x   rdf rs1 24..20=0 31..27=0x1E 14..12=0 26..25=0 6..2=0x14 1..0=3',
    ],
    'rv32fr' : [
        'flw       rdf rs1 imm12 14..12=2 6..2=0x01 1..0=3',
        'fsw       rs1f rs2 imm12 14..12=2 6..2=0x09 1..0=3',
        'fmadd.s   rdf rs1f rs2f rs3f rm 26..25=0 6..2=0x10 1..0=3',
        'fmsub.s   rdf rs1f rs2f rs3f rm 26..25=0 6..2=0x11 1..0=3',
        'fnmsub.s  rdf rs1f rs2f rs3f rm 26..25=0 6..2=0x12 1..0=3',
        'fnmadd.s  rdf rs1f rs2f rs3f rm 26..25=0 6..2=0x13 1..0=3',
        'fadd.s    rdf rs1f rs2f      31..27=0x00 rm       26..25=0 6..2=0x14 1..0=3',
        'fsub.s    rdf rs1f rs2f      31..27=0x01 rm       26..25=0 6..2=0x14 1..0=3',
        'fmul.s    rdf rs1f rs2f      31..27=0x02 rm       26..25=0 6..2=0x14 1..0=3',
        'fdiv.s    rdf rs1f rs2f      31..27=0x03 rm       26..25=0 6..2=0x14 1..0=3',
        'fsqrt.s   rdf rs1f 24..20=0 31..27=0x0B rm       26..25=0 6..2=0x14 1..0=3',
        'fcvt.w.s  rd rs1f 24..20=0 31..27=0x18 rm       26..25=0 6..2=0x14 1..0=3',
        'fcvt.wu.s rd rs1f 24..20=1 31..27=0x18 rm       26..25=0 6..2=0x14 1..0=3',
        'fcvt.s.w  rdf rs1 24..20=0 31..27=0x1A rm       26..25=0 6..2=0x14 1..0=3',
        'fcvt.s.wu rdf rs1 24..20=1 31..27=0x1A rm       26..25=0 6..2=0x14 1..0=3',
    ],
    'rv64f' : [
        'fcvt.l.s  rd rs1f 24..20=2 31..27=0x18 rm       26..25=0 6..2=0x14 1..0=3',
        'fcvt.lu.s rd rs1f 24..20=3 31..27=0x18 rm       26..25=0 6..2=0x14 1..0=3',
        'fcvt.s.l  rdf rs1 24..20=2 31..27=0x1A rm       26..25=0 6..2=0x14 1..0=3',
        'fcvt.s.lu rdf rs1 24..20=3 31..27=0x1A rm       26..25=0 6..2=0x14 1..0=3',
    ],
    'rv64fr' : [
        'fcvt.l.s  rd rs1f 24..20=2 31..27=0x18 rm       26..25=0 6..2=0x14 1..0=3',
        'fcvt.lu.s rd rs1f 24..20=3 31..27=0x18 rm       26..25=0 6..2=0x14 1..0=3',
        'fcvt.s.l  rdf rs1 24..20=2 31..27=0x1A rm       26..25=0 6..2=0x14 1..0=3',
        'fcvt.s.lu rdf rs1 24..20=3 31..27=0x1A rm       26..25=0 6..2=0x14 1..0=3',
    ],
    'rv32d' : [
        'fld       rdf rs1 imm12 14..12=3 6..2=0x01 1..0=3',
        'fsd       rs1f rs2 imm12 14..12=3 6..2=0x09 1..0=3',
        'fmadd.d   rdf rs1f rs2f rs3f rm 26..25=1 6..2=0x10 1..0=3',
        'fmsub.d   rdf rs1f rs2f rs3f rm 26..25=1 6..2=0x11 1..0=3',
        'fnmsub.d  rdf rs1f rs2f rs3f rm 26..25=1 6..2=0x12 1..0=3',
        'fnmadd.d  rdf rs1f rs2f rs3f rm 26..25=1 6..2=0x13 1..0=3',
        'fadd.d    rdf rs1f rs2f      31..27=0x00 rm       26..25=1 6..2=0x14 1..0=3',
        'fsub.d    rdf rs1f rs2f      31..27=0x01 rm       26..25=1 6..2=0x14 1..0=3',
        'fmul.d    rdf rs1f rs2f      31..27=0x02 rm       26..25=1 6..2=0x14 1..0=3',
        'fdiv.d    rdf rs1f rs2f      31..27=0x03 rm       26..25=1 6..2=0x14 1..0=3',
        'fsqrt.d   rdf rs1f 24..20=0 31..27=0x0B rm       26..25=1 6..2=0x14 1..0=3',
        'fsgnj.d   rdf rs1f rs2f      31..27=0x04 14..12=0 26..25=1 6..2=0x14 1..0=3',
        'fsgnjn.d  rdf rs1f rs2f      31..27=0x04 14..12=1 26..25=1 6..2=0x14 1..0=3',
        'fsgnjx.d  rdf rs1f rs2f      31..27=0x04 14..12=2 26..25=1 6..2=0x14 1..0=3',
        'fmin.d    rdf rs1f rs2f      31..27=0x05 14..12=0 26..25=1 6..2=0x14 1..0=3',
        'fmax.d    rdf rs1f rs2f      31..27=0x05 14..12=1 26..25=1 6..2=0x14 1..0=3',
        'fcvt.s.d  rdf rs1f 24..20=1 31..27=0x08 rm       26..25=0 6..2=0x14 1..0=3',
        'fcvt.d.s  rdf rs1f 24..20=0 31..27=0x08 rm       26..25=1 6..2=0x14 1..0=3',
        'feq.d     rd rs1f rs2f      31..27=0x14 14..12=2 26..25=1 6..2=0x14 1..0=3',
        'flt.d     rd rs1f rs2f      31..27=0x14 14..12=1 26..25=1 6..2=0x14 1..0=3',
        'fle.d     rd rs1f rs2f      31..27=0x14 14..12=0 26..25=1 6..2=0x14 1..0=3',
        'fclass.d  rd rs1f 24..20=0 31..27=0x1C 14..12=1 26..25=1 6..2=0x14 1..0=3',
        'fcvt.w.d  rd rs1f 24..20=0 31..27=0x18 rm       26..25=1 6..2=0x14 1..0=3',
        'fcvt.wu.d rd rs1f 24..20=1 31..27=0x18 rm       26..25=1 6..2=0x14 1..0=3',
        'fcvt.d.w  rdf rs1 24..20=0 31..27=0x1A rm       26..25=1 6..2=0x14 1..0=3',
        'fcvt.d.wu rdf rs1 24..20=1 31..27=0x1A rm       26..25=1 6..2=0x14 1..0=3',
    ],
    'rv64d' : [
        'fcvt.l.d  rd rs1f 24..20=2 31..27=0x18 rm       26..25=1 6..2=0x14 1..0=3',
        'fcvt.lu.d rd rs1f 24..20=3 31..27=0x18 rm       26..25=1 6..2=0x14 1..0=3',
        'fmv.x.d   rd rs1f 24..20=0 31..27=0x1C 14..12=0 26..25=1 6..2=0x14 1..0=3',
        'fcvt.d.l  rdf rs1 24..20=2 31..27=0x1A rm       26..25=1 6..2=0x14 1..0=3',
        'fcvt.d.lu rdf rs1 24..20=3 31..27=0x1A rm       26..25=1 6..2=0x14 1..0=3',
        'fmv.d.x   rdf rs1 24..20=0 31..27=0x1E 14..12=0 26..25=1 6..2=0x14 1..0=3',
    ],
    'rvc.ctrl': [
        'c.j x0 imm11',
        'c.beqz rsprime1 x0 imm8',
        'c.bnez rsprime1 x0 imm8',
        'c.jr     x0  rs1 const0',
        'c.jalr x1 rs1 const0',
    ],
    'rvc.compute' : [
        'c.addi rd_rs1_prime nzimm6',
        'c.li rd x0 nzimm6',
        'c.lui rd nzuimm6',
        'c.andi rd_rs1_prime imm6',
        'c.sub rd_rs1_prime rsprime2',
        'c.xor rd_rs1_prime rsprime2',
        'c.or rd_rs1_prime rsprime2',
        'c.and rd_rs1_prime rsprime2',
        'c.add rd_rs1 rs2',
        'c.mv rd x0 rs2',
    ],
    'rvc.sp' : [
        'addi4spn rdprime sp nzuimm8',
        'c.addi16sp sp sp s16imm6',
    ],
    'rvc.data': [
        'c.lw rdprime rsprime1 s4uimm5',
        'c.sw rsprime1 rsprime2 s4uimm5',
        'c.lwsp  rd  sp  s4uimm6',
        'c.swsp  rs2  sp s4uimm6' 
    ],
    'rvc.fdata' : [
        'c.fld rdprimef rsprime1 s8uimm5',
        'c.fsd rsprime2f rsprime1 s8uimm5',
        'c.fldsp rdf sp  s8uimm6',
        'c.fsdsp rs2f sp s8uimm6',
    ],
    'rv32c.compute' : [
        'c.srli rd_rs1_prime nzuimm5',
        'c.srai rd_rs1_prime nzuimm5',
    ],
    'rv32c.ctrl' : [
        'c.jal x1 imm11',
    ],
    'rv32c.fdata' : [
        'c.flwsp rdf sp s4uimm6',
        'c.fswsp rs2f sp s4uimm6',
        'c.flw rdprimef rsprime1 s4uimm5',
        'c.fsw rsprime2f rsprime1 s4uimm5',
    ],
    'rv64c.compute': [
        'c.addiw rd_rs1_prime nzimm6',
        'c.srli rd_rs1_prime nzuimm6',
        'c.srai rd_rs1_prime nzuimm6',
        'c.slli rd_rs1_prime nzuimm6',
        'c.subw rd_rs1_prime rsprime2',
        'c.addw rd_rs1_prime rsprime2',
    ],
    'rv64c.data' : [
        'c.ld rdprime rsprime1 s8uimm5',
        'c.sd rsprime1 rsprime2 s8uimm5',
        'c.ldsp rd sp s8uimm6',
        'c.sdsp rs2 sp s8uimm6'
    ]
}

comp_insts_subs = {
    'addi4spn': 'addi',
    'c.fld': 'fld',
    'c.lw' : 'lw',
    'c.flw' : 'flw',
    'c.ld' : 'ld',
    'c.fsd' : 'fsd',
    'c.sw' : 'sw',
    'c.fsw' : 'fsw',
    'c.sd' : 'sd',
    'c.addi' : 'addi',
    'c.jal' : 'jal',
    'c.addiw' : 'addiw',
    'c.li' : 'addi',
    'c.addi16sp' : 'addi',
    'c.lui' : 'lui',
    'c.srli' : 'srli',
    'c.srai' : 'srai',
    'c.andi' : 'andi',
    'c.sub' : 'sub',
    'c.xor' : 'xor',
    'c.or' : 'or',
    'c.and' : 'and',
    'c.subw' : 'subw',
    'c.addw' : 'addw',
    'c.j' : 'jal',
    'c.beqz' : 'beq',
    'c.bnez' : 'bne',
    'c.slli' : 'slli',
    'c.fldsp' : 'fld',
    'c.lwsp' : 'lw',
    'c.flwsp' : 'flw',
    'c.ldsp' : 'ld',
    'c.jr' : 'jalr',
    'c.mv' : 'add',
    'c.jalr' : 'jalr',
    'c.add' : 'add',
    'c.fsdsp' : 'fsd', 
    'c.swsp' : 'sw',
    'c.fswsp' : 'fsw',
    'c.sdsp' : 'sd'
}

inst_store_fp_set = {key: inst_store_by_set[key] for key in ['rv32f', 'rv64f', 'rv32d', 'rv64d']}

fp_instrs = [inst.split(' ')[0] for inst_set in inst_store_fp_set.values() for inst in inst_set] 

atomic_insts = [x.split(' ')[0] for x in inst_store_by_set['rv32a'] + inst_store_by_set['rv64a']]

memory_insts = [x.split(' ')[0] for x in
        inst_store_by_set['rv32i.data'] +
        inst_store_by_set['rv64i.data'] +
        inst_store_by_set['rvc.data'] + 
        inst_store_by_set['rvc.fdata'] +
        inst_store_by_set['rv32c.fdata'] +
        inst_store_by_set['rv64c.data']
        ] + ['flw', 'fsw', 'fld', 'fsd']

float_insts = [x.split(' ')[0] for x in
        inst_store_by_set['rv32f'] +
        inst_store_by_set['rv64f'] +
        inst_store_by_set['rv32d'] + 
        inst_store_by_set['rv64d'] +
        inst_store_by_set['rv32c.fdata'] +
        inst_store_by_set['rv64c.data']
        ] + ['flw', 'fsw', 'fld', 'fsd']

float_insts_r = [x.split(' ')[0] for x in
        inst_store_by_set['rv32fr'] +
        inst_store_by_set['rv64fr']
        ]


comp_insts = [x.split(' ')[0] for x in
        inst_store_by_set['rvc.ctrl'] + 
        inst_store_by_set['rvc.compute'] + 
        inst_store_by_set['rvc.sp'] + 
        inst_store_by_set['rvc.data'] + 
        inst_store_by_set['rvc.fdata'] + 
        inst_store_by_set['rv32c.compute'] + 
        inst_store_by_set['rv32c.ctrl'] + 
        inst_store_by_set['rv32c.fdata'] + 
        inst_store_by_set['rv64c.compute'] +
        inst_store_by_set['rv64c.data']
]

ctrl_insts = [x.split(' ')[0] for x in inst_store_by_set['rv32i.ctrl']]

args_list = [
    'rd', 'rdf', 'rdprime', 'rdprimef',
    'rs1', 'rs1f','rsprime1', 'rsprime1f',
    'rs2', 'rs2f','rsprime2', 'rsprime2f',
    'rs3', 'rs3f',
    'rd_rs1_prime',
    'imm20',
    'imm12', 'imm11',
    'imm12lo',
    'imm12hi',
    'shamtw',
    'shamt',
    'rm',
    'imm6', 'nzuimm6', 'nzuimm5',
    'uimm5', 'uimm6',
    'uimm12',
    'imm8',
    'nzuimm8', 's8uimm5', 's4uimm5', 'nzimm6',
    's16imm6',
    'sp', 'x1', 'x0', 's8uimm6', 's4uimm6', 'const0', 'rd_rs1', 'rt',
    'bimm12', 'bimm20'
]

def get_random_inst_template(set_name):
    return random.choice(inst_store_by_set[set_name])

def get_random_inst_from_set(set_name):
    inst_template = get_random_inst_template(set_name)
    inst_tokens = inst_template.split(' ')
    return (inst_tokens[0], ) +  tuple(filter(lambda x: x in args_list, inst_tokens))

def is_floating_point(instr_name):
    ''' Check if given instruction name is floating point '''
    if instr_name in fp_instrs:
        return True
    else:
        return False

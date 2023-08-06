def make_format_func(isa_string,abi_string):
	makefile = '''
XLEN ?= 64
TARGET ?= unknown-elf
RISCVPREFIX=riscv${XLEN}-${TARGET}
ASM_SRC_DIR := asm
COMMON_DIR := common
BIN_DIR := bin
OBJ_DIR := objdump
LOG_DIR := log
ISA ?= {isa_string}
ABI ?= {abi_string}

INCLUDE_DIRS := common
CRT_FILE := common/crt.S
TEMPLATE_FILE := common/templates.S
GCC_OPTS := -march=$(ISA) -mabi=$(ABI) -DPREALLOCATE=1 -mcmodel=medany -static -std=gnu99 -O2 -fno-common -fno-builtin-printf
LINKER_OPTIONS := -static -nostdlib -nostartfiles -lm -lgcc -T 

BASE_SRC_FILES := $(wildcard $(ASM_SRC_DIR)/*.S)
SRC_FILES := $(filter-out $(wildcard $(ASM_SRC_DIR)/*template.S),$(BASE_SRC_FILES))
BIN_FILES := $(patsubst $(ASM_SRC_DIR)/%.S, $(BIN_DIR)/%.riscv, $(SRC_FILES))
OBJ_FILES := $(patsubst $(ASM_SRC_DIR)/%.S, $(OBJ_DIR)/%.objdump, $(SRC_FILES))
LOG_FILES := $(patsubst $(ASM_SRC_DIR)/%.S, $(LOG_DIR)/%.log, $(SRC_FILES))
DUMP_FILES := $(patsubst $(ASM_SRC_DIR)/%.S, $(LOG_DIR)/%.dump, $(SRC_FILES))

all: build objdump run dump
\t$(info ==================== Complete Build Finished =============)

build: $(BIN_FILES)
\t$(info ==================== Build completed ====================)
\t$(info )

$(BIN_DIR)/%.riscv: $(ASM_SRC_DIR)/%.S 
\t$(info ==================== Compiling asm to binary ============)
\t${RISCVPREFIX}-gcc $(GCC_OPTS) -I $(INCLUDE_DIRS) -o $@ $< $(CRT_FILE) $(LINKER_OPTIONS) $(<D)/$*.ld


objdump: $(OBJ_FILES)
\t$(info ==================== Objdump Completed ==================)
\t$(info )

$(OBJ_DIR)/%.objdump: $(BIN_DIR)/%.riscv
\t$(info ==================== Disassembling binary ===============)
\t${RISCVPREFIX}-objdump -D $< > $@

run: $(LOG_FILES)
\t$(info ==================== Spike Run Completed ================)
\t$(info )

$(LOG_DIR)/%.log: $(BIN_DIR)/%.riscv
\t$(info ==================== Simulating binary on Spike =========)
\tspike -l --isa=$(ISA) $< 2> $@

dump: $(DUMP_FILES)
\t$(info ==================== Spike dump Completed ===============)
\t$(info )

$(LOG_DIR)/%.dump: $(BIN_DIR)/%.riscv
\t$(info ==================== Generating spike dump ==============)
\tspike --log-commits --log  $@ --isa=$(ISA) +signature=$@.sign $<



.PHONY: clean
clean:
\trm -rf bin/* log/* objdump/*
'''.format(XLEN="{XLEN}",TARGET="{TARGET}",RISCVPREFIX="{RISCVPREFIX}",isa_string=isa_string,abi_string=abi_string)
	return makefile


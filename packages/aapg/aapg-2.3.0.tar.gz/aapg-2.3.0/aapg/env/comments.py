priv_mode = '''
# Sample config.yaml file to generate a random program
# using aapg (Automated Assembly Program Generator)

# Each section commands a behaviour of aapg
# and inline comments in each section will explain the
# usage
# ---------------------------------------------------------------------------------
# Privlege mode that instruction are executed in
# Options:
#       mode: m/s/u
# Note: If the privlege mode is either s or u, then the test_entry_macro
# will be defined accordingly
# ---------------------------------------------------------------------------------
'''
general = '''
# ---------------------------------------------------------------------------------
# General directives to aapg
# Options:
#       total_instructions: Approximate number of instructions to be generated
#                           by aapg. Actual may vary.
#       regs_not_use:       Comma separated list of RISC-V registers to not use for
#                           reading/writing in the random generated instructions
#       switching_modes:    DONT NOT PROVIDE ANY USER DEFINED 
#                           FUNCTIONS.
#                           
# ---------------------------------------------------------------------------------
'''
isadist = '''
# ---------------------------------------------------------------------------------
# Distribution of instructions according to ISA extensions
# Specify the relative frequency of each set 
# E.g. : A relative frequency of 1 each means each instruction will be 
# generated equal number of times in the total instructions. Specify 0 to disable.
# ---------------------------------------------------------------------------------
'''
recoptions = '''
# ---------------------------------------------------------------------------------
# Recursion options
# Options:
#       recursion_enable:   Generate the template for recursion or not
#       recursion_depth:    Number of times the recursive function is called
# ---------------------------------------------------------------------------------
'''
acc_sec = '''
# ---------------------------------------------------------------------------------
# Data access sections
# Specify which regions of memory will be accessed by the random program
# Options:
#       enable:         Force all memory accesses instructions to only load/store
#                       to the specified list of address sections
#                       
# Section Template: Specify legal access zones using the following template
#       section_name:  section_low,section_high (HEX)     
# ---------------------------------------------------------------------------------
'''
user_func = '''
# ---------------------------------------------------------------------------------
# User template sections
# Allows users to specify call to a custom function with number of times to call
# User should ensure that function does not modify 
#                       
# Section Template: Specify user template function calls with the number of times
#       function_name: '{number_of_times:"function_body"}'
# ---------------------------------------------------------------------------------
'''
switching_priv_modes = '''
# ---------------------------------------------------------------------------------
# Switching Privledge modes in AAPG
#       switching_modes:  true/false (Do not provide any user defined functions when
#                         shifting mdoes is true)
#       num_switches:     # of times privlege modes has to shift (This is randomised 
#                         and shifting may result in same mode)
# ---------------------------------------------------------------------------------
'''
i_cache = '''
# ---------------------------------------------------------------------------------
# Instruction Cache and Data-Cache Thrashing
# ---------------------------------------------------------------------------------
'''
exceptions = '''
# ---------------------------------------------------------------------------------
# Exception generation
# ---------------------------------------------------------------------------------
'''
data_hazards = '''
# ---------------------------------------------------------------------------------
# Data Hazards
# ---------------------------------------------------------------------------------
'''
csr_sections = '''
# ---------------------------------------------------------------------------------
# CSR sections
# Specify which CSRs will be accessed by the random program
# Options:              
#       sections:
#                 start-value1:end-value1, value2, start-value3:end-value3 (HEX)
#                 (Any Combination)
# ---------------------------------------------------------------------------------
'''
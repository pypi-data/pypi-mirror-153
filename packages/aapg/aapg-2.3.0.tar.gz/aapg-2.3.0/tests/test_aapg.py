import pytest 
import os
import random
import numpy as np
from random import seed
from random import randint
from click.testing import CliRunner
from aapg.main import cli
import sys

seed(1)

list_of_files = ['check_basic', 'check_branch', 'check_csr', 'check_switch_mode', 'check_exceptions', 'check_i_cache', 'check_recursion', 'check_all']


seeds = []

for _ in range(30):
    value = randint(0, 1000)
    seeds.append(value)

@pytest.fixture
def runner():
    return CliRunner()

@pytest.mark.serial
def test_print_seed(seed):
    print ("Displaying seed: "+seed)

@pytest.mark.serial
def test_setup(runner,seed):
    '''Testing setup option in serial mode'''
    result = runner.invoke(cli, ['setup','--setup_dir=work'])
    assert result.exit_code == 0

@pytest.mark.serial
def test_same_seed_gen1(runner,seed):
    '''Generating test with a seed'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--seed={gen_seed}'.format(gen_seed=seeds[1]),'--asm_name=test1'])
    assert result.exit_code == 0

@pytest.mark.serial
def test_same_seed_gen2(runner,seed):
    '''Generating test with a seed'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--seed={gen_seed}'.format(gen_seed=seeds[1]),'--asm_name=test2'])
    assert result.exit_code == 0

@pytest.mark.serial
def test_different_seed_gen3(runner,seed):
    '''Generating test with a seed'''
    result = runner.invoke(cli, ['gen','--setup_dir=work','--output_dir=work1','--seed={gen_seed}'.format(gen_seed=seeds[2]),'--asm_name=test3'])
    assert result.exit_code == 0

# @pytest.mark.serial
# def test_check_same_seed():
#     '''Generating another test with same seed'''
#     lines1_after_5 = None
#     lines2_after_5 = None
#     with open('work1/test1.S') as f:
#         lines1_after_5 = f.readlines()[5:]
#     with open('work1/test2.S') as f:
#         lines2_after_5 = f.readlines()[5:]
#     assert lines1_after_5 == lines2_after_5

@pytest.mark.serial
def test_check_different_seed():
    '''Check percentange of overlap between programs with different seed'''
    lines1_after_5 = None
    lines2_after_5 = None
    with open('work1/test1.S') as f:
        lines1_after_5 = f.readlines()[5:]
    with open('work1/test3.S') as f:
        lines2_after_5 = f.readlines()[5:]

    len_file_1 = len(lines1_after_5)
    len_file_2 = len(lines2_after_5)
    len_check = 0

    if len_file_1<len_file_2:
        len_check = len_file_1
    else:
        len_check = len_file_2

    lines_same = []
    for i in range(len_check):
        if lines1_after_5[i] == lines2_after_5[i]:
            lines_same.append(True)
        else:
            lines_same.append(False)

    lines_same = np.array(lines_same)
    percent_same = lines_same.mean()
    assert percent_same < 0.5

@pytest.mark.serial
def test_setup_for_clean(runner,seed):
    '''Setup directory to check clean option'''
    result = runner.invoke(cli, ['setup','--setup_dir=work_setup'])
    assert result.exit_code == 0

@pytest.mark.serial
def test_gen_for_clean(runner,seed):
    '''gen to check clean option'''
    result = runner.invoke(cli, ['gen','--setup_dir=work_setup','--output_dir=work_gen'])
    assert result.exit_code == 0

@pytest.mark.serial
def test_clean(runner,seed):
    '''gen to check clean option'''
    result = runner.invoke(cli, ['clean','--setup_dir=work_setup','--output_dir=work_gen'])
    assert result.exit_code == 0


@pytest.mark.timeout(200)
def test_basic(runner,seed):
    '''Testing check_basic.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/{config_file}'.format(config_file=list_of_files[0])])
    os.system('cp tests/ci_cd_templates/{config_file}.yaml tests/work/{config_file}/config.yaml'.format(config_file=list_of_files[0]))
    result = runner.invoke(cli, ['gen','--num_programs=10','--static_make','--setup_dir=tests/work/{config_file}'.format(config_file=list_of_files[0]),'--output_dir=tests/work/{config_file}/asm'.format(config_file=list_of_files[0])])
    try:
        out = os.system('cd tests/work/{config_file}; make'.format(config_file=list_of_files[0]))
        os.system('rm -rf tests/work/{config_file}'.format(config_file=list_of_files[0]))
    except:
        make = 0
    assert result.exit_code == 0 and make == 0


@pytest.mark.timeout(200)
def test_selfcheck(runner,seed):
    '''Testing self_checking.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/{config_file}'.format(config_file="self_checking")])
    os.system('cp tests/ci_cd_templates/{config_file}.yaml tests/work/{config_file}/config.yaml'.format(config_file="self_checking"))
    result = runner.invoke(cli, ['gen','--self_checking','--setup_dir=tests/work/{config_file}'.format(config_file="self_checking"),'--output_dir=tests/work/{config_file}/asm'.format(config_file="self_checking")])
    try:
        out = os.system('cd tests/work/{config_file}; make'.format(config_file="self_checking"))
        os.system('rm -rf tests/work/{config_file}'.format(config_file="self_checking"))
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_branch(runner,seed):
    '''Testing check_branch.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/{config_file}'.format(config_file=list_of_files[1])])
    os.system('cp tests/ci_cd_templates/{config_file}.yaml tests/work/{config_file}/config.yaml'.format(config_file=list_of_files[1]))
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/{config_file}'.format(config_file=list_of_files[1]),'--output_dir=tests/work/{config_file}/asm'.format(config_file=list_of_files[1])])
    try:
        os.system('cd tests/work/{config_file}; make'.format(config_file=list_of_files[1]))
        os.system('rm -rf tests/work/{config_file}'.format(config_file=list_of_files[1]))
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(15)
def test_csr(runner,seed):
    '''Testing check_basic.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/{config_file}'.format(config_file=list_of_files[2])])
    os.system('cp tests/ci_cd_templates/{config_file}.yaml tests/work/{config_file}/config.yaml'.format(config_file=list_of_files[2]))
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/{config_file}'.format(config_file=list_of_files[2]),'--output_dir=tests/work/{config_file}/asm'.format(config_file=list_of_files[2])])
    try:
        os.system('cd tests/work/{config_file}; make'.format(config_file=list_of_files[2]))
        os.system('rm -rf tests/work/{config_file}'.format(config_file=list_of_files[2]))
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_switch_mode(runner,seed):
    '''Testing check_basic.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/{config_file}'.format(config_file=list_of_files[3])])
    os.system('cp tests/ci_cd_templates/{config_file}.yaml tests/work/{config_file}/config.yaml'.format(config_file=list_of_files[3]))
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/{config_file}'.format(config_file=list_of_files[3]),'--output_dir=tests/work/{config_file}/asm'.format(config_file=list_of_files[3])])
    try:
        os.system('cd tests/work/{config_file}; make'.format(config_file=list_of_files[3]))
        os.system('rm -rf tests/work/{config_file}'.format(config_file=list_of_files[3]))
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_exceptions(runner,seed):
    '''Testing check_basic.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/{config_file}'.format(config_file=list_of_files[4])])
    os.system('cp tests/ci_cd_templates/{config_file}.yaml tests/work/{config_file}/config.yaml'.format(config_file=list_of_files[4]))
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/{config_file}'.format(config_file=list_of_files[4]),'--output_dir=tests/work/{config_file}/asm'.format(config_file=list_of_files[4])])
    try:
        os.system('cd tests/work/{config_file}; make'.format(config_file=list_of_files[4]))
        os.system('rm -rf tests/work/{config_file}'.format(config_file=list_of_files[4]))
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_i_cache(runner,seed):
    '''Testing check_basic.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/{config_file}'.format(config_file=list_of_files[5])])
    os.system('cp tests/ci_cd_templates/{config_file}.yaml tests/work/{config_file}/config.yaml'.format(config_file=list_of_files[5]))
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/{config_file}'.format(config_file=list_of_files[5]),'--output_dir=tests/work/{config_file}/asm'.format(config_file=list_of_files[5])])
    try:
        os.system('cd tests/work/{config_file}; make'.format(config_file=list_of_files[5]))
        os.system('rm -rf tests/work/{config_file}'.format(config_file=list_of_files[5]))
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_recursion(runner,seed):
    '''Testing check_basic.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/{config_file}'.format(config_file=list_of_files[6])])
    os.system('cp tests/ci_cd_templates/{config_file}.yaml tests/work/{config_file}/config.yaml'.format(config_file=list_of_files[6]))
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/{config_file}'.format(config_file=list_of_files[6]),'--output_dir=tests/work/{config_file}/asm'.format(config_file=list_of_files[6])])
    try:
        os.system('cd tests/work/{config_file}; make'.format(config_file=list_of_files[6]))
        os.system('rm -rf tests/work/{config_file}'.format(config_file=list_of_files[6]))
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

#@pytest.mark.timeout(15)
#def test_all(runner,seed):
#    '''Testing check_basic.yaml config file in parallel mode'''
#    make = 0
#    input_seed=int(seed)
#    runner.invoke(cli, ['setup','--setup_dir=tests/work/{config_file}'.format(config_file=list_of_files[7])])
#    os.system('cp tests/ci_cd_templates/{config_file}.yaml tests/work/{config_file}/config.yaml'.format(config_file=list_of_files[7]))
#    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/{config_file}'.format(config_file=list_of_files[7]),'--output_dir=tests/work/{config_file}/asm'.format(config_file=list_of_files[7])])
#    try:
#        os.system('cd tests/work/{config_file}; make'.format(config_file=list_of_files[7]))
#        os.system('rm -rf tests/work/{config_file}'.format(config_file=list_of_files[7]))
#    except:
#        make = 0
#    assert result.exit_code == 0 and make == 0


@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_hazards_s(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_hazards_s.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_hazards_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_hazards_s.yaml tests/work/aapg_iclass_rv64imafdc_hazards_s/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_hazards_s','--output_dir=tests/work/aapg_iclass_rv64imafdc_hazards_s/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_hazards_s; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_hazards_s')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_recurse_med(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_recurse_med.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_recurse_med'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_recurse_med.yaml tests/work/aapg_iclass_rv64imafdc_recurse_med/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_recurse_med','--output_dir=tests/work/aapg_iclass_rv64imafdc_recurse_med/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_recurse_med; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_recurse_med')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_hazards_u(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_hazards_u.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_hazards_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_hazards_u.yaml tests/work/aapg_cclass_rv64imafdc_hazards_u/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_hazards_u','--output_dir=tests/work/aapg_cclass_rv64imafdc_hazards_u/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_hazards_u; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_hazards_u')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_test_all2(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_test_all2.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_test_all2'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_test_all2.yaml tests/work/aapg_cclass_rv64imafdc_test_all2/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_test_all2','--output_dir=tests/work/aapg_cclass_rv64imafdc_test_all2/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_test_all2; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_test_all2')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_branches1(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_branches1.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_branches1'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_branches1.yaml tests/work/aapg_cclass_rv64imafdc_branches1/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_branches1','--output_dir=tests/work/aapg_cclass_rv64imafdc_branches1/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_branches1; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_branches1')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_bringup_s(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_bringup_s.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_bringup_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_bringup_s.yaml tests/work/aapg_cclass_rv64imafdc_bringup_s/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_bringup_s','--output_dir=tests/work/aapg_cclass_rv64imafdc_bringup_s/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_bringup_s; make')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_s_recursion(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_s_recursion.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_s_recursion'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_s_recursion.yaml tests/work/aapg_cclass_rv64imafdc_s_recursion/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_s_recursion','--output_dir=tests/work/aapg_cclass_rv64imafdc_s_recursion/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_s_recursion; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_s_recursion')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_branches1_u(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_branches1_u.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_branches1_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_branches1_u.yaml tests/work/aapg_iclass_rv64imafdc_branches1_u/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_branches1_u','--output_dir=tests/work/aapg_iclass_rv64imafdc_branches1_u/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_branches1_u; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_branches1_u')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_test_all2(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_test_all2.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_test_all2'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_test_all2.yaml tests/work/aapg_iclass_rv64imafdc_test_all2/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_test_all2','--output_dir=tests/work/aapg_iclass_rv64imafdc_test_all2/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_test_all2; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_test_all2')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_user_s(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_user_s.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_user_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_user_s.yaml tests/work/aapg_iclass_rv64imafdc_user_s/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_user_s','--output_dir=tests/work/aapg_iclass_rv64imafdc_user_s/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_user_s; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_user_s')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_user(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_user.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_user'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_user.yaml tests/work/aapg_cclass_rv64imafdc_user/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_user','--output_dir=tests/work/aapg_cclass_rv64imafdc_user/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_user; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_user')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_bringup(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_bringup.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_bringup'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_bringup.yaml tests/work/aapg_iclass_rv64imafdc_bringup/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_bringup','--output_dir=tests/work/aapg_iclass_rv64imafdc_bringup/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_bringup; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_bringup')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_hazards(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_hazards.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_hazards'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_hazards.yaml tests/work/aapg_cclass_rv64imafdc_hazards/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_hazards','--output_dir=tests/work/aapg_cclass_rv64imafdc_hazards/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_hazards; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_hazards')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_user(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_user.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_user'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_user.yaml tests/work/aapg_iclass_rv64imafdc_user/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_user','--output_dir=tests/work/aapg_iclass_rv64imafdc_user/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_user; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_user')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_branches1(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_branches1.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_branches1'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_branches1.yaml tests/work/aapg_iclass_rv64imafdc_branches1/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_branches1','--output_dir=tests/work/aapg_iclass_rv64imafdc_branches1/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_branches1; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_branches1')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_exceptions_u(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_exceptions_u.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_exceptions_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_exceptions_u.yaml tests/work/aapg_cclass_rv64imafdc_exceptions_u/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_exceptions_u','--output_dir=tests/work/aapg_cclass_rv64imafdc_exceptions_u/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_exceptions_u; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_exceptions_u')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_hazards(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_hazards.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_hazards'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_hazards.yaml tests/work/aapg_iclass_rv64imafdc_hazards/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_hazards','--output_dir=tests/work/aapg_iclass_rv64imafdc_hazards/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_hazards; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_hazards')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_recursion_branch(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_recursion_branch.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_recursion_branch'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_recursion_branch.yaml tests/work/aapg_iclass_rv64imafdc_recursion_branch/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_recursion_branch','--output_dir=tests/work/aapg_iclass_rv64imafdc_recursion_branch/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_recursion_branch; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_recursion_branch')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_hazards_u(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_hazards_u.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_hazards_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_hazards_u.yaml tests/work/aapg_iclass_rv64imafdc_hazards_u/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_hazards_u','--output_dir=tests/work/aapg_iclass_rv64imafdc_hazards_u/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_hazards_u; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_hazards_u')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_exceptions_u(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_exceptions_u.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_exceptions_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_exceptions_u.yaml tests/work/aapg_iclass_rv64imafdc_exceptions_u/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_exceptions_u','--output_dir=tests/work/aapg_iclass_rv64imafdc_exceptions_u/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_exceptions_u; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_exceptions_u')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_branches1_s(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_branches1_s.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_branches1_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_branches1_s.yaml tests/work/aapg_cclass_rv64imafdc_branches1_s/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_branches1_s','--output_dir=tests/work/aapg_cclass_rv64imafdc_branches1_s/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_branches1_s; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_branches1_s')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_bringup_u(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_bringup_u.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_bringup_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_bringup_u.yaml tests/work/aapg_cclass_rv64imafdc_bringup_u/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_bringup_u','--output_dir=tests/work/aapg_cclass_rv64imafdc_bringup_u/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_bringup_u; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_bringup_u')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_illegal(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_illegal.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_illegal'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_illegal.yaml tests/work/aapg_iclass_rv64imafdc_illegal/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_illegal','--output_dir=tests/work/aapg_iclass_rv64imafdc_illegal/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_illegal; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_illegal')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_bringup_s(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_bringup_s.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_bringup_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_bringup_s.yaml tests/work/aapg_iclass_rv64imafdc_bringup_s/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_bringup_s','--output_dir=tests/work/aapg_iclass_rv64imafdc_bringup_s/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_bringup_s; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_bringup_s')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_user_s(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_user_s.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_user_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_user_s.yaml tests/work/aapg_cclass_rv64imafdc_user_s/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_user_s','--output_dir=tests/work/aapg_cclass_rv64imafdc_user_s/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_user_s; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_user_s')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_illegal_u(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_illegal_u.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_illegal_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_illegal_u.yaml tests/work/aapg_cclass_rv64imafdc_illegal_u/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_illegal_u','--output_dir=tests/work/aapg_cclass_rv64imafdc_illegal_u/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_illegal_u; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_illegal_u')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_recursion_branch(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_recursion_branch.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_recursion_branch'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_recursion_branch.yaml tests/work/aapg_cclass_rv64imafdc_recursion_branch/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_recursion_branch','--output_dir=tests/work/aapg_cclass_rv64imafdc_recursion_branch/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_recursion_branch; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_recursion_branch')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_bringup(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_bringup.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_bringup'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_bringup.yaml tests/work/aapg_cclass_rv64imafdc_bringup/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_bringup','--output_dir=tests/work/aapg_cclass_rv64imafdc_bringup/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_bringup; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_bringup')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_exceptions(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_exceptions.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_exceptions'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_exceptions.yaml tests/work/aapg_iclass_rv64imafdc_exceptions/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_exceptions','--output_dir=tests/work/aapg_iclass_rv64imafdc_exceptions/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_exceptions; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_exceptions')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_branches1_s(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_branches1_s.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_branches1_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_branches1_s.yaml tests/work/aapg_iclass_rv64imafdc_branches1_s/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_branches1_s','--output_dir=tests/work/aapg_iclass_rv64imafdc_branches1_s/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_branches1_s; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_branches1_s')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_s_recursion(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_s_recursion.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_s_recursion'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_s_recursion.yaml tests/work/aapg_iclass_rv64imafdc_s_recursion/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_s_recursion','--output_dir=tests/work/aapg_iclass_rv64imafdc_s_recursion/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_s_recursion; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_s_recursion')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_illegal_u(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_illegal_u.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_illegal_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_illegal_u.yaml tests/work/aapg_iclass_rv64imafdc_illegal_u/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_illegal_u','--output_dir=tests/work/aapg_iclass_rv64imafdc_illegal_u/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_illegal_u; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_illegal_u')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_hazards_s(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_hazards_s.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_hazards_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_hazards_s.yaml tests/work/aapg_cclass_rv64imafdc_hazards_s/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_hazards_s','--output_dir=tests/work/aapg_cclass_rv64imafdc_hazards_s/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_hazards_s; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_hazards_s')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_user_u(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_user_u.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_user_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_user_u.yaml tests/work/aapg_cclass_rv64imafdc_user_u/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_user_u','--output_dir=tests/work/aapg_cclass_rv64imafdc_user_u/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_user_u; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_user_u')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_exceptions_s(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_exceptions_s.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_exceptions_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_exceptions_s.yaml tests/work/aapg_cclass_rv64imafdc_exceptions_s/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_exceptions_s','--output_dir=tests/work/aapg_cclass_rv64imafdc_exceptions_s/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_exceptions_s; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_exceptions_s')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_test_all(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_test_all.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_test_all'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_test_all.yaml tests/work/aapg_cclass_rv64imafdc_test_all/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_test_all','--output_dir=tests/work/aapg_cclass_rv64imafdc_test_all/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_test_all; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_test_all')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_test_all(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_test_all.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_test_all'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_test_all.yaml tests/work/aapg_iclass_rv64imafdc_test_all/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_test_all','--output_dir=tests/work/aapg_iclass_rv64imafdc_test_all/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_test_all; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_test_all')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_recurse_low(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_recurse_low.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_recurse_low'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_recurse_low.yaml tests/work/aapg_iclass_rv64imafdc_recurse_low/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_recurse_low','--output_dir=tests/work/aapg_iclass_rv64imafdc_recurse_low/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_recurse_low; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_recurse_low')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_branches1_u(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_branches1_u.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_branches1_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_branches1_u.yaml tests/work/aapg_cclass_rv64imafdc_branches1_u/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_branches1_u','--output_dir=tests/work/aapg_cclass_rv64imafdc_branches1_u/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_branches1_u; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_branches1_u')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_exceptions(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_exceptions.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_exceptions'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_exceptions.yaml tests/work/aapg_cclass_rv64imafdc_exceptions/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_exceptions','--output_dir=tests/work/aapg_cclass_rv64imafdc_exceptions/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_exceptions; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_exceptions')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_illegal_s(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_illegal_s.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_illegal_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_illegal_s.yaml tests/work/aapg_cclass_rv64imafdc_illegal_s/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_illegal_s','--output_dir=tests/work/aapg_cclass_rv64imafdc_illegal_s/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_illegal_s; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_illegal_s')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_recurse_med(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_recurse_med.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_recurse_med'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_recurse_med.yaml tests/work/aapg_cclass_rv64imafdc_recurse_med/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_recurse_med','--output_dir=tests/work/aapg_cclass_rv64imafdc_recurse_med/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_recurse_med; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_recurse_med')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_user_u(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_user_u.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_user_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_user_u.yaml tests/work/aapg_iclass_rv64imafdc_user_u/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_user_u','--output_dir=tests/work/aapg_iclass_rv64imafdc_user_u/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_user_u; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_user_u')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_bringup_u(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_bringup_u.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_bringup_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_bringup_u.yaml tests/work/aapg_iclass_rv64imafdc_bringup_u/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_bringup_u','--output_dir=tests/work/aapg_iclass_rv64imafdc_bringup_u/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_bringup_u; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_bringup_u')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_illegal(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_illegal.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_illegal'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_illegal.yaml tests/work/aapg_cclass_rv64imafdc_illegal/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_illegal','--output_dir=tests/work/aapg_cclass_rv64imafdc_illegal/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_illegal; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_illegal')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_cclass_rv64imafdc_recurse_low(runner,seed):
    '''Testing aapg_cclass_rv64imafdc_recurse_low.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_recurse_low'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_recurse_low.yaml tests/work/aapg_cclass_rv64imafdc_recurse_low/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_cclass_rv64imafdc_recurse_low','--output_dir=tests/work/aapg_cclass_rv64imafdc_recurse_low/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_recurse_low; make')
        os.system('rm -rf tests/work/aapg_cclass_rv64imafdc_recurse_low')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_exceptions_s(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_exceptions_s.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_exceptions_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_exceptions_s.yaml tests/work/aapg_iclass_rv64imafdc_exceptions_s/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_exceptions_s','--output_dir=tests/work/aapg_iclass_rv64imafdc_exceptions_s/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_exceptions_s; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_exceptions_s')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_illegal_s(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_illegal_s.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_illegal_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_illegal_s.yaml tests/work/aapg_iclass_rv64imafdc_illegal_s/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_illegal_s','--output_dir=tests/work/aapg_iclass_rv64imafdc_illegal_s/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_illegal_s; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_illegal_s')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0


@pytest.mark.timeout(200)
def test_aapg_iclass_rv64imafdc_fpu_hazards(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_fpu_hazards.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_fpu_hazards'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_fpu_hazards.yaml tests/work/aapg_iclass_rv64imafdc_fpu_hazards/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_fpu_hazards','--output_dir=tests/work/aapg_iclass_rv64imafdc_fpu_hazards/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_fpu_hazards; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_fpu_hazards')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(200)

def test_aapg_iclass_rv64imafdc_while_test(runner,seed):
    '''Testing aapg_iclass_rv64imafdc_while_test.yaml config file in parallel mode'''
    make = 0
    input_seed=int(seed)
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_while_test'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_while_test.yaml tests/work/aapg_iclass_rv64imafdc_while_test/config.yaml')
    result = runner.invoke(cli, ['gen','--num_programs=2','--static_make','--seed={}'.format(input_seed),'--setup_dir=tests/work/aapg_iclass_rv64imafdc_while_test','--output_dir=tests/work/aapg_iclass_rv64imafdc_while_test/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_while_test; make')
        os.system('rm -rf tests/work/aapg_iclass_rv64imafdc_while_test')
    except:
        make = 0
    assert result.exit_code == 0 and make == 0

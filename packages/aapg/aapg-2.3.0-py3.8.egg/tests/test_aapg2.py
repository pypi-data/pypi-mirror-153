import pytest 
import os
import random
import numpy as np
from random import seed
from random import randint
from click.testing import CliRunner
from aapg.main import cli

seeds = []
seed(1)
for _ in range(30):
    value = randint(0, 1000)
    seeds.append(value)

@pytest.fixture
def runner():
    return CliRunner()

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_hazards_s(runner):
    """Testing aapg_iclass_rv64imafdc_hazards_s.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_hazards_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_hazards_s.yaml tests/work/aapg_iclass_rv64imafdc_hazards_s/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_hazards_s','--output_dir=tests/work/aapg_iclass_rv64imafdc_hazards_s/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_hazards_s; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_recurse_med(runner):
    """Testing aapg_iclass_rv64imafdc_recurse_med.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_recurse_med'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_recurse_med.yaml tests/work/aapg_iclass_rv64imafdc_recurse_med/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_recurse_med','--output_dir=tests/work/aapg_iclass_rv64imafdc_recurse_med/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_recurse_med; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_hazards_u(runner):
    """Testing aapg_cclass_rv64imafdc_hazards_u.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_hazards_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_hazards_u.yaml tests/work/aapg_cclass_rv64imafdc_hazards_u/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_hazards_u','--output_dir=tests/work/aapg_cclass_rv64imafdc_hazards_u/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_hazards_u; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_test_all2(runner):
    """Testing aapg_cclass_rv64imafdc_test_all2.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_test_all2'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_test_all2.yaml tests/work/aapg_cclass_rv64imafdc_test_all2/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_test_all2','--output_dir=tests/work/aapg_cclass_rv64imafdc_test_all2/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_test_all2; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_branches1(runner):
    """Testing aapg_cclass_rv64imafdc_branches1.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_branches1'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_branches1.yaml tests/work/aapg_cclass_rv64imafdc_branches1/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_branches1','--output_dir=tests/work/aapg_cclass_rv64imafdc_branches1/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_branches1; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_bringup_s(runner):
    """Testing aapg_cclass_rv64imafdc_bringup_s.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_bringup_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_bringup_s.yaml tests/work/aapg_cclass_rv64imafdc_bringup_s/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_bringup_s','--output_dir=tests/work/aapg_cclass_rv64imafdc_bringup_s/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_bringup_s; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_s_recursion(runner):
    """Testing aapg_cclass_rv64imafdc_s_recursion.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_s_recursion'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_s_recursion.yaml tests/work/aapg_cclass_rv64imafdc_s_recursion/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_s_recursion','--output_dir=tests/work/aapg_cclass_rv64imafdc_s_recursion/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_s_recursion; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_branches1_u(runner):
    """Testing aapg_iclass_rv64imafdc_branches1_u.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_branches1_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_branches1_u.yaml tests/work/aapg_iclass_rv64imafdc_branches1_u/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_branches1_u','--output_dir=tests/work/aapg_iclass_rv64imafdc_branches1_u/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_branches1_u; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_test_all2(runner):
    """Testing aapg_iclass_rv64imafdc_test_all2.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_test_all2'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_test_all2.yaml tests/work/aapg_iclass_rv64imafdc_test_all2/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_test_all2','--output_dir=tests/work/aapg_iclass_rv64imafdc_test_all2/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_test_all2; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_user_s(runner):
    """Testing aapg_iclass_rv64imafdc_user_s.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_user_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_user_s.yaml tests/work/aapg_iclass_rv64imafdc_user_s/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_user_s','--output_dir=tests/work/aapg_iclass_rv64imafdc_user_s/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_user_s; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_user(runner):
    """Testing aapg_cclass_rv64imafdc_user.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_user'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_user.yaml tests/work/aapg_cclass_rv64imafdc_user/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_user','--output_dir=tests/work/aapg_cclass_rv64imafdc_user/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_user; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_bringup(runner):
    """Testing aapg_iclass_rv64imafdc_bringup.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_bringup'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_bringup.yaml tests/work/aapg_iclass_rv64imafdc_bringup/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_bringup','--output_dir=tests/work/aapg_iclass_rv64imafdc_bringup/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_bringup; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_hazards(runner):
    """Testing aapg_cclass_rv64imafdc_hazards.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_hazards'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_hazards.yaml tests/work/aapg_cclass_rv64imafdc_hazards/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_hazards','--output_dir=tests/work/aapg_cclass_rv64imafdc_hazards/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_hazards; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_user(runner):
    """Testing aapg_iclass_rv64imafdc_user.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_user'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_user.yaml tests/work/aapg_iclass_rv64imafdc_user/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_user','--output_dir=tests/work/aapg_iclass_rv64imafdc_user/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_user; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_branches1(runner):
    """Testing aapg_iclass_rv64imafdc_branches1.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_branches1'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_branches1.yaml tests/work/aapg_iclass_rv64imafdc_branches1/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_branches1','--output_dir=tests/work/aapg_iclass_rv64imafdc_branches1/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_branches1; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_exceptions_u(runner):
    """Testing aapg_cclass_rv64imafdc_exceptions_u.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_exceptions_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_exceptions_u.yaml tests/work/aapg_cclass_rv64imafdc_exceptions_u/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_exceptions_u','--output_dir=tests/work/aapg_cclass_rv64imafdc_exceptions_u/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_exceptions_u; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_hazards(runner):
    """Testing aapg_iclass_rv64imafdc_hazards.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_hazards'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_hazards.yaml tests/work/aapg_iclass_rv64imafdc_hazards/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_hazards','--output_dir=tests/work/aapg_iclass_rv64imafdc_hazards/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_hazards; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_recursion_branch(runner):
    """Testing aapg_iclass_rv64imafdc_recursion_branch.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_recursion_branch'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_recursion_branch.yaml tests/work/aapg_iclass_rv64imafdc_recursion_branch/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_recursion_branch','--output_dir=tests/work/aapg_iclass_rv64imafdc_recursion_branch/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_recursion_branch; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_hazards_u(runner):
    """Testing aapg_iclass_rv64imafdc_hazards_u.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_hazards_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_hazards_u.yaml tests/work/aapg_iclass_rv64imafdc_hazards_u/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_hazards_u','--output_dir=tests/work/aapg_iclass_rv64imafdc_hazards_u/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_hazards_u; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_exceptions_u(runner):
    """Testing aapg_iclass_rv64imafdc_exceptions_u.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_exceptions_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_exceptions_u.yaml tests/work/aapg_iclass_rv64imafdc_exceptions_u/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_exceptions_u','--output_dir=tests/work/aapg_iclass_rv64imafdc_exceptions_u/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_exceptions_u; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_branches1_s(runner):
    """Testing aapg_cclass_rv64imafdc_branches1_s.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_branches1_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_branches1_s.yaml tests/work/aapg_cclass_rv64imafdc_branches1_s/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_branches1_s','--output_dir=tests/work/aapg_cclass_rv64imafdc_branches1_s/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_branches1_s; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_bringup_u(runner):
    """Testing aapg_cclass_rv64imafdc_bringup_u.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_bringup_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_bringup_u.yaml tests/work/aapg_cclass_rv64imafdc_bringup_u/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_bringup_u','--output_dir=tests/work/aapg_cclass_rv64imafdc_bringup_u/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_bringup_u; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_illegal(runner):
    """Testing aapg_iclass_rv64imafdc_illegal.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_illegal'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_illegal.yaml tests/work/aapg_iclass_rv64imafdc_illegal/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_illegal','--output_dir=tests/work/aapg_iclass_rv64imafdc_illegal/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_illegal; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_bringup_s(runner):
    """Testing aapg_iclass_rv64imafdc_bringup_s.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_bringup_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_bringup_s.yaml tests/work/aapg_iclass_rv64imafdc_bringup_s/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_bringup_s','--output_dir=tests/work/aapg_iclass_rv64imafdc_bringup_s/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_bringup_s; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_user_s(runner):
    """Testing aapg_cclass_rv64imafdc_user_s.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_user_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_user_s.yaml tests/work/aapg_cclass_rv64imafdc_user_s/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_user_s','--output_dir=tests/work/aapg_cclass_rv64imafdc_user_s/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_user_s; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_illegal_u(runner):
    """Testing aapg_cclass_rv64imafdc_illegal_u.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_illegal_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_illegal_u.yaml tests/work/aapg_cclass_rv64imafdc_illegal_u/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_illegal_u','--output_dir=tests/work/aapg_cclass_rv64imafdc_illegal_u/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_illegal_u; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_recursion_branch(runner):
    """Testing aapg_cclass_rv64imafdc_recursion_branch.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_recursion_branch'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_recursion_branch.yaml tests/work/aapg_cclass_rv64imafdc_recursion_branch/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_recursion_branch','--output_dir=tests/work/aapg_cclass_rv64imafdc_recursion_branch/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_recursion_branch; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_bringup(runner):
    """Testing aapg_cclass_rv64imafdc_bringup.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_bringup'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_bringup.yaml tests/work/aapg_cclass_rv64imafdc_bringup/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_bringup','--output_dir=tests/work/aapg_cclass_rv64imafdc_bringup/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_bringup; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_exceptions(runner):
    """Testing aapg_iclass_rv64imafdc_exceptions.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_exceptions'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_exceptions.yaml tests/work/aapg_iclass_rv64imafdc_exceptions/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_exceptions','--output_dir=tests/work/aapg_iclass_rv64imafdc_exceptions/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_exceptions; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_branches1_s(runner):
    """Testing aapg_iclass_rv64imafdc_branches1_s.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_branches1_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_branches1_s.yaml tests/work/aapg_iclass_rv64imafdc_branches1_s/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_branches1_s','--output_dir=tests/work/aapg_iclass_rv64imafdc_branches1_s/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_branches1_s; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_s_recursion(runner):
    """Testing aapg_iclass_rv64imafdc_s_recursion.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_s_recursion'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_s_recursion.yaml tests/work/aapg_iclass_rv64imafdc_s_recursion/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_s_recursion','--output_dir=tests/work/aapg_iclass_rv64imafdc_s_recursion/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_s_recursion; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_illegal_u(runner):
    """Testing aapg_iclass_rv64imafdc_illegal_u.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_illegal_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_illegal_u.yaml tests/work/aapg_iclass_rv64imafdc_illegal_u/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_illegal_u','--output_dir=tests/work/aapg_iclass_rv64imafdc_illegal_u/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_illegal_u; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_hazards_s(runner):
    """Testing aapg_cclass_rv64imafdc_hazards_s.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_hazards_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_hazards_s.yaml tests/work/aapg_cclass_rv64imafdc_hazards_s/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_hazards_s','--output_dir=tests/work/aapg_cclass_rv64imafdc_hazards_s/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_hazards_s; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_user_u(runner):
    """Testing aapg_cclass_rv64imafdc_user_u.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_user_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_user_u.yaml tests/work/aapg_cclass_rv64imafdc_user_u/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_user_u','--output_dir=tests/work/aapg_cclass_rv64imafdc_user_u/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_user_u; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_exceptions_s(runner):
    """Testing aapg_cclass_rv64imafdc_exceptions_s.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_exceptions_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_exceptions_s.yaml tests/work/aapg_cclass_rv64imafdc_exceptions_s/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_exceptions_s','--output_dir=tests/work/aapg_cclass_rv64imafdc_exceptions_s/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_exceptions_s; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_test_all(runner):
    """Testing aapg_cclass_rv64imafdc_test_all.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_test_all'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_test_all.yaml tests/work/aapg_cclass_rv64imafdc_test_all/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_test_all','--output_dir=tests/work/aapg_cclass_rv64imafdc_test_all/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_test_all; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_test_all(runner):
    """Testing aapg_iclass_rv64imafdc_test_all.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_test_all'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_test_all.yaml tests/work/aapg_iclass_rv64imafdc_test_all/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_test_all','--output_dir=tests/work/aapg_iclass_rv64imafdc_test_all/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_test_all; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_recurse_low(runner):
    """Testing aapg_iclass_rv64imafdc_recurse_low.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_recurse_low'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_recurse_low.yaml tests/work/aapg_iclass_rv64imafdc_recurse_low/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_recurse_low','--output_dir=tests/work/aapg_iclass_rv64imafdc_recurse_low/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_recurse_low; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_branches1_u(runner):
    """Testing aapg_cclass_rv64imafdc_branches1_u.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_branches1_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_branches1_u.yaml tests/work/aapg_cclass_rv64imafdc_branches1_u/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_branches1_u','--output_dir=tests/work/aapg_cclass_rv64imafdc_branches1_u/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_branches1_u; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_exceptions(runner):
    """Testing aapg_cclass_rv64imafdc_exceptions.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_exceptions'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_exceptions.yaml tests/work/aapg_cclass_rv64imafdc_exceptions/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_exceptions','--output_dir=tests/work/aapg_cclass_rv64imafdc_exceptions/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_exceptions; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_illegal_s(runner):
    """Testing aapg_cclass_rv64imafdc_illegal_s.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_illegal_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_illegal_s.yaml tests/work/aapg_cclass_rv64imafdc_illegal_s/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_illegal_s','--output_dir=tests/work/aapg_cclass_rv64imafdc_illegal_s/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_illegal_s; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_recurse_med(runner):
    """Testing aapg_cclass_rv64imafdc_recurse_med.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_recurse_med'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_recurse_med.yaml tests/work/aapg_cclass_rv64imafdc_recurse_med/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_recurse_med','--output_dir=tests/work/aapg_cclass_rv64imafdc_recurse_med/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_recurse_med; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_user_u(runner):
    """Testing aapg_iclass_rv64imafdc_user_u.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_user_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_user_u.yaml tests/work/aapg_iclass_rv64imafdc_user_u/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_user_u','--output_dir=tests/work/aapg_iclass_rv64imafdc_user_u/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_user_u; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_bringup_u(runner):
    """Testing aapg_iclass_rv64imafdc_bringup_u.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_bringup_u'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_bringup_u.yaml tests/work/aapg_iclass_rv64imafdc_bringup_u/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_bringup_u','--output_dir=tests/work/aapg_iclass_rv64imafdc_bringup_u/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_bringup_u; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_illegal(runner):
    """Testing aapg_cclass_rv64imafdc_illegal.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_illegal'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_illegal.yaml tests/work/aapg_cclass_rv64imafdc_illegal/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_illegal','--output_dir=tests/work/aapg_cclass_rv64imafdc_illegal/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_illegal; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_cclass_rv64imafdc_recurse_low(runner):
    """Testing aapg_cclass_rv64imafdc_recurse_low.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_cclass_rv64imafdc_recurse_low'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_cclass_rv64imafdc_recurse_low.yaml tests/work/aapg_cclass_rv64imafdc_recurse_low/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_cclass_rv64imafdc_recurse_low','--output_dir=tests/work/aapg_cclass_rv64imafdc_recurse_low/asm'])
    try:
        os.system('cd tests/work/aapg_cclass_rv64imafdc_recurse_low; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_exceptions_s(runner):
    """Testing aapg_iclass_rv64imafdc_exceptions_s.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_exceptions_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_exceptions_s.yaml tests/work/aapg_iclass_rv64imafdc_exceptions_s/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_exceptions_s','--output_dir=tests/work/aapg_iclass_rv64imafdc_exceptions_s/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_exceptions_s; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_illegal_s(runner):
    """Testing aapg_iclass_rv64imafdc_illegal_s.yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_illegal_s'])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_illegal_s.yaml tests/work/aapg_iclass_rv64imafdc_illegal_s/config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_illegal_s','--output_dir=tests/work/aapg_iclass_rv64imafdc_illegal_s/asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_illegal_s; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0

@pytest.mark.timeout(300)
def test_aapg_iclass_rv64imafdc_data_trashing (runner):
    """Testing aapg_iclass_rv64imafdc_data_trashing .yaml config file in parallel mode"""
    make = 0
    runner.invoke(cli, ['setup','--setup_dir=tests/work/aapg_iclass_rv64imafdc_data_trashing '])
    os.system('cp tests/ci_cd_templates/core_configs/aapg_iclass_rv64imafdc_data_trashing .yaml tests/work/aapg_iclass_rv64imafdc_data_trashing /config.yaml')
    result = runner.invoke(cli, ['gen','--setup_dir=tests/work/aapg_iclass_rv64imafdc_data_trashing ','--output_dir=tests/work/aapg_iclass_rv64imafdc_data_trashing /asm'])
    try:
        os.system('cd tests/work/aapg_iclass_rv64imafdc_data_trashing ; make')
    except:
        make = 1
    assert result.exit_code == 0 and make == 0







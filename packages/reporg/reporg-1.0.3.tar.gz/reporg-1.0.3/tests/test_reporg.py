from click.testing import CliRunner
from reporg.main import cli
import pytest 
import os

@pytest.fixture
def runner():
    return CliRunner()


def test_version(runner):
    '''Testing version option'''
    result = runner.invoke(cli, ['--version'])
    assert result.exit_code == 0

def test_patch(runner):
    '''Testing version option'''
    result = runner.invoke(cli, ['--dir', os.getcwd(), '--list', '{0}/repo_patch.yaml'.format(os.getcwd())])
    assert result.exit_code == 0



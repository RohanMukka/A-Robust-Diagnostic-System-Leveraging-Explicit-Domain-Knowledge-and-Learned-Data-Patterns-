import os
import sys
import pathlib
from subprocess import check_output
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

CLI_PATH = os.path.join(os.path.dirname(__file__), '..', 'diagnosis', 'diagnose.py')


def test_cli_run():
    output = check_output([sys.executable, CLI_PATH, '--symptoms', 'Fever,Cough,ShortnessOfBreath'])
    assert b'diagnosis' in output.lower()

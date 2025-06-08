import os
import sys
import pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from ml.train_model import train, DATA_FILE


def test_training_accuracy():
    if not os.path.exists(DATA_FILE):
        import pytest
        pytest.skip('Dataset not available')
    acc = train()
    assert acc > 0.7

import argparse
import os
from pathlib import Path

import pytest

from appjsonify import main
from appjsonify.utils.error import NotAPDFError, PipelineOrderError


@pytest.fixture()
def txt(tmpdir) -> str:
    # create a .txt sample
    tmp_file = Path(tmpdir.join('test.txt'))
    tmp_file.write_text("This is a test.")
    
    # pass to test_func
    yield str(tmp_file)

    # post-processing
    os.remove(str(tmp_file))


@pytest.fixture()
def output(tmpdir) -> str:
    # pass to test_func
    return str(tmpdir)


@pytest.fixture()
def pdf(tmpdir) -> str:
    # create a .txt sample
    tmp_file = Path(tmpdir.join('test.pdf'))
    tmp_file.write_text("This is a test.")
    
    # pass to test_func
    yield str(tmp_file)

    # post-processing
    os.remove(str(tmp_file))


def test_filenotfounderror():
    # FileNotFoundError
    args_dict: dict = {
        "input_dir_or_file_path": "/path/to/test",
    }
    args = argparse.Namespace(**args_dict)
    with pytest.raises(FileNotFoundError):
        main(args)


def test_notapdferror(txt):
    # NotAPDFError
    args_dict: dict = {
        "input_dir_or_file_path": txt,
    }
    args = argparse.Namespace(**args_dict)
    with pytest.raises(NotAPDFError):
        main(args)


def test_notimplementederror(pdf, output):
    # NotImplementedError
    args_dict: dict = {
        "input_dir_or_file_path": pdf,
        "output_dir": output,
        "pipeline": None,
        "paper_type": None
    }
    args = argparse.Namespace(**args_dict)
    with pytest.raises(NotImplementedError) as exc_info:
        main(args)
    assert str(exc_info.value) == "Please specify `--pipeline` when `--paper_type` is not set!"


def test_pipelineordererror_1(pdf, output):
    # PipelineOrderError
    args_dict: dict = {
        "input_dir_or_file_path": pdf,
        "output_dir": output,
        "pipeline": ["detect_sections"],
        "paper_type": None
    }
    args = argparse.Namespace(**args_dict)
    with pytest.raises(PipelineOrderError):
        main(args)


def test_pipelineordererror_2(pdf, output):
    # PipelineOrderError
    args_dict: dict = {
        "input_dir_or_file_path": pdf,
        "output_dir": output,
        "pipeline": ["no_such_a_module"],
        "paper_type": None
    }
    args = argparse.Namespace(**args_dict)
    with pytest.raises(PipelineOrderError):
        main(args)
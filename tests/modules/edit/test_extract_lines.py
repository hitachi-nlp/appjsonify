import argparse

import pytest

from appjsonify.modules.doc import Document, Page, Token
from appjsonify.modules.runner import BaseRunner


@pytest.fixture()
def documents():
    # create tokens
    token_1 = Token("1", (0, 100, 10, 110), 10.0, "test")
    token_2 = Token("2", (10, 100, 20, 110), 10.0, "test")
    token_3 = Token("3", (20, 100, 30, 110), 10.0, "test")
    token_4 = Token("4", (30, 100, 40, 110), 10.0, "test")
    token_5 = Token("5", (40, 100, 50, 110), 10.0, "test")
    
    token_6 = Token("6", (0, 120, 10, 130), 10.0, "test")
    token_7 = Token("7", (10, 120, 20, 130), 10.0, "test")
    token_8 = Token("8", (20, 120, 30, 130), 10.0, "test")
    
    token_9 = Token("9", (0, 140, 10, 150), 10.0, "test")
    
    token_10 = Token("10", (0, 150, 10, 160), 10.0, "test")
    
    token_11 = Token("11", (0, 160, 10, 170), 10.0, "test")
    token_12 = Token("12", (10, 160, 20, 170), 10.0, "test")
    
    # compose a page
    page = Page(
        None, None, [
            token_1, token_2, token_3, token_4, token_5,
            token_6, token_7, token_8, token_9, token_10,
            token_11, token_12
        ]
    )
    
    # create a list of `Document`` instances
    docs = [Document("", [page])]
    return docs
    
    
def test_extract_lines(documents):
    # set necessary args
    args_dict: dict = {
        "y_tolerance": 5
    }
    args = argparse.Namespace(**args_dict)
    
    # get a module instance
    module_cls = BaseRunner.by_name("extract_lines")
    
    # execute a process
    docs = module_cls().execute(documents=documents, **vars(args))
    
    # compare
    ret_lines = [line.line for line in docs[0].pages[0].lines]
    gold_lines = ["1 2 3 4 5", "6 7 8", "9", "10", "11 12"]
    assert ret_lines == gold_lines

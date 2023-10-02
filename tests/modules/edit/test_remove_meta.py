import argparse

import pytest

from appjsonify.modules.doc import Document, Page, Token
from appjsonify.modules.runner import BaseRunner


@pytest.fixture()
def documents():
    # create test tokens
    header_token = Token(
        "header",
        pos=(100, 10, 200, 20),
        font_size=10.0,
        font_name="test"
    )
    footer_token = Token(
        "footer",
        pos=(100, 980, 200, 990),
        font_size=10.0,
        font_name="test"
    )
    left_token = Token(
        "left",
        pos=(10, 100, 20, 200),
        font_size=10.0,
        font_name="test"
    )
    right_token = Token(
        "right",
        pos=(980, 100, 990, 200),
        font_size=10.0,
        font_name="test"
    )
    
    # compose a page
    page = Page(
        None, None, [
            header_token, footer_token, left_token, right_token
        ]
    )
    
    # create a list of `Document`` instances
    docs = [Document("", [page])]
    return docs


@pytest.fixture()
def documents_without_header():
    # create test tokens
    footer_token = Token(
        "footer",
        pos=(100, 980, 200, 990),
        font_size=10.0,
        font_name="test"
    )
    left_token = Token(
        "left",
        pos=(10, 100, 20, 200),
        font_size=10.0,
        font_name="test"
    )
    right_token = Token(
        "right",
        pos=(980, 100, 990, 200),
        font_size=10.0,
        font_name="test"
    )
    
    # compose a page
    page = Page(
        None, None, [
            footer_token, left_token, right_token
        ]
    )
    
    # create a list of `Document`` instances
    docs = [Document("", [page])]
    return docs
    
def test_header_removal(documents, documents_without_header):
    # set necessary args
    args_dict: dict = {
        "header_offset": 20,
        "footer_offset": 0,
        "left_side_offset": 0,
        "right_side_offset": 0   
    }
    args = argparse.Namespace(**args_dict)
    
    # get a module instance
    module_cls = BaseRunner.by_name("remove_meta")
    
    # execute a process
    docs = module_cls().execute(documents=documents, **vars(args))
    
    # compare
    ret_tokens = [token.token for token in docs[0].pages[0].tokens]
    gold_tokens = [token.token for token in documents_without_header[0].pages[0].tokens]
    assert ret_tokens == gold_tokens


@pytest.fixture()
def documents_without_footer():
    # create test tokens
    header_token = Token(
        "header",
        pos=(100, 10, 200, 20),
        font_size=10.0,
        font_name="test"
    )
    left_token = Token(
        "left",
        pos=(10, 100, 20, 200),
        font_size=10.0,
        font_name="test"
    )
    right_token = Token(
        "right",
        pos=(980, 100, 990, 200),
        font_size=10.0,
        font_name="test"
    )
    
    # compose a page
    page = Page(
        None, None, [
            header_token, left_token, right_token
        ]
    )
    
    # create a list of `Document`` instances
    docs = [Document("", [page])]
    return docs


def test_footer_removal(documents, documents_without_footer):
    # set necessary args
    args_dict: dict = {
        "header_offset": 0,
        "footer_offset": 20,
        "left_side_offset": 0,
        "right_side_offset": 0   
    }
    args = argparse.Namespace(**args_dict)
    
    # get a module instance
    module_cls = BaseRunner.by_name("remove_meta")
    
    # execute a process
    docs = module_cls().execute(documents=documents, **vars(args))
    
    # compare
    ret_tokens = [token.token for token in docs[0].pages[0].tokens]
    gold_tokens = [token.token for token in documents_without_footer[0].pages[0].tokens]
    assert ret_tokens == gold_tokens


@pytest.fixture()
def documents_without_left():
    # create test tokens
    header_token = Token(
        "header",
        pos=(100, 10, 200, 20),
        font_size=10.0,
        font_name="test"
    )
    footer_token = Token(
        "footer",
        pos=(100, 980, 200, 990),
        font_size=10.0,
        font_name="test"
    )
    right_token = Token(
        "right",
        pos=(980, 100, 990, 200),
        font_size=10.0,
        font_name="test"
    )
    
    # compose a page
    page = Page(
        None, None, [
            header_token, footer_token, right_token
        ]
    )
    
    # create a list of `Document`` instances
    docs = [Document("", [page])]
    return docs

def test_left_side_margin_removal(documents, documents_without_left):
    # set necessary args
    args_dict: dict = {
        "header_offset": 0,
        "footer_offset": 0,
        "left_side_offset": 20,
        "right_side_offset": 0   
    }
    args = argparse.Namespace(**args_dict)
    
    # get a module instance
    module_cls = BaseRunner.by_name("remove_meta")
    
    # execute a process
    docs = module_cls().execute(documents=documents, **vars(args))
    
    # compare
    ret_tokens = [token.token for token in docs[0].pages[0].tokens]
    gold_tokens = [token.token for token in documents_without_left[0].pages[0].tokens]
    assert ret_tokens == gold_tokens


@pytest.fixture()
def documents_without_right():
    # create test tokens
    header_token = Token(
        "header",
        pos=(100, 10, 200, 20),
        font_size=10.0,
        font_name="test"
    )
    footer_token = Token(
        "footer",
        pos=(100, 980, 200, 990),
        font_size=10.0,
        font_name="test"
    )
    left_token = Token(
        "left",
        pos=(10, 100, 20, 200),
        font_size=10.0,
        font_name="test"
    )
    
    # compose a page
    page = Page(
        None, None, [
            header_token, footer_token, left_token
        ]
    )
    
    # create a list of `Document`` instances
    docs = [Document("", [page])]
    return docs

def test_right_side_margin_removal(documents, documents_without_right):
    # set necessary args
    args_dict: dict = {
        "header_offset": 0,
        "footer_offset": 0,
        "left_side_offset": 0,
        "right_side_offset": 20   
    }
    args = argparse.Namespace(**args_dict)
    
    # get a module instance
    module_cls = BaseRunner.by_name("remove_meta")
    
    # execute a process
    docs = module_cls().execute(documents=documents, **vars(args))
    
    # compare
    ret_tokens = [token.token for token in docs[0].pages[0].tokens]
    gold_tokens = [token.token for token in documents_without_right[0].pages[0].tokens]
    assert ret_tokens == gold_tokens

import argparse

import pytest

from appjsonify.modules.doc import Document, Page, Line, Token
from appjsonify.modules.runner import BaseRunner


@pytest.fixture()
def documents():
    # create lines
    line_to_be_removed = Line(
        "Footnote", (100, 950, 200, 960), 10.0, "test", []
    )
    line_not_to_be_removed = Line(
        "Test", (0, 100, 10, 110), 10.0, "test", []
    )
    
    # compose a page
    page = Page(
        None, [line_to_be_removed, line_not_to_be_removed], None,
        {
            "lines": [
                Token(
                    "", (100, 900, 350, 900), 1.0, "test",
                )
            ]
        }
    )
    
    # create a list of `Document`` instances
    docs = [Document("", [page], meta={"most_common_font_size": 12.0})]
    return docs
    
    
def test_extract_footnotes_1(documents):
    # set necessary args
    args_dict: dict = {
        "footnote_offset": 150,
        "use_horizontal_lines": True,
        "caption_font_size": None
    }
    args = argparse.Namespace(**args_dict)
    
    # get a module instance
    module_cls = BaseRunner.by_name("extract_footnotes")
    
    # execute a process
    docs = module_cls().execute(documents=documents, **vars(args))
    
    # compare
    ret_lines = [line.line for line in docs[0].pages[0].lines]
    gold_lines = ["Test"]
    assert ret_lines == gold_lines


def test_extract_footnotes_2(documents):
    # set necessary args
    args_dict: dict = {
        "footnote_offset": 10,
        "use_horizontal_lines": False,
        "caption_font_size": None
    }
    args = argparse.Namespace(**args_dict)
    
    # get a module instance
    module_cls = BaseRunner.by_name("extract_footnotes")
    
    # execute a process
    docs = module_cls().execute(documents=documents, **vars(args))
    
    # compare
    ret_lines = [line.line for line in docs[0].pages[0].lines]
    gold_lines = ["Footnote", "Test"]
    assert ret_lines == gold_lines


@pytest.fixture()
def documents_3():
    # create lines
    line_to_be_removed = Line(
        "Footnote", (100, 950, 200, 960), 10.0, "test", []
    )
    line_not_to_be_removed = Line(
        "Test", (0, 100, 10, 110), 10.0, "test", []
    )
    
    # compose a page
    page = Page(
        None, [line_to_be_removed, line_not_to_be_removed], None,
        {
            "lines": [
                Token(
                    "", (100, 900, 350, 910), 1.0, "test",
                )
            ]
        }
    )
    
    # create a list of `Document`` instances
    docs = [Document("", [page], meta={"most_common_font_size": 12.0})]
    return docs

def test_extract_footnotes_3(documents_3):
    # set necessary args
    args_dict: dict = {
        "footnote_offset": 150,
        "use_horizontal_lines": True,
        "caption_font_size": None
    }
    args = argparse.Namespace(**args_dict)
    
    # get a module instance
    module_cls = BaseRunner.by_name("extract_footnotes")
    
    # execute a process
    docs = module_cls().execute(documents=documents_3, **vars(args))
    
    # compare
    ret_lines = [line.line for line in docs[0].pages[0].lines]
    gold_lines = ["Footnote", "Test"]
    assert ret_lines == gold_lines


@pytest.fixture()
def documents_4():
    # create lines
    line_to_be_removed = Line(
        "Footnote", (100, 950, 200, 960), 9.0, "test", []
    )
    line_not_to_be_removed = Line(
        "Test", (0, 100, 10, 110), 10.0, "test", []
    )
    
    # compose a page
    page = Page(
        None, [line_to_be_removed, line_not_to_be_removed], None,
        {
            "lines": [
                Token(
                    "", (100, 900, 350, 910), 1.0, "test",
                )
            ]
        }
    )
    
    # create a list of `Document`` instances
    docs = [Document("", [page], meta={"most_common_font_size": 12.0})]
    return docs

def test_extract_footnotes_4(documents_4):
    # set necessary args
    args_dict: dict = {
        "footnote_offset": 150,
        "use_horizontal_lines": False,
        "caption_font_size": 9.0
    }
    args = argparse.Namespace(**args_dict)
    
    # get a module instance
    module_cls = BaseRunner.by_name("extract_footnotes")
    
    # execute a process
    docs = module_cls().execute(documents=documents_4, **vars(args))
    
    # compare
    ret_lines = [line.line for line in docs[0].pages[0].lines]
    gold_lines = ["Test"]
    assert ret_lines == gold_lines


@pytest.fixture()
def documents_5():
    # create lines
    line_to_be_removed = Line(
        "Footnote", (100, 950, 200, 960), 9.0, "test", []
    )
    line_not_to_be_removed = Line(
        "Test", (0, 100, 10, 110), 10.0, "test", []
    )
    
    # compose a page
    page = Page(
        None, [line_to_be_removed, line_not_to_be_removed], None,
        {
            "lines": [
                Token(
                    "", (100, 900, 350, 900), 1.0, "test",
                )
            ]
        }
    )
    
    # create a list of `Document`` instances
    docs = [Document("", [page], meta={"most_common_font_size": 12.0})]
    return docs

def test_extract_footnotes_5(documents_5):
    # set necessary args
    args_dict: dict = {
        "footnote_offset": 150,
        "use_horizontal_lines": True,
        "caption_font_size": 9.0
    }
    args = argparse.Namespace(**args_dict)
    
    # get a module instance
    module_cls = BaseRunner.by_name("extract_footnotes")
    
    # execute a process
    docs = module_cls().execute(documents=documents_5, **vars(args))
    
    # compare
    ret_lines = [line.line for line in docs[0].pages[0].lines]
    gold_lines = ["Test"]
    assert ret_lines == gold_lines
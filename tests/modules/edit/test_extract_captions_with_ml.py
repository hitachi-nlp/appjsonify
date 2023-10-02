import argparse

import pytest

from appjsonify.modules.doc import Document, Page, Line, Token
from appjsonify.modules.runner import BaseRunner


@pytest.fixture()
def documents_no_caption():
    # create lines
    line = Line(
        "test", (0, 100, 10, 110), 10.0, "test", 
        [Token("test", (0, 100, 10, 110), 10.0, "test")]
    )
    
    # compose a page
    page = Page(
        None, [line], None,
        {"captions": []}
    )
    
    # create a list of `Document`` instances
    docs = [Document("", [page])]
    return docs
    
def test_extract_captions_with_ml_1(documents_no_caption):
    # get a module instance
    module_cls = BaseRunner.by_name("extract_captions_with_ml")
    
    # execute a process
    docs = module_cls().execute(documents=documents_no_caption)
    
    # compare
    ret_lines = [line.line for line in docs[0].pages[0].lines]
    gold_lines = ["test"]
    assert ret_lines == gold_lines


@pytest.fixture()
def documents_only_captions():
    # create lines
    line = Line(
        "test", (0, 100, 10, 110), 10.0, "test", 
        [Token("test", (0, 100, 10, 110), 10.0, "test")]
    )
    
    # compose a page
    page = Page(
        None, [line], None,
        {
            "captions": [
                Token(
                    "", (0, 0, 0, 0), 10.0, "test", 
                    {
                        "tokens": [
                            Token("Table", (0, 0, 0, 0), 10.0, "test"),
                            Token("1:", (0, 0, 0, 0), 10.0, "test"),
                            Token("Test", (0, 0, 0, 0), 10.0, "test")
                        ]
                    }
                ),
                Token(
                    "", (1, 1, 1, 1), 10.0, "test", 
                    {
                        "tokens": [
                            Token("Figure", (1, 1, 1, 1), 10.0, "test"),
                            Token("1:", (1, 1, 1, 1), 10.0, "test"),
                            Token("Test",(1, 1, 1, 1), 10.0, "test")
                        ]
                    }
                ),
                Token(
                    "", (1, 1, 1, 1), 10.0, "test", 
                    {
                        "tokens": [
                            Token("Test", (1, 1, 1, 1), 10.0, "test"),
                            Token("1:", (1, 1, 1, 1), 10.0, "test"),
                            Token("Test",(1, 1, 1, 1), 10.0, "test")
                        ]
                    }
                ),
            ],
        }
    )
    
    # create a list of `Document`` instances
    docs = [Document("", [page])]
    return docs
    
def test_extract_captions_with_ml_2(documents_only_captions):
    # get a module instance
    module_cls = BaseRunner.by_name("extract_captions_with_ml")
    
    # execute a process
    docs = module_cls().execute(documents=documents_only_captions)
    
    # compare
    ret_lines = [line.line for line in docs[0].pages[0].lines]
    gold_lines = ["test"]
    assert ret_lines == gold_lines


@pytest.fixture()
def documents_with_caption_and_table():
    # create lines
    line_1 = Line("Table 1: Test", (100, 350, 350, 360), 10.0, "test", [])
    line_2 = Line("Test", (100, 360, 350, 370), 10.0, "test", [])
    line_3 = Line("Table 2: Test", (600, 350, 850, 360), 10.0, "test", [])
    
    # compose a page
    page = Page(
        None, [line_1, line_2, line_3], None,
        {
            "captions": [
                Token(
                    "", (100, 350, 350, 360), 10.0, "test", 
                    {
                        "tokens": [
                            Token("Table", (0, 0, 0, 0), 10.0, "test"),
                            Token("1:", (0, 0, 0, 0), 10.0, "test"),
                            Token("Test", (0, 0, 0, 0), 10.0, "test")
                        ]
                    }
                ),
                Token(
                    "", (600, 350, 850, 360), 10.0, "test", 
                    {
                        "tokens": [
                            Token("Table", (0, 0, 0, 0), 10.0, "test"),
                            Token("2:", (0, 0, 0, 0), 10.0, "test"),
                            Token("Test", (0, 0, 0, 0), 10.0, "test")
                        ]
                    }
                ),
            ],
            "tables": [
                Token(
                    "", (100, 100, 350, 300), 10.0, "test",
                ),
                Token(
                    "", (600, 100, 850, 300), 10.0, "test",
                )
            ]
        }
    )
    
    # create a list of `Document`` instances
    docs = [Document("", [page])]
    return docs
    
def test_extract_captions_with_ml_3(documents_with_caption_and_table):
    # get a module instance
    module_cls = BaseRunner.by_name("extract_captions_with_ml")
    
    # execute a process
    docs = module_cls().execute(documents=documents_with_caption_and_table)
    
    # compare
    ret_lines = [line.line for line in docs[0].pages[0].lines]
    gold_lines = ["Test"]
    assert ret_lines == gold_lines


@pytest.fixture()
def documents_with_caption_and_figure():
    # create lines
    line_1 = Line("Figure 1: Test", (100, 350, 350, 360), 10.0, "test", [])
    line_2 = Line("Test", (100, 360, 350, 370), 10.0, "test", [])
    line_3 = Line("Figure 2: Test", (600, 350, 850, 360), 10.0, "test", [])

    # compose a page
    page = Page(
        None, [line_1, line_2, line_3], None,
        {
            "captions": [
                Token(
                    "", (100, 350, 350, 360), 10.0, "test", 
                    {
                        "tokens": [
                            Token("Figure", (0, 0, 0, 0), 10.0, "test"),
                            Token("1:", (0, 0, 0, 0), 10.0, "test"),
                            Token("Test", (0, 0, 0, 0), 10.0, "test")
                        ]
                    }
                ),
                Token(
                    "", (600, 350, 850, 360), 10.0, "test", 
                    {
                        "tokens": [
                            Token("Figure", (0, 0, 0, 0), 10.0, "test"),
                            Token("2:", (0, 0, 0, 0), 10.0, "test"),
                            Token("Test", (0, 0, 0, 0), 10.0, "test")
                        ]
                    }
                ),
                Token(
                    "", (600, 900, 850, 910), 10.0, "test", 
                    {
                        "tokens": [
                            Token("Figure", (0, 0, 0, 0), 10.0, "test"),
                            Token("3:", (0, 0, 0, 0), 10.0, "test"),
                            Token("Test", (0, 0, 0, 0), 10.0, "test")
                        ]
                    }
                ),
            ],
            "figures": [
                Token(
                    "", (100, 100, 350, 300), 10.0, "test",
                ),
                Token(
                    "", (600, 100, 850, 300), 10.0, "test",
                )
            ]
        }
    )
    
    # create a list of `Document`` instances
    docs = [Document("", [page])]
    return docs
    
def test_extract_captions_with_ml_4(documents_with_caption_and_figure):
    # get a module instance
    module_cls = BaseRunner.by_name("extract_captions_with_ml")
    
    # execute a process
    docs = module_cls().execute(documents=documents_with_caption_and_figure)
    
    # compare
    ret_lines = [line.line for line in docs[0].pages[0].lines]
    gold_lines = ["Test"]
    assert ret_lines == gold_lines

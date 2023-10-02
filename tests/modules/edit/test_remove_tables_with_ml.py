import argparse

import pytest

from appjsonify.modules.doc import Document, Page, Line, Token
from appjsonify.modules.runner import BaseRunner


@pytest.fixture()
def documents():
    # create lines
    line_to_be_removed = Line(
        "Removed", (100, 100, 200, 200), 10.0, "test", []
    )
    line_not_to_be_removed = Line(
        "Test", (0, 100, 10, 110), 10.0, "test", []
    )
    
    # compose a page
    page = Page(
        None, [line_to_be_removed, line_not_to_be_removed], None,
        {
            "tables": [
                Token(
                    "", (100, 100, 350, 300), 10.0, "test",
                )
            ]
        }
    )
    
    # create a list of `Document`` instances
    docs = [Document("", [page])]
    return docs
    
    
def test_remove_tables_with_ml(documents):
    # set necessary args
    args_dict: dict = {
        "object_bbox_offset": 25
    }
    args = argparse.Namespace(**args_dict)
    
    # get a module instance
    module_cls = BaseRunner.by_name("remove_tables_with_ml")
    
    # execute a process
    docs = module_cls().execute(documents=documents, **vars(args))
    
    # compare
    ret_lines = [line.line for line in docs[0].pages[0].lines]
    gold_lines = ["Test"]
    assert ret_lines == gold_lines

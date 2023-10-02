import pytest

from appjsonify.modules.doc import Document, Page, Token
from appjsonify.modules.runner import BaseRunner


@pytest.fixture()
def documents():
    # create test tokens
    ng_token = Token(
        "(cid:100)",
        pos=(100, 100, 110, 200),
        font_size=10.0,
        font_name="test"
    )
    ok_token = Token(
        "OK",
        pos=(120, 100, 130, 200),
        font_size=10.0,
        font_name="test"
    )
    
    # compose a page
    page = Page(
        None, None, [
            ng_token, ok_token
        ]
    )
    
    # create a list of `Document`` instances
    docs = [Document("", [page])]
    return docs


def test_remove_illegal_tokens(documents):
    # get a module instance
    module_cls = BaseRunner.by_name("remove_illegal_tokens")
    
    # execute a process
    docs = module_cls().execute(documents=documents)
    
    # compare
    ret_tokens = [token.token for token in docs[0].pages[0].tokens]
    gold_tokens = ["OK"]
    assert ret_tokens == gold_tokens

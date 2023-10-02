import copy
from tqdm.contrib import tenumerate
import re
import difflib

from ..doc import Document, Token
from ..runner import BaseRunner


@BaseRunner.register("remove_illegal_tokens")
class IllegalTokenRemover(BaseRunner):
    """Remove illegal token."""
    @staticmethod
    def _check_code(
        token: str
    ) -> str:
        # init
        copied_token = copy.copy(token)
        copied_token = copied_token.encode('utf-8').decode('utf-8')
        illegal_char_ptn = re.compile(r'\(cid:[0-9]+\)')
        
        # search illegal chars
        illegal_chars = []
        for symbol in difflib.ndiff(copied_token, repr(copied_token)[1:len(repr(copied_token))-1]):
            if symbol[0]==' ':
                continue
            if symbol[0]=='-':
                illegal_chars.append(symbol[-1])
        
        # replace illegal chars with blanks
        for illegal_char in illegal_chars:
            copied_token = copied_token.replace(illegal_char, '')
        copied_token = illegal_char_ptn.sub('', copied_token)
                
        return copied_token


    def execute(
        self, 
        documents: list[Document], 
        **kwargs: dict
    ) -> list[Document]:
        # init
        self.check_args(self.execute, locals())
        
        # avoid overwrite
        copied_documents: list[Document] = copy.deepcopy(documents)
        
        # extract lines
        for _, doc in tenumerate(copied_documents, total=len(copied_documents)):
            for page in doc.pages:
                ret_tokens: list[Token] = []
                for token in page.tokens:
                    ret_token = self._check_code(token.token)
                    if ret_token != '':
                        ret_tokens.append(
                            Token(
                                ret_token,
                                token.pos,
                                token.font_size,
                                token.font_name,
                                token.meta
                            )
                        )
                # update tokens
                page.tokens = ret_tokens
        
        return copied_documents

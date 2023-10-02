import copy
from tqdm.contrib import tenumerate

from ..runner import BaseRunner
from ..doc import Document, Page, Token


@BaseRunner.register("remove_meta")
class RuleBasedMetaRemover(BaseRunner):
    """Remove headers and footers."""
    def _process_by_page(
        self, 
        page: Page, 
        y0_header_offset: int = 80,
        y1_footer_offset: int = 80,
        x0_left_side_offset: int = 40,
        x1_right_side_offset: int = 40
    ):
        # init
        ret_tokens: list[Token] = []

        for token in page.tokens:
            # get pos
            x0, y0, x1, y1 = token.pos

            # check if a token is a header
            if y0 < y0_header_offset:
                continue
            
            # check if a token is a footer
            if abs(1000 - y1) < y1_footer_offset:
                continue

            # check if a token is in a margin area
            if x0 < x0_left_side_offset:
                continue
            if abs(1000 - x1) < x1_right_side_offset:
                continue

            ret_tokens.append(token)
        
        # update tokens
        page.tokens = ret_tokens
        return 


    def execute(
        self, 
        documents: list[Document], 
        header_offset: int = 80,
        footer_offset: int = 80,
        left_side_offset: int = 40,
        right_side_offset: int = 40,
        **kwargs: dict
    ) -> list[Document]:
        # init
        self.check_args(self.execute, locals())
        
        # avoid overwrite
        copied_documents: list[Document] = copy.deepcopy(documents)

        # remove meta information by page
        for _, doc in tenumerate(copied_documents, total=len(copied_documents)):
            for page in doc.pages:
                self._process_by_page(
                    page, header_offset, footer_offset,
                    left_side_offset, right_side_offset,
                )
        return copied_documents

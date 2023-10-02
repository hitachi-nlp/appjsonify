import re
import copy
import math

from tqdm.contrib import tenumerate

from ..common import check_token_overlap
from ..doc import Document, Line, Page
from ..runner import BaseRunner


@BaseRunner.register("extract_footnotes_with_ml")
class MLBasedFootnoteExtractor(BaseRunner):
    """Extract footnotes with ML-based bbox detectors' outputs."""
    def _process_by_page(
        self, 
        page: Page,
        threshold: float
    ) -> Page:
        # no footnotes
        if page.meta.get("footers") == [] and page.meta.get("footers") is not None:
            return page
        
        # extract footnotes
        footnotes: list[list[Line]] = []
        for footer in page.meta["footers"]:
            footnote: list[Line] = []
            for line in page.lines:
                if check_token_overlap(
                    footer.pos, line.pos, threshold=threshold
                ):
                    footnote.append(line) 
            footnotes.append(footnote)
        
        # remove footers from lines
        lines: list[Line] = []
        for line in page.lines:
            to_be_removed: bool = False
            if page.meta.get("footers") != []:
                for footer in page.meta.get("footers"):
                    if check_token_overlap(footer.pos, line.pos, threshold=threshold):
                        to_be_removed = True
                        break
            if to_be_removed is False:
                lines.append(line)
        
        return Page(
            page.paragraphs,
            lines,
            page.tokens,
            page.meta | {
                "line_footers": footnotes
            }
        )


    def execute(
        self, 
        documents: list[Document],
        footnote_overlap_threshold: float = 0.5,
        **kwargs: dict
    ) -> list[Document]:
        # init
        self.check_args(self.execute, locals())
        
        # avoid overwrite
        copied_documents = copy.deepcopy(documents)

        for _, doc in tenumerate(copied_documents, total=len(copied_documents)):
            pages: list[Page] = []
            for page in doc.pages:
                pages.append(
                    self._process_by_page(
                        page, 
                        footnote_overlap_threshold
                    )
                )
            doc.pages = pages
        return copied_documents

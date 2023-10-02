import copy
from collections import Counter

from tqdm.contrib import tenumerate

from ..common import get_most_common_font_size
from ..doc import Document, Line, Page
from ..runner import BaseRunner


@BaseRunner.register("extract_footnotes")
class RuleBasedFootnoteExtractor(BaseRunner):
    """Extract footnotes."""
    def _process_by_page(
        self, 
        page: Page, 
        footnote_offset: int = 150,
        most_common_font_size: float = None,
        use_horizontal_lines: bool = False,
        caption_font_size: float = None
    ):
        # filter horizontal lines
        if use_horizontal_lines:
            horizontal_lines: list[tuple] = []
            for line in page.meta.get("lines"):
                if line.pos[1] == line.pos[3]: 
                    # horizontal line
                    horizontal_lines.append(line.pos)

        ret_lines: list[Line] = []
        ret_footnotes: list[Line] = []
        for line in page.lines:
            # get line pos
            x0, y0, x1, y1 = line.pos

            # check if a line is a footnote
            skip_token = False
            if use_horizontal_lines:
                for hline in horizontal_lines:
                    if caption_font_size is None:
                        if (hline[1] <= y0 and hline[3] < y1 and abs(y0 - hline[1]) <= footnote_offset * 1.5) \
                            and (hline[0] <= x0 and hline[2] > x0) \
                            and (abs(1000 - y1) <= footnote_offset) \
                            and (line.font_size < most_common_font_size):
                                skip_token = True
                                break
                    else:
                        if (hline[1] <= y0 and hline[3] < y1 and abs(y0 - hline[1]) <= footnote_offset * 1.5) \
                            and (hline[0] <= x0 and hline[2] > x0) \
                            and (abs(1000 - y1) <= footnote_offset) \
                            and (line.font_size <= caption_font_size):
                                skip_token = True
                                break
            else:
                if caption_font_size is None:
                    if (abs(1000 - y1) <= footnote_offset) and (line.font_size < most_common_font_size):
                        skip_token = True
                else:
                    if (abs(1000 - y1) <= footnote_offset) and (line.font_size <= caption_font_size):
                        skip_token = True
            if skip_token:
                ret_footnotes.append(line)
            else:
                ret_lines.append(line)
        
        # update lines
        page.lines = ret_lines
        # add footnotes
        page.meta["footnotes"] = ret_footnotes
        return 


    def execute(
        self, 
        documents: list[Document], 
        footnote_offset: int = 150,
        use_horizontal_lines: bool = False,
        caption_font_size: float = None,
        **kwargs: dict
    ) -> list[Document]:
        # init
        self.check_args(self.execute, locals())
        
        # avoid overwrite
        copied_documents: list[Document] = copy.deepcopy(documents)

        # remove meta information by page
        for _, doc in tenumerate(copied_documents, total=len(copied_documents)):
            # get most_common_font_size
            if doc.meta.get("most_common_font_size") is None:
                most_common_font_size = get_most_common_font_size(doc)
                doc.meta["most_common_font_size"] = most_common_font_size
            else:
                most_common_font_size = doc.meta["most_common_font_size"]
            for page in doc.pages:
                self._process_by_page(
                    page, 
                    footnote_offset, 
                    most_common_font_size,
                    use_horizontal_lines,
                    caption_font_size
                )
        return copied_documents
    
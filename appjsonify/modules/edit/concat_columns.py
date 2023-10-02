import copy
import re
from collections import Counter

from tqdm.contrib import tenumerate

from ..doc import Document, Page, Paragraph
from ..runner import BaseRunner


@BaseRunner.register("concat_columns")
class RuleBasedColumnConcatenator(BaseRunner):
    """Concatenate paragraphs in different columns if they meet given conditions."""
    @staticmethod
    def gather_as_list(paragraph: Paragraph, target_name: str) -> list:
        return [getattr(token, target_name) for line in paragraph.lines for token in line.tokens]
    
    def _process_by_page(
        self, 
        page: Page, 
        column_offset: int = 300, 
        consider_font_size: bool = False
    ):
        # init
        paragraphs: list[Paragraph] = []
        prev_paragraph: Paragraph = None
        str_end_ptn_now = re.compile(r".*?[。．.、，,!！?？:：]$")
        str_end_ptn_prev = re.compile(r".*?[。．.!！?？]”?[0-9]*$")

        for paragraph in page.paragraphs:
            # get paragraph info
            x0, y0, x1, y1 = paragraph.pos

            if prev_paragraph is not None:
                if abs(x0 - prev_paragraph.pos[0]) >= column_offset:
                    # a column has changed
                    if consider_font_size:
                        font_cond = paragraph.font_size == prev_paragraph.font_size
                    else:
                        font_cond = True
                    if str_end_ptn_prev.search(prev_paragraph.paragraph) is None \
                        and str_end_ptn_now.search(paragraph.paragraph) is not None \
                        and font_cond:
                        #####
                        # concat
                        # -- Condition 1: prev_paragraph should not be the end of the paragraph.
                        # -- Condition 2: current paragraph should be the end of the paragraph.
                        #####
                        if prev_paragraph.paragraph.endswith("-"):
                            paragraph_content: str = prev_paragraph.paragraph[:-1]
                        else:
                            paragraph_content: str = prev_paragraph.paragraph + ' '
                        paragraphs.append(
                            Paragraph(
                                paragraph_content + paragraph.paragraph,
                                (-1, -1, -1, -1),
                                max(
                                    self.gather_as_list(paragraph, "font_size")
                                    + self.gather_as_list(prev_paragraph, "font_size")
                                ),
                                Counter(
                                    self.gather_as_list(paragraph, "font_name")
                                    + self.gather_as_list(prev_paragraph, "font_name")
                                ).most_common(1)[0][0],
                                prev_paragraph.lines + paragraph.lines,
                                paragraph.meta | {"pos": (prev_paragraph.pos, paragraph.pos)}
                            )
                        )
                        prev_paragraph = None
                        continue
                    else:
                        # no concat
                        paragraphs.append(prev_paragraph)
                else:
                    # no column change
                    paragraphs.append(prev_paragraph)

            # update prev
            prev_paragraph = paragraph
        
        else:
            # end of for loop
            if prev_paragraph is not None:
                paragraphs.append(prev_paragraph)    

        # update paragraphs
        page.paragraphs = paragraphs
        return 


    def execute(
        self, 
        documents: list[Document],
        column_offset: int = 300,
        consider_font_size: bool = False, 
        **kwargs: dict
    ) -> list[Document]:
        # init
        self.check_args(self.execute, locals())
        
        # avoid overwrite
        copied_documents = copy.deepcopy(documents)

        for _, doc in tenumerate(copied_documents, total=len(copied_documents)):
            for page in doc.pages:
                self._process_by_page(
                    page,
                    column_offset,
                    consider_font_size
                )
        return copied_documents

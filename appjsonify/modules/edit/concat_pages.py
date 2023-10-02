import copy
import re
from collections import Counter

from tqdm.contrib import tenumerate

from ..doc import Document, Paragraph
from ..runner import BaseRunner


@BaseRunner.register("concat_pages")
class RuleBasedPageConcatenator(BaseRunner):
    """Concatenate paragraphs in different pages if they meet given conditions."""
    @staticmethod
    def gather_as_list(paragraph: Paragraph, target_name: str) -> list:
        return [getattr(token, target_name) for line in paragraph.lines for token in line.tokens]
    
    def _process_by_doc(
        self, 
        doc: Document,
        consider_font_size: bool = False
    ) -> Document:
        # init
        paragraphs: list[Paragraph] = []
        tables: list[dict] = []
        figures: list[dict] = []
        footers: list[str] = []
        prev_paragraph: Paragraph = None
        str_end_ptn_now = re.compile(r".*?[。．.、，,!！?？:：]$")
        str_end_ptn_prev = re.compile(r".*?[。．.!！?？]”?[0-9]*$")

        for page in doc.pages:
            # get meta info
            if page.meta.get("line_footers") is not None:
                for footer in page.meta.get("line_footers"):
                    footer_str = ' '.join([line.line for line in footer])
                    footers.append(footer_str)
            if page.meta.get("footnotes") is not None:
                for footnote in page.meta.get("footnotes"):
                    footers.append(footnote.line)
            if page.meta.get("figures") is not None:
                for figure in page.meta.get("figures"):
                    figures.append(
                        {
                            "image_path": figure.meta["img_path"],
                            "caption": figure.meta.get("caption") if figure.meta.get("caption") is not None else ''
                        }
                    )
            if page.meta.get("tables") is not None:
                for table in page.meta.get("tables"):
                    tables.append(
                        {
                            "image_path": table.meta["img_path"],
                            "caption": table.meta.get("caption") if table.meta.get("caption") is not None else ''
                        }
                    )
            
            # if page has no paragraphs
            if page.paragraphs == [] or page.paragraphs is None:
                if prev_paragraph is not None:
                    paragraphs.append(prev_paragraph)
                    prev_paragraph = None
                continue
            
            if prev_paragraph is None:
                # init
                # add paragraphs except the last paragraph
                if len(page.paragraphs) > 1:
                    paragraphs.extend(page.paragraphs[:-1])
                # update prev
                prev_paragraph = page.paragraphs[-1]
                
            else:
                paragraph: Paragraph = page.paragraphs[0]
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
                    # add paragraphs except the last paragraph
                    if len(page.paragraphs) > 2:
                        paragraphs.extend(page.paragraphs[1:-1])
                    # update prev
                    if len(page.paragraphs) == 1:
                        prev_paragraph = None
                    else:
                        prev_paragraph = page.paragraphs[-1]
                else:
                    # no concat
                    paragraphs.append(prev_paragraph)
                    # add paragraphs except the last paragraph
                    if len(page.paragraphs) > 1:
                        paragraphs.extend(page.paragraphs[:-1])
                    # update prev
                    prev_paragraph = page.paragraphs[-1]
        
        else:
            # end of for loop
            if prev_paragraph is not None:
                paragraphs.append(prev_paragraph)    

        return Document(
            doc.input_path,
            doc.pages,
            paragraphs,
            doc.meta | {
                "tables": tables,
                "figures": figures,
                "footers": footers
            }
        )


    def execute(
        self, 
        documents: list[Document],
        consider_font_size: bool = False, 
        **kwargs: dict
    ) -> list[Document]:
        # init
        self.check_args(self.execute, locals())
        
        # avoid overwrite
        copied_documents = copy.deepcopy(documents)
        docs: list[Document] = []
        for _, doc in tenumerate(copied_documents, total=len(copied_documents)):
            docs.append(self._process_by_doc(doc, consider_font_size))   
        return docs

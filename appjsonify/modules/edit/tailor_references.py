import copy
import re
from collections import Counter

from tqdm.contrib import tenumerate

from ..doc import Document, Paragraph
from ..runner import BaseRunner


@BaseRunner.register("tailor_references")
class RuleBasedReferenceTailor(BaseRunner):
    """Concatenate reference paragraphs if they are in the same listing paragraph."""
    @staticmethod
    def gather_as_list(paragraph: Paragraph, target_name: str) -> list:
        return [getattr(token, target_name) for line in paragraph.lines for token in line.tokens]
    
    def _process_by_doc(
        self, 
        doc: Document,
        listing_offset: int
    ):
        # init
        is_in_references: bool = False
        str_start_ptn = re.compile(r"^.*?\s(1|2)([0-9]{3})\w?\.")
        str_end_ptn = re.compile(r".*?[.!?:;]”?[0-9]*$")

        for page in doc.pages:
            # init
            paragraphs: list[Paragraph] = []
            prev_paragraph: Paragraph = None
            
            for paragraph in page.paragraphs:
                if not is_in_references:
                    # skip up to references section
                    if paragraph.paragraph != "References" and paragraph.paragraph != "REFERENCES":
                        paragraphs.append(paragraph)
                        continue
                    elif paragraph.meta["style"] == "section":
                        is_in_references = True
                    else:
                        raise NotImplementedError("Style for ``References'' should be section!")
                elif paragraph.meta["style"] in ["section", "subsection"]:
                    # end of references section
                    is_in_references = False
                    if prev_paragraph is not None:
                        paragraphs.append(prev_paragraph)
                        prev_paragraph = None
                    paragraphs.append(paragraph)
                    continue
                
                if prev_paragraph is None:
                    # init
                    paragraph_min_x0, paragraph_max_x1 = paragraph.pos[0], paragraph.pos[2]
                    prev_paragraph = paragraph
                else:
                    # font size condition
                    font_cond = paragraph.font_size == prev_paragraph.font_size
                    # listing offset init
                    if listing_offset is None:
                        listing_offset = int(paragraph.font_size * 6)
                    # join prev and current paragraph
                    if prev_paragraph.paragraph.endswith("-"):
                        tmp_paragraph = prev_paragraph.paragraph[:-1] + paragraph.paragraph
                    else:
                        tmp_paragraph = prev_paragraph.paragraph + ' ' + paragraph.paragraph
                    if (0 <= (paragraph.pos[0] - prev_paragraph.pos[0]) <= listing_offset) \
                        and str_start_ptn.match(tmp_paragraph) is not None \
                        and str_end_ptn.search(paragraph.paragraph) is not None \
                        and font_cond:
                        #####
                        # concat
                        # -- Condition 1: prev_paragraph should be the beginning of a listing paragraph (listing).
                        # -- Condition 2: listing should start with author names then followed by a publication year.
                        # -- Condition 3: current paragraph should be the end of the complete paragraph.
                        # -- Condition 4: both font sizes must be the same.
                        #####
                        # TODO: Review the effectiveness of conditions 2 and 3.
                        if paragraph.pos[0] < paragraph_min_x0:
                            paragraph_min_x0 = paragraph.pos[0]
                        if paragraph.pos[2] > paragraph_max_x1:
                            paragraph_max_x1 = paragraph.pos[2]
                        paragraphs.append(
                            Paragraph(
                                tmp_paragraph,
                                (paragraph_min_x0, prev_paragraph.pos[1], paragraph_max_x1, paragraph.pos[3]),
                                max(
                                    self.gather_as_list(paragraph, "font_size")
                                    + self.gather_as_list(prev_paragraph, "font_size")
                                ),
                                Counter(
                                    self.gather_as_list(paragraph, "font_name")
                                    + self.gather_as_list(prev_paragraph, "font_name")
                                ).most_common(1)[0][0],
                                prev_paragraph.lines + paragraph.lines,
                                prev_paragraph.meta | paragraph.meta | {"pos": (prev_paragraph.pos, paragraph.pos)}
                            )
                        )
                        prev_paragraph = None
                        continue
                    else:
                        # no concat
                        paragraphs.append(prev_paragraph)
                    
                    # update paragraph
                    paragraph_min_x0, paragraph_max_x1 = paragraph.pos[0], paragraph.pos[2]
                    prev_paragraph = paragraph
                    
            # end of for loop
            if prev_paragraph is not None:
                paragraphs.append(prev_paragraph)    

            # update pages
            page.paragraphs = paragraphs
        return 


    def execute(
        self, 
        documents: list[Document],
        listing_offset: int,
        **kwargs: dict
    ) -> list[Document]:
        # init
        self.check_args(self.execute, locals())
        
        # avoid overwrite
        copied_documents = copy.deepcopy(documents)

        for _, doc in tenumerate(copied_documents, total=len(copied_documents)):
            self._process_by_doc(
                doc, listing_offset
            )
        return copied_documents

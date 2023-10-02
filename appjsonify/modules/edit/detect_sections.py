import copy
import re

from tqdm.contrib import tenumerate

from ..common import (get_font_specs_config, get_math_font_names,
                      get_most_common_font_name, get_most_common_font_size)
from ..doc import Document, Page, Paragraph
from ..runner import BaseRunner


@BaseRunner.register("detect_sections")
class RuleBasedSectionDetector(BaseRunner):
    """Detect sections."""
    @staticmethod
    def judge_style(
        paragraph: Paragraph,
        most_common_font_size: float,
        most_common_font_name: float,
        max_headline_len: int,
        headline_names: list[str]
    ) -> str:
        # init
        headline_ptn = re.compile(r'^([IVXLCDM\.]+|([A-Z0-9][0-9\.]*))\s([^\.]*)$')
        capilitzed_headline_ptn = re.compile(r'^[A-Z\s]+$')
        ret_headline = headline_ptn.search(paragraph.paragraph)
        if ret_headline is not None:
            paragraph_len = len(ret_headline.groups()[2].split(' '))
            if paragraph_len <= max_headline_len and paragraph_len > 0 \
                and paragraph.font_size >= most_common_font_size \
                and (paragraph.font_name.split('+')[1] != most_common_font_name \
                    or capilitzed_headline_ptn.match(ret_headline.groups()[2]) is not None):
                # Possibly a section
                style = "section"
            else:
                # Possibly a body
                style = "body"
        elif paragraph.paragraph in headline_names:
            style = "section"
        else:
            style = "body"
        return style
    
    
    def _process_by_page(
        self,
        page: Page,
        font_specs: dict[tuple[float, str], str],
        math_font_names: tuple[str],
        most_common_font_size: float,
        most_common_font_name: float,
        max_headline_len: int,
        headline_names: list[str]
    ) -> list[Paragraph]:
        paragraphs: list[Paragraph] = []
        if font_specs is None:
            for paragraph in page.paragraphs:
                style = self.judge_style(
                    paragraph, 
                    most_common_font_size,
                    most_common_font_name,
                    max_headline_len,
                    headline_names
                )
                # Need to update an instance as we edit meta information
                paragraphs.append(
                    Paragraph(
                        paragraph.paragraph,
                        paragraph.pos,
                        paragraph.font_size,
                        paragraph.font_name,
                        paragraph.lines,
                        paragraph.meta | {"style": style}
                    )
                )
                
        else:
            transposed_font_specs = {value: key for key, value in font_specs.items()}
            if transposed_font_specs.get("body") is not None:
                most_common_font_size = transposed_font_specs["body"][0]
                most_common_font_name = transposed_font_specs["body"][1]
            prev_style: str = None
            for paragraph in page.paragraphs:
                try:
                    font_spec = (paragraph.font_size, paragraph.font_name.split('+')[1])
                except IndexError:
                    font_spec = (paragraph.font_size, paragraph.font_name)
                # check if the font name is not a math one
                style: str = None
                if type(math_font_names) is not str:
                    for math_ptn_str in  math_font_names:
                        if re.match(math_ptn_str, font_spec[1]) is not None:
                            style = "equation"
                            break
                else:
                    if re.match(math_font_names, font_spec[1]) is not None:
                        style = "equation"
                # check if the font spec is in the dictionary
                if style is None:
                    if font_specs.get(font_spec) is None:
                        style = self.judge_style(
                            paragraph,
                            most_common_font_size,
                            most_common_font_name,
                            max_headline_len,
                            headline_names
                        )
                    else:
                        style = font_specs.get(font_spec)
                # tailor paragraphs based on `style`
                if prev_style == "title" and style == "title":
                    # merge
                    prev_paragraph: Paragraph = paragraphs.pop()
                    paragraphs.append(
                        Paragraph(
                            prev_paragraph.paragraph + ' ' + paragraph.paragraph,
                            (
                                prev_paragraph.pos[0] if prev_paragraph.pos[0] < paragraph.pos[0] else paragraph.pos[0],
                                prev_paragraph.pos[1] if prev_paragraph.pos[1] < paragraph.pos[1] else paragraph.pos[1],
                                paragraph.pos[2] if paragraph.pos[2] > prev_paragraph.pos[2] else prev_paragraph.pos[2],
                                paragraph.pos[3] if paragraph.pos[3] > prev_paragraph.pos[3] else prev_paragraph.pos[3]
                            ),
                            paragraph.font_size,
                            paragraph.font_name,
                            prev_paragraph.lines + paragraph.lines,
                            prev_paragraph.meta | paragraph.meta | {"style": style}
                        )
                    )
                else:
                    paragraphs.append(
                        Paragraph(
                            paragraph.paragraph,
                            paragraph.pos,
                            paragraph.font_size,
                            paragraph.font_name,
                            paragraph.lines,
                            paragraph.meta | {"style": style}
                        )
                    )
                # update prev
                prev_style = style

        # update paragraphs
        page.paragraphs = paragraphs
        return
    
    
    def execute(
        self, 
        documents: list[Document],
        paper_type: str,
        max_headline_len: int,
        headline_names: list[str],
        **kwargs: dict
    ) -> list[Document]:
        # init
        self.check_args(self.execute, locals())
        
        # avoid overwrite
        copied_documents = copy.deepcopy(documents)
        if paper_type is not None:
            font_specs = get_font_specs_config(paper_type)
            math_font_names = get_math_font_names(paper_type)
        else:
            font_specs = None
            math_font_names = None
        for _, doc in tenumerate(copied_documents, total=len(copied_documents)):
            # get most_common_font_size
            if doc.meta.get("most_common_font_size") is None:
                most_common_font_size = get_most_common_font_size(doc)
                doc.meta["most_common_font_size"] = most_common_font_size
            else:
                most_common_font_size = doc.meta["most_common_font_size"]
            # get most_common_font_name
            if doc.meta.get("most_common_font_name") is None:
                most_common_font_name = get_most_common_font_name(doc)
                doc.meta["most_common_font_name"] = most_common_font_name
            else:
                most_common_font_name = doc.meta["most_common_font_name"]
            for page in doc.pages:
                self._process_by_page(
                    page, 
                    font_specs, 
                    math_font_names,
                    most_common_font_size, 
                    most_common_font_name,
                    max_headline_len,
                    headline_names
                )
        return copied_documents

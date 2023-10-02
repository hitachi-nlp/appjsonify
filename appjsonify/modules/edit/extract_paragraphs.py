import copy
import re
from collections import Counter

import numpy as np
from tqdm.contrib import tenumerate

from ..doc import Document, Line, Page, Paragraph
from ..runner import BaseRunner


@BaseRunner.register("extract_paragraphs")
class RuleBasedParagraphExtractor(BaseRunner):
    """Concatenate line elements if they are in the same paragraph."""
    @staticmethod
    def gather_as_list(line: Line, target_name: str) -> list:
        return [getattr(token, target_name) for token in line.tokens]
    
    def _process_by_page(
        self, 
        page: Page,
        x_offset: int = 18, 
        y_offset: int = 4,
        consider_font_size: bool = False,
        indent_offset: int = None,
        listing_offset: int = None,
    ) -> list[Paragraph]:
        # init
        paragraphs: list[Paragraph] = []
        prev_line: Line = None
        is_listing: bool = False
        cache: dict = {
            "line": [], 
            "lines": [], 
            "x0": -1, 
            "y0": -1, 
            "x1": -1, 
            "y1": -1, 
            "font_size": [],
            "font_name": [], 
            "init": True
        }
        str_end_ptn = re.compile(r".*?[.!?:;]”?\s*[0-9]*$")
        # TODO: Add more listing styles if necessary
        # references
        str_start_ptn_1 = re.compile(r"^[\[\(]?\d+[0-9\.]*[\]\)]?")
        # appendix
        str_start_ptn_2 = re.compile(r"^[A-Z]{1}[0-9\.]*\s")
        # listing
        str_start_ptn_3 = re.compile(r"^\-|–|•")

        # process by line 
        for line in page.lines:
            if prev_line is None:
                # init
                font_size_list = self.gather_as_list(line, "font_size")
                font_name_list = self.gather_as_list(line, "font_name")
                cache: dict = {
                    "line": [line.line], 
                    "lines": [line], 
                    "x0": line.pos[0], 
                    "y0": line.pos[1], 
                    "x1": line.pos[2], 
                    "y1": line.pos[3], 
                    "font_size": font_size_list,
                    "font_name": font_name_list, 
                    "init": True
                }
                paragraph_min_x0, paragraph_max_x1 = line.pos[0], line.pos[2]
            else:
                # Font size condition
                if consider_font_size:
                    font_cond = line.font_size == prev_line.font_size
                else:
                    font_cond = True
                
                # Indent offset
                if indent_offset is None:
                    indent_offset = int(line.font_size * 2)
                
                # listing offset
                if listing_offset is None:
                    listing_offset = int(line.font_size * 6)
                
                if ((abs(line.pos[0] - prev_line.pos[0]) <= x_offset) \
                        or (0 <= (prev_line.pos[0] - line.pos[0]) <= indent_offset and is_listing is False) \
                        or ((str_start_ptn_1.search(prev_line.line) is not None or str_start_ptn_2.match(prev_line.line) is not None or str_start_ptn_3.search(prev_line.line) is not None) \
                            and 0 <= (line.pos[0] - prev_line.pos[0]) <= listing_offset)) \
                    and font_cond \
                    and abs(line.pos[2] - prev_line.pos[2]) <= x_offset \
                    and abs(line.pos[1] - prev_line.pos[3]) <= y_offset:
                    #####
                    # line in the same paragraph
                    # -- Condition 1: normal
                    # -- Condition 2: prev_line should be the beginning of a paragraph (indent).
                    # -- Condition 3: prev_line should be the beginning of a listing paragraph (listing).
                    #####
                    if (str_start_ptn_1.search(prev_line.line) is not None or str_start_ptn_2.match(prev_line.line) is not None or str_start_ptn_3.search(prev_line.line) is not None) \
                        and 0 <= (line.pos[0] - prev_line.pos[0]) <= listing_offset:
                        is_listing = True
                    
                    if cache["line"][-1].endswith("-"):
                        tmp_line = cache["line"].pop()[:-1] + line.line
                        cache["line"].append(tmp_line)
                    else:
                        cache["line"].append(line.line)
                    cache["lines"].append(line)
                    font_size_list = self.gather_as_list(line, "font_size")
                    cache["font_size"].extend(font_size_list)
                    font_name_list = self.gather_as_list(line, "font_name")
                    cache["font_name"].extend(font_name_list)
                    cache["init"] = False
                    if line.pos[0] < paragraph_min_x0:
                        paragraph_min_x0 = line.pos[0]
                    if line.pos[2] > paragraph_max_x1:
                        paragraph_max_x1 = line.pos[2]

                elif ((abs(line.pos[0] - prev_line.pos[0]) <= x_offset and str_end_ptn.search(line.line) is not None) \
                        or (0 <= (prev_line.pos[0] - line.pos[0]) <= indent_offset and str_end_ptn.search(line.line) is not None and is_listing is False) \
                        or (str_start_ptn_1.search(prev_line.line) is not None or str_start_ptn_2.match(prev_line.line) is not None or str_start_ptn_3.search(prev_line.line) is not None) \
                            and 0 <= (line.pos[0] - prev_line.pos[0]) <= listing_offset
                        or (abs(line.pos[0] - prev_line.pos[0]) <= x_offset and is_listing is True)) \
                    and font_cond \
                    and (prev_line.pos[2] - line.pos[2]) > x_offset \
                    and abs(line.pos[1] - prev_line.pos[3]) <= y_offset:
                    #####
                    # line in the same paragraph but should be the end of the paragraph block.
                    # Condition 1: normal
                    # Condition 2: prev_line should be the beginning of a paragraph (indent).
                    # Condition 3: prev_line should be the beginning of a listing paragraph (listing).
                    # Condition 4: current cached paragraph is a listing paragraph.
                    #####
                    if cache["line"][-1].endswith("-"):
                        tmp_line = cache["line"].pop()[:-1] + line.line
                        cache["line"].append(tmp_line)
                    else:
                        cache["line"].append(line.line)
                    cache["lines"].append(line)
                    font_size_list = self.gather_as_list(line, "font_size")
                    cache["font_size"].extend(font_size_list)
                    font_name_list = self.gather_as_list(line, "font_name")
                    cache["font_name"].extend(font_name_list)
                    cache["init"] = False
                    if line.pos[0] < paragraph_min_x0:
                        paragraph_min_x0 = line.pos[0]
                    if line.pos[2] > paragraph_max_x1:
                        paragraph_max_x1 = line.pos[2]
                    
                    # register
                    paragraphs.append(
                        Paragraph(
                            ' '.join(cache["line"]),
                            (paragraph_min_x0, cache["y0"], paragraph_max_x1, line.pos[3]),
                            max(cache["font_size"]),
                            Counter(cache["font_name"]).most_common(1)[0][0],
                            cache["lines"]
                        )
                    ) 
                    
                    # init
                    cache: dict = {
                        "line": [], 
                        "lines": [], 
                        "x0": -1, 
                        "y0": -1, 
                        "x1": -1, 
                        "y1": -1, 
                        "font_size": [],
                        "font_name": [],
                        "init": True
                    }
                    paragraph_min_x0, paragraph_max_x1 = 1000, 0
                    prev_line = None
                    is_listing = False
                    continue

                else:
                    #####
                    # line not in the same paragraph => register cache
                    #####
                    if cache["init"] is False:
                        # cache has several elements
                        cache["y1"] = prev_line.pos[3]
                        paragraphs.append(
                            Paragraph(
                                ' '.join(cache["line"]),
                                (paragraph_min_x0, cache["y0"], paragraph_max_x1, cache["y1"]),
                                max(cache["font_size"]),
                                Counter(cache["font_name"]).most_common(1)[0][0],
                                cache["lines"]
                            )
                        )
                    else:
                        # cache has only one element
                        if cache['line'] != []:
                            paragraphs.append(
                                Paragraph(
                                    cache["line"].pop(),
                                    (cache["x0"], cache["y0"], cache["x1"], cache["y1"]),
                                    max(cache["font_size"]),
                                    Counter(cache["font_name"]).most_common(1)[0][0],
                                    cache["lines"]
                                )
                            )
                    
                    # clear cache
                    font_size_list = self.gather_as_list(line, "font_size")
                    font_name_list = self.gather_as_list(line, "font_name")
                    cache: dict = {
                        "line": [line.line], 
                        "lines": [line], 
                        "x0": line.pos[0], 
                        "y0": line.pos[1], 
                        "x1": line.pos[2], 
                        "y1": line.pos[3], 
                        "font_size": font_size_list,
                        "font_name": font_name_list, 
                        "init": True
                    }
                    is_listing = False
                    paragraph_min_x0, paragraph_max_x1 = line.pos[0], line.pos[2]
                
            # update prev_line
            prev_line = line
            
        else:
            # end of for loop
            if cache["init"] is False:
                cache["y1"] = prev_line.pos[3]
                paragraphs.append(
                    Paragraph(
                        ' '.join(cache["line"]),
                        (paragraph_min_x0, cache["y0"], paragraph_max_x1, cache["y1"]),
                        max(cache["font_size"]),
                        Counter(cache["font_name"]).most_common(1)[0][0],
                        cache["lines"]
                    )
                )
            else:
                if cache['line'] != []:
                    paragraphs.append(
                        Paragraph(
                            cache["line"].pop(),
                            (cache["x0"], cache["y0"], cache["x1"], cache["y1"]),
                            max(cache["font_size"]),
                            Counter(cache["font_name"]).most_common(1)[0][0],
                            cache["lines"]
                        )
                    )
                    
        return paragraphs


    def execute(
        self, 
        documents: list[Document], 
        x_offset: int = 18,
        y_offset: int = 4,
        consider_font_size: bool = False,
        indent_offset: int = None,
        listing_offset: int = None,
        **kwargs: dict
    ) -> list[Document]:
        # init
        self.check_args(self.execute, locals())
        
        # avoid overwrite
        copied_documents: list[Document] = copy.deepcopy(documents)

        for _, doc in tenumerate(copied_documents, total=len(copied_documents)):
            for page in doc.pages:
                paragraphs = self._process_by_page(
                    page, x_offset, y_offset, consider_font_size, indent_offset, listing_offset
                )
                page.paragraphs = paragraphs

        return copied_documents

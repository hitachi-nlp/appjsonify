import copy
from collections import Counter
from typing import Any

import numpy as np
from tqdm.contrib import tenumerate

from ..doc import Document, Line, Token
from ..runner import BaseRunner


@BaseRunner.register("extract_lines")
class LineExtractor(BaseRunner):
    """Extract lines."""
    @staticmethod
    def _extract_lines(
        tokens: list[Token],
        y_tolerance: float
    ) -> list[Line]:
        """Extract lines from a given list of tokens in a page.

        Args:
            tokens (list[Token]): A list of tokens.
            y_tolerance (float): A threshold value to determine if different tokens are in the same line.

        Returns:
            list[Line]: A list of lines.
        """
        # init
        lines: list[Line] = []
        prev_token: Token = None
        cache: dict[str, Any] = {
            "token": [], 
            "tokens": [], 
            "x0": -1, 
            "y0": -1, 
            "x1": -1, 
            "y1": -1, 
            "font_size": [],
            "font_name": [], 
            "init": True
        }
        line_min_y0, line_max_y1 = 1000, 0
        
        # process by token
        for token in tokens:
            if prev_token is None:
                # init
                cache: dict[str, Any] = {
                    "token": [token.token], 
                    "tokens": [token],
                    "x0": token.pos[0], 
                    "y0": [token.pos[1]], 
                    "x1": token.pos[2], 
                    "y1": [token.pos[3]],  
                    "font_size": [token.font_size], 
                    "font_name": [token.font_name],
                    "init": True
                }
                line_min_y0, line_max_y1 = token.pos[1], token.pos[3]
            else:
                if abs(token.pos[1] - np.mean(cache["y0"], dtype=int)) <= y_tolerance \
                    or abs(token.pos[3] - np.mean(cache["y1"], dtype=int)) <= y_tolerance:
                    #####
                    # token in the same line => merge
                    #####
                    cache["token"].append(token.token)
                    if int(token.pos[1]) < line_min_y0:
                        line_min_y0 = int(token.pos[1])
                    if int(token.pos[3]) > line_max_y1:
                        line_max_y1 = int(token.pos[3])
                    cache["tokens"].append(token)
                    cache["y0"].append(token.pos[1])
                    cache["y1"].append(token.pos[3])
                    cache["font_size"].append(token.font_size)
                    cache["font_name"].append(token.font_name)
                    cache["init"] = False
                else:
                    #####
                    # token not in the same line => register cache
                    #####
                    if cache["init"] is False:
                        # cache has several elements
                        cache["x1"] = prev_token.pos[2]
                        lines.append(
                            Line(
                                ' '.join(cache["token"]),
                                (cache["x0"], line_min_y0, cache["x1"], line_max_y1),
                                max(cache["font_size"]),
                                Counter(cache["font_name"]).most_common(1)[0][0],
                                cache["tokens"]
                            )
                        )
                    else:
                        # cache has only one element
                        if cache['token'][0] != '':
                            lines.append(
                                Line(
                                    cache["token"].pop(),
                                    (cache["x0"], cache["y0"].pop(), cache["x1"], cache["y1"].pop()),
                                    cache["font_size"].pop(),
                                    cache["font_name"].pop(),
                                    cache["tokens"]
                                )
                            )
                    # clear cache
                    cache = {
                        "token": [token.token], 
                        "tokens": [token],
                        "x0": token.pos[0], 
                        "y0": [token.pos[1]], 
                        "x1": token.pos[2], 
                        "y1": [token.pos[3]],  
                        "font_size": [token.font_size], 
                        "font_name": [token.font_name],
                        "init": True
                    }
                    line_min_y0, line_max_y1 = token.pos[1], token.pos[3]
                    
            # update prev_token
            prev_token = token
            
        else:
            # end of for loop
            if cache["init"] is False:
                cache["x1"] = prev_token.pos[2]
                lines.append(
                    Line(
                        ' '.join(cache["token"]),
                        (cache["x0"], line_min_y0, cache["x1"], line_max_y1),
                        max(cache["font_size"]),
                        Counter(cache["font_name"]).most_common(1)[0][0],
                        cache["tokens"]
                    )
                )
            else:
                if cache['token'][0] != '':
                    lines.append(
                        Line(
                            cache["token"].pop(),
                            (cache["x0"], cache["y0"].pop(), cache["x1"], cache["y1"].pop()),
                            cache["font_size"].pop(),
                            cache["font_name"].pop(),
                            cache["tokens"]
                        )
                    )
        
        return lines
    
    
    def _process_by_doc(
        self, 
        doc: Document,
        y_tolerance: float,
    ) -> Document:
        """Process a PDF document."""
        for index, page in enumerate(doc.pages, start=1):
            # extract lines
            lines = self._extract_lines(page.tokens, y_tolerance)
            # edit page
            page.lines = lines
        return doc


    def execute(
        self, 
        documents: list[Document],
        y_tolerance: float,
        **kwargs: dict
    ) -> list[Document]:
        # init
        self.check_args(self.execute, locals())
        
        # avoid overwrite
        copied_documents: list[Document] = copy.deepcopy(documents)

        # extract lines
        docs: list[Document] = []
        for _, doc in tenumerate(copied_documents, total=len(copied_documents)):
            docs.append(
                self._process_by_doc(
                    doc,
                    y_tolerance
                )
            )
        
        return docs

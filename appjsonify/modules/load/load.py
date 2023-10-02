import copy
import re
import statistics
from collections import Counter
from typing import Any

import pdfplumber
from tqdm.contrib import tenumerate

from ..doc import Document, Page, Token
from ..runner import BaseRunner
from ..common import normalize_bbox


@BaseRunner.register("load_docs")
class DocumentLoader(BaseRunner):
    """Get tokens from input PDF files."""
    @staticmethod
    def _extract_tokens(
        page: pdfplumber.page.Page,
        width: int, 
        height: int, 
        x_tolerance: int
    ) -> list[Token]:
        """Extract tokens from a given page.

        Args:
            page (pdfplumber.page.Page): A target page.
            width (int): A page width.
            height (int): A page height.
            x_tolerance (int): A threshold value to determine if one character forms the same word.

        Returns:
            list[Token]: A list of tokens in a given page.
        """
        def extract_token(
            page: pdfplumber.page.Page,
            word: dict[str, Any],
            width: float,
            height: float
        ) -> Token:
            """Extract a single token."""
            word_bbox = [float(word['x0']), float(word['top']), 
                        float(word['x1']), float(word['bottom'])]
            normalised_word_bbox = normalize_bbox(word_bbox, width, height)
            word_bbox[0] = 0 if word_bbox[0] < 0  else word_bbox[0]
            word_bbox[1] = 0 if word_bbox[1] < 0  else word_bbox[1]
            word_bbox[2] = width if word_bbox[2] > width else word_bbox[2]
            word_bbox[3] = height if word_bbox[3] > height else word_bbox[3]
            try:
                word_font_specs = [(char['fontname'], char['size']) 
                                for char in page.crop(tuple(word_bbox)).chars]
                font_size = round(statistics.median([word_font_spec[1] 
                                                    for word_font_spec in word_font_specs]), 1)
                font_name = Counter([word_font_spec[0] 
                                    for word_font_spec in word_font_specs]).most_common(1)[0][0]
            except ValueError:
                font_size = -1
                font_name = 'default'
            token = Token(
                re.sub(r"\s+", "", word['text']),
                pos=normalised_word_bbox,
                font_size=font_size,
                font_name=font_name
            )
            return token
        
        # init
        tokens: list[Token] = []
        
        # extract words
        words = page.extract_words(
            x_tolerance=x_tolerance, 
            use_text_flow=True
        )
        
        # Generate Token instances
        for word in words:
            tokens.append(
                extract_token(
                    page, word, width, height
                )
            )
        
        return tokens
    

    def _extract_objects_in_page(
            self, 
            page, 
            object_name: str, 
            width: int, 
            height: int
        ) -> list[Token]:
        objs: list[Token] = []
        for obj in getattr(page, object_name):
            # format bbox
            obj_bbox = (float(obj['x0']), float(obj['top']), 
                        float(obj['x1']), float(obj['bottom']))
            obj_bbox = normalize_bbox(obj_bbox, width, height)
            # add to tokens
            objs.append(
                Token(
                    f'[{object_name.capitalize()}]', 
                    obj_bbox,
                    font_size=-1,
                    font_name="default"
                )
            )
        return objs
    
    
    def _parse_by_doc(
            self, 
            doc: Document,
            x_tolerance: float,
        ) -> Document:
        """Parse a PDF document."""
        with pdfplumber.open(str(doc.input_path)) as pdf:
            pages: list[Page] = []
            for index, page in enumerate(pdf.pages, start=1):
                # get height and width of a page
                width, height = int(page.width), int(page.height)
                
                # extract tokens
                tokens = self._extract_tokens(
                    page, width, height, x_tolerance
                )

                # extract object tokens
                images = self._extract_objects_in_page(
                    page, 'images', width, height
                )
                lines = self._extract_objects_in_page(
                    page, 'lines', width, height
                )
                curves = self._extract_objects_in_page(
                    page, 'curves', width, height
                )
                rects= self._extract_objects_in_page(
                    page, 'rects', width, height
                )
                
                # generate a page instance
                page = Page(
                    None, None, tokens,
                    meta={
                        "images": images,
                        "lines": lines,
                        "curves": curves,
                        "rects": rects
                    }
                )
                pages.append(page)
            
            # edit doc
            doc.pages = pages
            doc.meta = pdf.metadata
            
        return doc


    def execute(
        self, 
        documents: list[Document],
        x_tolerance: float,
        **kwargs: dict
    ) -> list[Document]:
        # init
        self.check_args(self.execute, locals())
        
        # avoid overwrite
        copied_documents: list[Document] = copy.deepcopy(documents)

        # load contents
        docs: list[Document] = []
        for _, doc in tenumerate(copied_documents, total=len(copied_documents)):
            docs.append(
                self._parse_by_doc(
                    doc,
                    x_tolerance
                )
            )
        return docs

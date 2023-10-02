import re
import copy
import math

from tqdm.contrib import tenumerate

from ..common import check_token_overlap
from ..doc import Document, Line, Page, Token
from ..runner import BaseRunner


@BaseRunner.register("extract_captions_with_ml")
class MLBasedCaptionExtractor(BaseRunner):
    """Extract captions with ML-based bbox detectors' outputs."""
    @staticmethod
    def get_centroid(bbox: tuple[int], option: str = 'standard') -> tuple[int]:
        if option == 'standard':
            x_pos = (abs(bbox[2] - bbox[0]) / 2) + bbox[0]
            y_pos = (abs(bbox[3] - bbox[1]) / 2) + bbox[1]
        elif option == 'above':
            x_pos = (abs(bbox[2] - bbox[0]) / 2) + bbox[0]
            y_pos = bbox[1]
        elif option == 'below':
            x_pos = (abs(bbox[2] - bbox[0]) / 2) + bbox[0]
            y_pos = bbox[3]
        else:
            raise ValueError('No such a `preset_caption_pos`!')
        return (x_pos, y_pos)
    
    
    def _match_object_with_caption_in_page(
        self, 
        objects: list[Token], 
        captions: list[Token],
        preset_caption_pos: str = 'below',
        caption_assignment_threshold: float = 75.0
    ) -> list[Token]:
        # calculate centroids
        if preset_caption_pos == 'above':
            caption_pos = 'below'
            object_pos = 'above'
        elif preset_caption_pos == 'below':
            caption_pos = 'above'
            object_pos = 'below'
        else:
            caption_pos = 'standard'
            object_pos = 'standard'
        captions = [Token(token.token, 
                          token.pos,
                          -1, 'default',
                          meta=token.meta | {"centroid": self.get_centroid(token.pos, caption_pos)})
                    for token in captions]
        objects = [Token(token.token, 
                         token.pos,
                         -1, 'default',
                         meta=token.meta | {"centroid": self.get_centroid(token.pos, object_pos)})
                    for token in objects]
            
        # calculate distances
        for caption in captions:
            # calculate distance
            caption_pos = caption.meta["centroid"]
            distance_list: list[float] = []
            for target_index, object in enumerate(objects):
                target_pos = object.meta["centroid"]
                distance = math.sqrt(abs(caption_pos[0] - target_pos[0])**2 +
                                     abs(caption_pos[1] - target_pos[1])**2)
                distance_list.append((target_index, distance))
            
            # get the nearest index
            sorted_distance_list = sorted(distance_list, key=lambda x: x[1])
            index = sorted_distance_list[0][0]
            
            # get a caption
            caption_str = ' '.join([token.token 
                                    for token in caption.meta["tokens"]])
            
            # assign captions
            if sorted_distance_list[0][1] < caption_assignment_threshold:
                if objects[index].meta.get("caption") is None:
                    objects[index].meta["caption"] = [caption_str]
                else:
                    if caption_str not in objects[index].meta["caption"]:
                        objects[index].meta["caption"].append(caption_str)
            else:
                print(f'Skip caption matching due to the distance threshold: {sorted_distance_list[0][1]} >= {caption_assignment_threshold}. Caption: {caption_str}.')
                      
        return objects


    @staticmethod
    def classify_captions(
        captions: list[Token],
        table_start_ptn_str: str = r'Table [0-9]+:',
        figure_start_ptn_str: str = r'Figure [0-9]+:'
    ) -> tuple[list[Token], list[Token]]:
        # init
        table_captions: list[Token] = []
        figure_captions: list[Token] = []
        table_start_ptn = re.compile(table_start_ptn_str)
        figure_start_ptn = re.compile(figure_start_ptn_str)
        
        # match
        for caption in captions:
            caption_str = ' '.join([token.token 
                                    for token in caption.meta["tokens"]])
            if table_start_ptn.search(caption_str) is not None:
                table_captions.append(caption)
            elif figure_start_ptn.search(caption_str) is not None:
                figure_captions.append(caption)
            else:
                print(f'No matched object for the caption: "{caption_str}"!')
        
        return (table_captions, figure_captions)
    
    
    def _process_by_page(
        self, 
        page: Page,
        threshold: float,
        table_start_ptn_str: str = r'Table [0-9]+:',
        figure_start_ptn_str: str = r'Figure [0-9]+:',
        preset_table_caption_pos: str = 'below',
        preset_figure_caption_pos: str = 'below',
        caption_assignment_threshold: float = 75.0
    ) -> Page:
        # no captions
        if page.meta.get("captions") == [] and page.meta.get("captions") is not None:
            return page
        
        # divide captions into table captions and figure captions
        table_captions, figure_captions = self.classify_captions(
            page.meta["captions"],
            table_start_ptn_str,
            figure_start_ptn_str
        )
        
        # assign a caption to each table or figure
        if page.meta.get("tables") is not None and page.meta.get("tables") != []:
            if table_captions != []:
                tables = self._match_object_with_caption_in_page(
                    page.meta["tables"],
                    table_captions,
                    preset_table_caption_pos,
                    caption_assignment_threshold
                )
            else:
                tables = page.meta["tables"]
        else:
            tables = []
        if page.meta.get("figures") is not None and page.meta.get("figures") != []:
            if figure_captions != []:
                figures = self._match_object_with_caption_in_page(
                    page.meta["figures"],
                    figure_captions,
                    preset_figure_caption_pos,
                    caption_assignment_threshold
                )
            else:
                figures = page.meta["figures"]
        else:
            figures = []
            
        # remove captions from lines
        lines: list[Line] = []
        for line in page.lines:
            to_be_removed: bool = False
            if page.meta.get("captions") != []:
                for caption in page.meta.get("captions"):
                    if check_token_overlap(caption.pos, line.pos, threshold=threshold):
                        to_be_removed = True
                        break
            if to_be_removed is False:
                lines.append(line)
        
        return Page(
            page.paragraphs,
            lines,
            page.tokens,
            page.meta | {
                "tables": tables,
                "figures": figures
            }
        )


    def execute(
        self, 
        documents: list[Document],
        caption_overlap_threshold: float = 0.5,
        table_start_ptn_str: str = r'Table [0-9]+:',
        figure_start_ptn_str: str = r'Figure [0-9]+:',
        preset_table_caption_pos: str = 'below',
        preset_figure_caption_pos: str = 'below',
        caption_assignment_threshold: float = 75.0,
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
                        caption_overlap_threshold,
                        table_start_ptn_str,
                        figure_start_ptn_str,
                        preset_table_caption_pos,
                        preset_figure_caption_pos,
                        caption_assignment_threshold
                    )
                )
            doc.pages = pages
        return copied_documents

import copy
import os
import re
from pathlib import Path

from pdf2image import convert_from_path
from PIL import Image
from tqdm.contrib import tenumerate

from ...utils import download_individual_file
from ..common import check_token_overlap
from ..doc import Document, Page, Token
from ..runner import BaseRunner
from .models import DocBankModel, PublaynetModel, TableBankModel


@BaseRunner.register("load_objects_with_ml")
class MLBasedObjectLoader(BaseRunner):
    """Load objects with ML-based models."""
    @staticmethod
    def get_object_tokens_in_page(
        object_name: str, 
        obj_bboxes: dict[int, dict],
        tokens: list[Token] = None
    ) -> list[Token]:
        """Get object tokens in a page. If `tokens` is given, associate such tokens to each object token."""
        if tokens is None:
            objs = [
                Token(
                    f'[{object_name}]', 
                    val["bbox"],
                    -1,
                    "default",
                    {"img_path": val["img_path"]}
                ) for val in obj_bboxes.values()
            ]
        else:
            objs: list[Token] = []
            for val in obj_bboxes.values():
                obj_actual_tokens: list[Token] = []
                for token in tokens:
                    if check_token_overlap(
                        val["bbox"], token.pos, threshold=0.50
                    ):
                        obj_actual_tokens.append(token) 
                objs.append(
                    Token(
                        f'[{object_name}]', 
                        val["bbox"], 
                        -1,
                        "default",
                        {
                            "img_path": val["img_path"], 
                            "tokens": obj_actual_tokens
                        }
                    )
                )
        return objs
    
    
    @staticmethod
    def get_title_tokens_in_page(
        obj_bboxes: dict[int, dict],
        tokens: list[Token] = None,
        max_headline_len: int = 20
    ) -> list[Token]:
        """Get title tokens in a page. If `tokens` is given, associate such tokens to each title token."""
        if tokens is None:
            objs = [
                Token(
                    '[TITLE]', 
                    val["bbox"],
                    -1,
                    "default",
                    {"img_path": val["img_path"]}
                ) for val in obj_bboxes.values()
            ]
        else:
            end_str = r".*?[。．.、，,;；:：][0-9]*$"
            end_str_ptn = re.compile(end_str)
            objs: list[Token] = []
            for val in obj_bboxes.values():
                obj_actual_tokens: list[Token] = []
                for token in tokens:
                    if check_token_overlap(
                        val["bbox"], token.pos, threshold=0.50
                    ):
                        obj_actual_tokens.append(token) 
                else:
                    # TODO: Validate the effectiveness
                    # skip this token as it does not seem to be a title
                    if len(obj_actual_tokens) == 0 \
                        or len(obj_actual_tokens) > max_headline_len \
                        or end_str_ptn.search(obj_actual_tokens[-1].token) is not None:
                            continue
                objs.append(
                    Token(
                        '[TITLE]', 
                        val["bbox"],
                        -1,
                        "default",
                        {
                            "img_path": val["img_path"], 
                            "tokens": obj_actual_tokens
                        }
                    )
                )
        return objs
    
    
    @staticmethod
    def adjust_object_bboxes_by_text_bbox(
        obj_bboxes: dict[int, dict], 
        text_bboxes: dict[int, dict]
    ) -> dict[int, dict]:
        """Adjust bboxes to improve performance with the help of text bboxes."""
        _obj_bboxes = copy.deepcopy(obj_bboxes)
        for obj_index, val_obj in obj_bboxes.items():
            val_obj_bbox = val_obj["bbox"]
            for val_text in text_bboxes.values():
                val_text_bbox = val_text["bbox"]
                if check_token_overlap(val_obj_bbox, val_text_bbox, threshold=0.50):
                    # adjust bounding box
                    ret_bbox: list[int] = list(copy.copy(val_obj_bbox))
                    if val_obj_bbox[0] > val_text_bbox[0]: # x0
                        ret_bbox[0] = val_text_bbox[0]
                    if val_obj_bbox[1] > val_text_bbox[1]: # y0
                        ret_bbox[1] = val_text_bbox[1]
                    if val_obj_bbox[2] < val_text_bbox[2]: # x1
                        ret_bbox[2] = val_text_bbox[2]
                    if val_obj_bbox[3] < val_text_bbox[3]: # y1
                        ret_bbox[3] = val_text_bbox[3]
                    _obj_bboxes[obj_index]["bbox"] = ret_bbox
        return _obj_bboxes
    
    
    @staticmethod
    def merge_object_bboxes(
        ref_bboxes: dict[int, dict],
        target_bboxes: dict[int, dict]
    ) -> dict[int, dict]:
        """Merge two bboxes dictionaries.

        Args:
            ref_bboxes (dict[int, dict]): A reference bbox dictionary.
            target_bboxes (dict[int, dict]): A target bbox dictionary.

        Returns:
            dict[int, dict]: A merged bbox dictionary.
        """
        # init
        ret_bboxes: dict[int, dict] = {}
        ret_index: int = 0
        visited = set()
        
        for ref_obj in ref_bboxes.values():
            ref_bbox = ref_obj["bbox"]
            cache: list[dict] = []
            to_be_merged: bool = False
            for target_key, target_obj in target_bboxes.items():
                target_bbox = target_obj["bbox"]
                if check_token_overlap(ref_bbox, target_bbox, threshold=0.50):
                    # add to cache
                    cache.append(target_obj)
                    visited.add(target_key)
                    to_be_merged = True
                    
            if to_be_merged:
                # merge
                bboxes = [list(ref_obj["bbox"])] + [list(obj["bbox"]) for obj in cache]
                x0 = min([bbox[0] for bbox in bboxes])
                y0 = min([bbox[1] for bbox in bboxes])
                x1 = max([bbox[2] for bbox in bboxes])
                y1 = max([bbox[3] for bbox in bboxes])
                img_path = ref_obj["img_path"] if type(ref_obj["img_path"]) == list else [ref_obj["img_path"]]
                for obj in cache:
                    if type(obj["img_path"]) == list:
                        img_path += obj["img_path"]
                    else:
                        img_path += [obj["img_path"]]
                ret_bboxes[ret_index] = {
                    "bbox": (x0, y0, x1, y1),
                    "img_path": img_path
                }
                ret_index += 1
            else:
                ret_bboxes[ret_index] = {
                    "bbox": ref_bbox,
                    "img_path": ref_obj["img_path"]
                }
                ret_index += 1
        
        # check if any elements in target_bboxes are in ret_bboxes
        for target_key, target_obj in target_bboxes.items():
            if target_key not in visited:
                img_path = target_obj["img_path"] if type(target_obj["img_path"]) == list else [target_obj["img_path"]]
                ret_bboxes[ret_index] = {
                    "bbox": target_obj["bbox"],
                    "img_path": target_obj["img_path"]
                }
                ret_index += 1
        
        return ret_bboxes
    
    
    def _process_by_page(
        self,
        page: Page,
        image: Image,
        page_number: int,
        save_image: bool,
        output_image_dir: str,
        tablebank_model: TableBankModel,
        publaynet_model: PublaynetModel,
        docbank_model: DocBankModel,
        max_headline_len: int
    ) -> Page:
        # get bboxes    
        table_bboxes_tablebank = tablebank_model.get_bboxes(
            image,
            page_number,
            save_image,
            output_image_dir
        )
        (table_bboxes_publaynet, figure_bboxes_publaynet, _, text_bboxes) = \
            publaynet_model.get_bboxes(
                image, 
                page_number, 
                save_image, 
                output_image_dir
            )
        (_, _, caption_bboxes, _, equation_bboxes, footer_bboxes, _, 
         title_bboxes, figure_bboxes_docbank, table_bboxes_docbank) = \
            docbank_model.get_bboxes(
                image, 
                page_number, 
                save_image,
                output_image_dir
            )
            
        # adjust bboxes using text bboxes
        caption_bboxes = self.adjust_object_bboxes_by_text_bbox(
            caption_bboxes, text_bboxes
        )
        footer_bboxes = self.adjust_object_bboxes_by_text_bbox(
            footer_bboxes, text_bboxes
        )
        title_bboxes = self.adjust_object_bboxes_by_text_bbox(
            title_bboxes, text_bboxes
        )
        
        # merge bboxes
        # tables
        if table_bboxes_tablebank is not None and table_bboxes_publaynet is not None:
            table_bboxes = self.merge_object_bboxes(
                table_bboxes_tablebank, table_bboxes_publaynet
            )
        elif table_bboxes_tablebank is not None:
            table_bboxes = table_bboxes_tablebank
        elif table_bboxes_publaynet is not None:
            table_bboxes = table_bboxes_publaynet
        else:
            table_bboxes = {}
        if table_bboxes != {} and table_bboxes_docbank is not None:
            table_bboxes = self.merge_object_bboxes(
                table_bboxes, table_bboxes_docbank
            )
        elif table_bboxes_docbank is not None:
            table_bboxes = table_bboxes_docbank
        
        # figures
        if figure_bboxes_docbank is not None and figure_bboxes_publaynet is not None:
            figure_bboxes = self.merge_object_bboxes(
                figure_bboxes_docbank, figure_bboxes_publaynet
            )
        elif figure_bboxes_docbank is not None:
            figure_bboxes = figure_bboxes_docbank
        elif figure_bboxes_publaynet is not None:
            figure_bboxes = figure_bboxes_publaynet
        else:
            figure_bboxes = {}
        
        # get object tokens
        tables = self.get_object_tokens_in_page(
            'TABLE', table_bboxes
        ) if table_bboxes is not None else []
        figures = self.get_object_tokens_in_page(
            'FIGURE', figure_bboxes
        ) if figure_bboxes != {} else []
        captions = self.get_object_tokens_in_page(
            'CAPTION', caption_bboxes, page.tokens
        ) if caption_bboxes != {} else []
        equations = self.get_object_tokens_in_page(
            'EQUATION', equation_bboxes, page.tokens
        ) if equation_bboxes != {} else []
        footers = self.get_object_tokens_in_page(
            'FOOTER', footer_bboxes, page.tokens
        ) if footer_bboxes != {} else []
        titles = self.get_title_tokens_in_page(
            title_bboxes, page.tokens, max_headline_len
        )
        
        return Page(
            page.paragraphs,
            page.lines,
            page.tokens,
            page.meta | {
                "tables": tables,
                "figures": figures,
                "captions": captions,
                "equations": equations,
                "footers": footers,
                "titles": titles
            }
        )


    @staticmethod
    def check_model_file_path() -> str:
        # init
        top_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        configs = {
            "tablebank": {
                "base": os.path.join(top_directory, "weights/tablebank/configs/Base-RCNN-FPN.yaml"),
                "config": os.path.join(top_directory, "weights/tablebank/X152/All_X152.yaml"),
                "weight": os.path.join(top_directory, "weights/tablebank/X152/model_final.pth")
            },
            "publaynet": {
                "base": os.path.join(top_directory, "weights/publaynet/X101/Base-RCNN-FPN.yaml"),
                "config": os.path.join(top_directory, "weights/publaynet/X101/DLA_mask_rcnn_X_101_32x8d_FPN_3x.yaml"),
                "weight": os.path.join(top_directory, "weights/publaynet/X101/model_final_trimmed.pth")
            },
            "docbank": {
                "base": os.path.join(top_directory, "weights/configs/Base-RCNN-FPN.yaml"),
                "config": os.path.join(top_directory, "weights/docbank/X101/X101.yaml"),
                "weight": os.path.join(top_directory, "weights/docbank/X101/model.pth"),
            }
        }
        
        # check paths
        for model_type, path_dict in configs.items():
            for key, val in path_dict.items():
                path = Path(val)
                if path.exists():
                    print('\t{} exists. Use the downloaded file.'.format(val))
                else:
                    print('\t{} does not exist. Download the file.'.format(val))
                    download_individual_file(model_type, key)
        return            
            

    def execute(
        self, 
        documents: list[Document],
        tablebank_threshold: float = 0.9,
        publaynet_threshold: float = 0.75,
        docbank_threshold: float = 0.9,
        detectron_device_mode: str = 'cpu',
        save_image: bool = False,
        output_image_dir: str = '',
        max_headline_len: int = 30,
        **kwargs: dict
    ) -> list[Document]:
        # init
        self.check_args(self.execute, locals())
        self.check_model_file_path()
        top_directory = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        tablebank_model = TableBankModel(
            os.path.join(top_directory, "weights/tablebank/X152/All_X152.yaml"),
            os.path.join(top_directory, "weights/tablebank/X152/model_final.pth"),
            detectron_device_mode,
            tablebank_threshold
        )
        publaynet_model = PublaynetModel(
            os.path.join(top_directory, "weights/publaynet/X101/DLA_mask_rcnn_X_101_32x8d_FPN_3x.yaml"),
            os.path.join(top_directory, "weights/publaynet/X101/model_final_trimmed.pth"),
            detectron_device_mode,
            publaynet_threshold
        )
        docbank_model = DocBankModel(
            os.path.join(top_directory, "weights/docbank/X101/X101.yaml"),
            os.path.join(top_directory, "weights/docbank/X101/model.pth"),
            detectron_device_mode,
            docbank_threshold
        )
        
        # avoid overwrite
        copied_documents = copy.deepcopy(documents)
        for _, doc in tenumerate(copied_documents, total=len(copied_documents)):
            # generate doc images
            pdf_images = convert_from_path(str(doc.input_path))
            
            # output settings
            if save_image is True:
                doc_name: str = doc.input_path.stem
                output_image_dir: Path = Path(output_image_dir)
                if not output_image_dir.exists():
                    output_image_dir.mkdir()
                output_path = output_image_dir / doc_name
                if not output_path.exists():
                    output_path.mkdir()
                output_path = str(output_path)
            else:
                output_path = ""
            
            # process by page
            pages: list[Page] = []
            for index, page in enumerate(doc.pages):
                pages.append(
                    self._process_by_page(
                        page,
                        pdf_images[index],
                        index + 1,
                        save_image,
                        output_path,
                        tablebank_model,
                        publaynet_model,
                        docbank_model,
                        max_headline_len
                    )
                )
            doc.pages = pages
            
        return copied_documents

from pathlib import Path

try:
    from detectron2.config import get_cfg
    from detectron2.data.detection_utils import convert_PIL_to_numpy
except ModuleNotFoundError:
    raise ModuleNotFoundError("Please install detectron2 by specifying `python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'`!")
from PIL import Image

from ...common import normalize_bbox
from .base_model import BaseModel
from .detectron2_demo.predictor import VisualizationDemo


class DocBankModel(BaseModel):
    """Bounding box detector based on DocBank."""
    def __init__(
        self,
        detectron_config_path: str,
        detectron_model_path: str,
        detectron_device_mode: str,
        detectron_threshold: float = 0.9
    ):
        # init
        super().__init__()
        cfg = get_cfg()
        cfg.merge_from_file(detectron_config_path)
        cfg.MODEL.WEIGHTS = detectron_model_path
        cfg.MODEL.DEVICE = detectron_device_mode
        cfg.MODEL.RETINANET.SCORE_THRESH_TEST = detectron_threshold
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = detectron_threshold
        cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = detectron_threshold
        cfg.freeze()
        self.demo = VisualizationDemo(cfg)
        
        # util
        self.index_to_label_name = {
            0: "ABSTRACT",
            1: "AUTHOR",
            2: "CAPTION",
            3: "DATE",
            4: "EQUATION",
            5: "FIGURE",
            6: "FOOTER",
            7: "LIST",
            8: "PARAGRAPH",
            9: "REFERENCE",
            10: "SECTION",
            11: "TABLE",
            12: "TITLE"
        }
    
    def get_bboxes(
        self, 
        img: Image, 
        page_number: int,
        save_image: bool = False,
        output_dir: str = ''
    ) -> tuple[dict[int, dict]]:
        """Get bounding boxes of objects.

        Args:
            img (Image): An image of a page
            page_number (int): A page number
            save_image (bool, optional): Whether to save table images. Defaults to False.
            output_dir (str): If `save_image` is True, specify an output image path.

        Returns:
            tuple[dict[int, dict]]: A tuple of bbox dictionaries.
        """
        # init
        abstract_bboxes: dict[int, dict] = {}
        author_bboxes: dict[int, dict] = {}
        caption_bboxes: dict[int, dict] = {}
        date_bboxes: dict[int, dict] = {}
        equation_bboxes: dict[int, dict] = {}
        footer_bboxes: dict[int, dict] = {}
        section_bboxes: dict[int, dict] = {}
        figure_bboxes: dict[int, dict] = {}
        table_bboxes: dict[int, dict] = {}
        title_bboxes: dict[int, dict] = {}
        np_img = convert_PIL_to_numpy(img, format="BGR")
        h, w = np_img.shape[:2]
        
        # get bbox predictions
        predictions, _ = self.demo.run_on_image(np_img)
        p = predictions["instances"].to('cpu')

        for obj_index, (pred_bbox, _, pred_class) \
            in enumerate(zip(p.pred_boxes, p.scores, p.pred_classes)):
            # tailor bbox info
            bbox = [int(b) for b in pred_bbox.numpy().tolist()]
            normalised_bbox = normalize_bbox(
                [b for b in pred_bbox.numpy().tolist()], w, h
            )
            p_cls = pred_class.numpy().tolist()
            
            # save an object image
            if save_image:
                if output_dir == '' or not Path(output_dir).exists():
                    raise ValueError('Need to specify the valid save path!')
                im_crop = img.crop(bbox)
                obj_img_path = str(Path(output_dir) / f'{page_number}_DOCBANK_{self.index_to_label_name[p_cls]}_{obj_index}.png')
                # add to bboxes
                if self.index_to_label_name[p_cls] == 'ABSTRACT':
                    #abstract_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": obj_img_path}
                    abstract_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": None}
                elif self.index_to_label_name[p_cls] == 'AUTHOR':
                    #author_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": obj_img_path}
                    author_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": None}
                elif self.index_to_label_name[p_cls] == 'CAPTION':
                    im_crop.save(obj_img_path)
                    caption_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": obj_img_path}
                elif self.index_to_label_name[p_cls] == 'DATE':
                    #date_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": obj_img_path}
                    date_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": None}
                elif self.index_to_label_name[p_cls] == 'EQUATION':
                    im_crop.save(obj_img_path)
                    equation_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": obj_img_path}
                elif self.index_to_label_name[p_cls] == 'FOOTER':
                    im_crop.save(obj_img_path)
                    footer_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": obj_img_path}
                elif self.index_to_label_name[p_cls] == 'SECTION':
                    #section_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": obj_img_path}
                    section_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": None}
                elif self.index_to_label_name[p_cls] == 'TITLE':
                    #title_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": obj_img_path}
                    title_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": None}
                elif self.index_to_label_name[p_cls] == 'FIGURE':
                    im_crop.save(obj_img_path)
                    figure_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": obj_img_path}
                elif self.index_to_label_name[p_cls] == 'TABLE':
                    im_crop.save(obj_img_path)
                    table_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": obj_img_path}
                else:
                    pass # LIST, PARAGRAPH, REFERENCE
            else:
                if self.index_to_label_name[p_cls] == 'ABSTRACT':
                    abstract_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": None}
                elif self.index_to_label_name[p_cls] == 'AUTHOR':
                    author_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": None}
                elif self.index_to_label_name[p_cls] == 'CAPTION':
                    caption_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": None}
                elif self.index_to_label_name[p_cls] == 'DATE':
                    date_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": None}
                elif self.index_to_label_name[p_cls] == 'EQUATION':
                    equation_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": None}
                elif self.index_to_label_name[p_cls] == 'FOOTER':
                    footer_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": None}
                elif self.index_to_label_name[p_cls] == 'SECTION':
                    section_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": None}
                elif self.index_to_label_name[p_cls] == 'TITLE':
                    title_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": None}
                elif self.index_to_label_name[p_cls] == 'FIGURE':
                    figure_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": None}
                elif self.index_to_label_name[p_cls] == 'TABLE':
                    table_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": None}
                else:
                    pass # LIST, PARAGRAPH, REFERENCE
        
        return (
            abstract_bboxes, 
            author_bboxes, 
            caption_bboxes, 
            date_bboxes,
            equation_bboxes, 
            footer_bboxes, 
            section_bboxes, 
            title_bboxes,
            figure_bboxes,
            table_bboxes
        )            

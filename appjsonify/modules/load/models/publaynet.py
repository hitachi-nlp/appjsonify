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


class PublaynetModel(BaseModel):
    """Bounding box detector based on Publaynet."""
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
            0: "TEXT",
            1: "TITLE",
            2: "LIST",
            3: "TABLE",
            4: "FIGURE"
        }
    
    
    def get_bboxes(
        self, 
        img: Image, 
        page_number: int,
        save_image: bool = False,
        output_dir: str = ''
    ) -> tuple[dict[int, dict]]:
        """Get bounding boxes of titles, figures, texts, and tables.

        Args:
            img (Image): An image of a page.
            page_number (int): A page number.
            save_image (bool, optional): Whether to save table images. Defaults to False.
            output_dir (str): If `save_image` is True, specify an output image path.

        Returns:
            tuple[dict[int, dict]]: A tuple of bbox dictionaries.
        """
        # init
        figure_bboxes: dict[int, dict] = {}
        table_bboxes: dict[int, dict] = {}
        title_bboxes: dict[int, dict] = {}
        text_bboxes: dict[int, dict] = {}
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
                im_crop = img.crop(bbox)
                if output_dir == '' or not Path(output_dir).exists():
                    raise ValueError('Need to specify the valid save path!')
                obj_img_path = str(Path(output_dir) / f'{page_number}_PUBLAYNET_{self.index_to_label_name[p_cls]}_{obj_index}.png')
                # add to bboxes
                if self.index_to_label_name[p_cls] == 'TEXT':
                    #text_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": obj_img_path}
                    text_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": None}
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
                    pass # LIST  
            else:
                if self.index_to_label_name[p_cls] == 'TEXT':
                    text_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": None}
                elif self.index_to_label_name[p_cls] == 'TITLE':
                    title_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": None}
                elif self.index_to_label_name[p_cls] == 'FIGURE':
                    figure_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": None}
                elif self.index_to_label_name[p_cls] == 'TABLE':
                    table_bboxes[obj_index] = {"bbox": normalised_bbox, "img_path": None}
                else:
                    pass # LIST
        
        return (table_bboxes, figure_bboxes, title_bboxes, text_bboxes)

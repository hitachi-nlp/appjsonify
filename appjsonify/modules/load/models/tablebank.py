from pathlib import Path

import numpy as np
try:
    from detectron2.config import get_cfg
    from detectron2.data.detection_utils import convert_PIL_to_numpy
except ModuleNotFoundError:
    raise ModuleNotFoundError("Please install detectron2 by specifying `python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'`!")
from PIL import Image

from ...common import normalize_bbox
from .base_model import BaseModel
from .detectron2_demo.predictor import VisualizationDemo


class TableBankModel(BaseModel):
    """Table bounding box detector based on TableBank."""
    def __init__(
        self,
        detectron_config_path: str,
        detectron_model_path: str,
        detectron_device_mode: str,
        detectron_threshold: float = 0.9
    ):
        # init
        cfg = get_cfg()
        cfg.merge_from_file(detectron_config_path)
        cfg.MODEL.WEIGHTS = detectron_model_path
        cfg.MODEL.DEVICE = detectron_device_mode
        cfg.MODEL.RETINANET.SCORE_THRESH_TEST = detectron_threshold
        cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = detectron_threshold
        cfg.MODEL.PANOPTIC_FPN.COMBINE.INSTANCES_CONFIDENCE_THRESH = detectron_threshold
        cfg.freeze()
        self.demo = VisualizationDemo(cfg)
    
    
    def get_bboxes(
        self, 
        img: Image, 
        page_number: int,
        save_image: bool = False,
        output_dir: str = ''
    ) -> dict[int, dict]:
        """Get bounding boxes of tables.

        Args:
            img (Image): An image of a page.
            page_number (int): A page number.
            save_image (bool, optional): Whether to save table images. Defaults to False.
            output_dir (str): If `save_image` is True, specify an output image path.

        Returns:
            dict[int, dict]: A table bbox dictionary.
        """
        # init
        table_bboxes: dict[int, dict] = {}
        np_img = convert_PIL_to_numpy(img, format="BGR")
        h, w = np_img.shape[:2]
        
        # get bbox predictions
        predictions, _ = self.demo.run_on_image(np_img)
        p = predictions["instances"].to('cpu')

        for tb_index, (pred_bbox, _, _) \
            in enumerate(zip(p.pred_boxes, p.scores, p.pred_classes)):
            # tailor bbox info
            bbox = [int(b) for b in pred_bbox.numpy().tolist()]
            normalised_bbox = normalize_bbox(
                [b for b in pred_bbox.numpy().tolist()], w, h
            )
            
            # save table image
            if save_image:
                if output_dir == '' or not Path(output_dir).exists():
                    raise ValueError('Need to specify the valid save path!')
                im_crop = img.crop(bbox)
                tb_path = str(Path(output_dir) / f'{page_number}_TABLEBANK_TABLE_{tb_index + 1}.png')
                im_crop.save(tb_path)
                # add to table_bboxs
                table_bboxes[tb_index] = {"bbox": normalised_bbox, "img_path": tb_path}
            else:
                table_bboxes[tb_index] = {"bbox": normalised_bbox, "img_path": None}
        
        return table_bboxes if table_bboxes != {} else None

from PIL import Image

class BaseModel:
    """Base model for a bounding box detector."""
    def __init__(self) -> None:
        pass
    
    def get_bboxes(self, 
                   img: Image, 
                   page_number: int,
                   save_image: bool = False,
                   output_dir: str = '') -> tuple[dict[int, dict]]:
        """Get bounding boxes of objects.

        Args:
            img_path (str): An image of a page.
            page_number (int): A page number.
            save_image (bool, optional): Whether to save table images. Defaults to False.
            output_dir (str): If `save_image` is True, specify an output image path.

        Returns:
            Tuple[Dict[int, Dict]]: A tuple of bbox dictionaries.
        """
        pass

import copy
from tqdm.contrib import tenumerate

from ..runner import BaseRunner
from ..doc import Document, Page, Line
from ..common import judge_within_bbox


@BaseRunner.register("remove_figures_with_ml")
class MLBasedFigureRemover(BaseRunner):
    """Remove figures with ML-based bbox detectors' outputs."""
    def _process_by_page(
        self, 
        page: Page,
        object_bbox_offset: int
    ):
        lines: list[Line] = []
        for line in page.lines:
            to_be_removed: bool = False
            if page.meta.get("figures") != []:
                for figure in page.meta.get("figures"):
                    ref_bbox: tuple[int] = (
                        figure.pos[0] - object_bbox_offset,
                        figure.pos[1] - object_bbox_offset,
                        figure.pos[2] + object_bbox_offset,
                        figure.pos[3] + object_bbox_offset
                    )
                    if judge_within_bbox(ref_bbox, line.pos):
                        to_be_removed = True
                        break
            if to_be_removed is False:
                lines.append(line)
        page.lines = lines
        return                    


    def execute(
        self, 
        documents: list[Document],
        object_bbox_offset: int = 25,
        **kwargs: dict
    ) -> list[Document]:
        # init
        self.check_args(self.execute, locals())
        
        # avoid overwrite
        copied_documents = copy.deepcopy(documents)

        for _, doc in tenumerate(copied_documents, total=len(copied_documents)):
            for page in doc.pages:
                self._process_by_page(page, object_bbox_offset)
        return copied_documents

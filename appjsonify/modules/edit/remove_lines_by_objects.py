import copy
from tqdm.contrib import tenumerate

from ..runner import BaseRunner
from ..doc import Document, Page, Line, Token
from ..common import judge_within_bbox


@BaseRunner.register("remove_lines_by_objects")
class RuleBasedLineRemoverByObjects(BaseRunner):
    """Remove lines by objects."""
    def _process_by_obj(
        self, 
        page: Page, 
        object_bbox_offset: int = 25, 
        remove_by_line: bool = True,
        remove_by_rect: bool = True,
        remove_by_curve: bool = True
    ):
        # init
        vertical_lines: list[tuple[int]] = []
        horizontal_lines: list[tuple[int]] = []
        cross_lines: list[tuple[int]] = []
        for line in page.meta["lines"]:
            if line.pos[0] == line.pos[2]: # vertical line
                vertical_lines.append(line.pos)
            elif line.pos[1] == line.pos[3]: # horizontal line
                horizontal_lines.append(line.pos)
            else:
                cross_lines.append(line.pos)
        rects: list[tuple[int]] = [rect.pos for rect in page.meta["rects"]]
        curves: list[tuple[int]] = [curve.pos for curve in page.meta["curves"]]
        
        # process by line
        ret_lines: list[Line] = []
        for line in page.lines:
            # get line pos
            x0, y0, x1, y1 = line.pos

            # decision based on lines
            skip_line: bool = False
            if remove_by_line:
                for vline in vertical_lines:
                    if (abs(x0 - vline[0]) < object_bbox_offset or abs(x1 - vline[2]) < object_bbox_offset) \
                        and (y0 >= (vline[1] - object_bbox_offset) and y1 <= (vline[3] + object_bbox_offset)):
                        skip_line = True
                        break
                if skip_line:
                    continue
                for hline in horizontal_lines:
                    if (abs(y0 - hline[1]) < object_bbox_offset or abs(y1 - hline[3]) < object_bbox_offset) \
                        and (x0 >= (hline[0] - object_bbox_offset) and x1 <= (hline[2] + object_bbox_offset)):
                        skip_line = True
                        break
                if skip_line:
                    continue
                for cline in cross_lines:
                    ref_bbox: tuple[int] = (
                        cline[0] - object_bbox_offset,
                        cline[1] - object_bbox_offset,
                        cline[2] + object_bbox_offset,
                        cline[3] + object_bbox_offset
                    )
                    if judge_within_bbox(ref_bbox, line.pos):
                        skip_line = True
                        break
                if skip_line:
                    continue

            # decision based on rects
            if remove_by_rect:
                for rect in rects:
                    ref_bbox: tuple[int] = (
                        rect[0] - object_bbox_offset,
                        rect[1] - object_bbox_offset,
                        rect[2] + object_bbox_offset,
                        rect[3] + object_bbox_offset
                    )
                    if judge_within_bbox(ref_bbox, line.pos):
                        skip_line = True
                        break
                if skip_line:
                    continue
            
            # decision based on curves
            if remove_by_curve:
                for curve in curves:
                    ref_bbox: tuple[int] = (
                        curve[0] - object_bbox_offset,
                        curve[1] - object_bbox_offset,
                        curve[2] + object_bbox_offset,
                        curve[3] + object_bbox_offset
                    )
                    if judge_within_bbox(ref_bbox, line.pos):
                        skip_line = True
                        break
                if skip_line:
                    continue
            
            # add to ret_lines
            ret_lines.append(line)

        # update lines
        page.lines = ret_lines
        return


    def execute(
        self, 
        documents: list[Document], 
        object_bbox_offset: int = 25,
        remove_by_line: bool = False,
        remove_by_rect: bool = False,
        remove_by_curve: bool = False,
        **kwargs: dict
    ) -> list[Document]:
        # init
        self.check_args(self.execute, locals())
        
        # avoid overwrite
        copied_documents = copy.deepcopy(documents)

        for _, doc in tenumerate(copied_documents, total=len(copied_documents)):
            for page in doc.pages:
                self._process_by_obj(
                    page, 
                    object_bbox_offset, 
                    remove_by_line, 
                    remove_by_rect, 
                    remove_by_curve
                )
        return copied_documents

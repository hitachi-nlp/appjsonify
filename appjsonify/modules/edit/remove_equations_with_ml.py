import copy
from tqdm.contrib import tenumerate

from ..runner import BaseRunner
from ..doc import Document, Page, Line
from ..common import check_token_overlap


@BaseRunner.register("remove_equations_with_ml")
class MLBasedEquationRemover(BaseRunner):
    """Remove equations with ML-based bbox detectors' outputs."""
    def _process_by_page(
        self, 
        page: Page,
        threshold: float
    ):
        lines: list[Line] = []
        for line in page.lines:
            to_be_removed: bool = False
            if page.meta.get("equations") != []:
                for equation in page.meta.get("equations"):
                    if check_token_overlap(equation.pos, line.pos, threshold=threshold):
                        to_be_removed = True
                        break
            if to_be_removed is False:
                lines.append(line)
        page.lines = lines
        return                    


    def execute(
        self, 
        documents: list[Document],
        equation_overlap_threshold: float,
        **kwargs: dict
    ) -> list[Document]:
        # init
        self.check_args(self.execute, locals())
        
        # avoid overwrite
        copied_documents = copy.deepcopy(documents)

        for _, doc in tenumerate(copied_documents, total=len(copied_documents)):
            for page in doc.pages:
                self._process_by_page(page, equation_overlap_threshold)
        return copied_documents

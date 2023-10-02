Customize `appjsonify`
===

[Go back to top](../README.md)

## 1. Implement your module
To add your own module in `appjsonify`, you first need to use the following `BaseRunner` class template to register your module to the pipeline.

```python
import copy

from tqdm.contrib import tenumerate

from ..doc import Document
from ..runner import BaseRunner

@BaseRunner.register("module_name")
class ModuleClassName(BaseRunner):
    def execute(
        self, 
        documents: list[Document],
        **kwargs: dict
    ) -> list[Document]:
        # init
        self.check_args(self.execute, locals())
        
        # avoid overwrite
        copied_documents: list[Document] = copy.deepcopy(documents)

        # extract lines
        docs: list[Document] = []
        for _, doc in tenumerate(copied_documents, total=len(copied_documents)):
            # DO SOMETHING HERE
        return docs
```

All you have to do is to implement `execute` method, take `documents` and `kwargs` as the input arguments, and return processed `list[Documents]` as its output.


## 2. Register your module
We recommend that you place your Python script in the [`modules/edit`](../appjsonify/modules/edit/) directory if your module is related to editing.

Make sure you add your module path to [`__init__.py`](../appjsonify/modules/edit/__init__.py).

You will also need to register your module with [`pipeline_checker.py`](../appjsonify/utils/pipeline_checker.py) so that `appjsonify` can check the prerequisites modules to run your module.
You can define the prerequisites for your module as `'your_module_name': [list of prerequisite module names in order]` in the `prerequisites` dictionary.

Now you should be ready to use your module in `appjsonify`.

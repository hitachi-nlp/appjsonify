import inspect
from typing import Any

from registrable import Registrable

from .doc import Document


class BaseRunner(Registrable):
    @staticmethod
    def check_args(
        func, 
        arg_dict: dict[str, Any]
    ):
        """Check input arguments and put some warnings when they are default ones."""
        # get default values
        signature = inspect.signature(func)
        defaults = {
            k: v.default
            for k, v in signature.parameters.items()
            if v.default is not inspect.Parameter.empty
        }
        
        # check input args are default or not
        same_params = {}
        for key, val in defaults.items():
            if arg_dict[key] == val:
                same_params[key] = val
        
        # put warnings
        if same_params != {}:
            print('\tThe followings will use the default value as they are not specified or unchanged!')
            for key, val in same_params.items():
                print(f'\t\t{key}:\t{val}')
        return
    
    
    def execute(
        self, 
        documents: list[Document],
        **kwargs: dict
    ) -> list[Document]:
        raise NotImplementedError()

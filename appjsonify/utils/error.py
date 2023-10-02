class NotAPDFError(Exception):
    """Not a PDF error!"""
    def __init__(self, message="The file is not a PDF."):
        self.message = message
        super().__init__(self.message)

class PipelineOrderError(Exception):
    """Pipeline order error!"""
    def __init__(self, message="The given pipeline order is incorrect and violates the prerequisites."):
        self.message = message
        super().__init__(self.message)

class DownloadFailureError(Exception):
    """Download failure error!"""
    def __init__(self, message="Failed to download the file from the given URL."):
        self.message = message
        super().__init__(self.message)

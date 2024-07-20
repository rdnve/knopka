class RequestError(Exception):
    """Exception on general request error"""


class RequestUnhandledException(RequestError):
    """Error due to critical 5** issues"""


class RequestAuthorizationException(RequestError):
    """Error due to incorrect authorization token"""


class DocumentsNotFoundException(RequestError):
    """Documents not found"""


class DocumentsInProcessException(RequestError):
    """Documents are in the process of being prepared"""


class UnableGetFileException(RequestError):
    """Unable to download the file."""


class UnableDownloadFileException(RequestError):
    """Unable to download the file."""

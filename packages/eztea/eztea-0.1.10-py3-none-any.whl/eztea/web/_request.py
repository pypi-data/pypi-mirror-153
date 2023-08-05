from validr import T, modelclass


@modelclass
class FormFile:
    # content type
    content_type: str = T.str
    # secure filename
    filename: str = T.str
    # file data
    data: bytes = T.bytes

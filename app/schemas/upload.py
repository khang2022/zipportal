from schemas.base import BaseSchema
from typing import List


class UploadResponse(BaseSchema):
    preview: dict = None

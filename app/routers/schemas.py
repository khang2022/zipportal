from typing import List

from pydantic import BaseModel


class UploadResponse(BaseModel):
    filename: str = None
    preview: List[dict] = None


class EncodeRequest(BaseModel):
    filename: str = None
    columns: List[str] = None

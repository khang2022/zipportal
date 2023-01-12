from typing import List

from pydantic import BaseModel

class EncodeRequest(BaseModel):
    filename: str = None
    columns: List[str] = None

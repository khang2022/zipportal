from fastapi import APIRouter, Depends

from routers.schemas import EncodeRequest
from services import encode_service

router = APIRouter()


@router.post("/encode")
async def create_upload_file(req: EncodeRequest):
    encode_service.encode_csv(req.filename, hash_cols=req.columns)
    encode_service.upload_to_azure(req.filename, hash_cols=req.columns)
    return {}

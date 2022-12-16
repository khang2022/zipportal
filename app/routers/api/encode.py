from fastapi import APIRouter, Depends
from routers.schemas import EncodeRequest
from services import encode_service
from sercurity import JWTBearer


router = APIRouter()


@router.post("/encode", response_model=dict)
async def create_upload_file(req: EncodeRequest, token: str = Depends(JWTBearer())):
    filename = encode_service.encode_csv(req.filename, hash_cols=req.columns)
    result = encode_service.upload_to_azure(filename)
    encode_service.remove_uploaded_file(filename)
    return result

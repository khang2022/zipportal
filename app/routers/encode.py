from fastapi import APIRouter, Depends
from fastapi.security import HTTPAuthorizationCredentials
from schemas import EncodeRequest
from services import encode_service
from security import get_token

router = APIRouter()


@router.post("/encode", response_model=dict)
async def create_upload_file(req: EncodeRequest, credentials: HTTPAuthorizationCredentials = Depends(get_token)):
    filename = encode_service.encode_csv(req.filename, hash_cols=req.columns)
    result = encode_service.upload_to_azure(filename)
    encode_service.remove_uploaded_file(filename)
    return result

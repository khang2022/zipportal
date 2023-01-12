from fastapi import APIRouter, File, Depends, UploadFile
from fastapi.security import HTTPAuthorizationCredentials
from schemas import UploadResponse
from services import file_service
from routers.deps import limit_file_size
from security import get_token


router = APIRouter()



@router.post(
    "/upload",
    response_model=UploadResponse,
    dependencies=[Depends(limit_file_size)],
)
async def create_upload_file(credentials: HTTPAuthorizationCredentials = Depends(get_token), uploaded_file: UploadFile = File()):
    renamed_file = file_service.save_file(uploaded_file)
    return file_service.response_file(renamed_file)

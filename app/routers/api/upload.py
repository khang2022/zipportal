from fastapi import APIRouter, UploadFile, File, Depends
from routers.schemas import UploadResponse
from services import file_service
from routers.deps import limit_file_size
from sercurity import JWTBearer


router = APIRouter()


@router.post(
    "/upload",
    response_model=UploadResponse,
    dependencies=[Depends(JWTBearer()), Depends(limit_file_size)],
)
async def create_upload_file(uploaded_file: UploadFile = File(...)):
    renamed_file = file_service.save_file(uploaded_file)
    return file_service.response_file(renamed_file)

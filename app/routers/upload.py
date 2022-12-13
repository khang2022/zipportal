from fastapi import APIRouter, Depends
from base.validate import validate_upload_file
from services import upload_service
from schemas import UploadResponse
from typing import List


router = APIRouter()


@router.post("/upload", response_model=List[dict])
async def create_upload_file(uploaded_file=Depends(validate_upload_file)):
    renamed_file = upload_service.save_file(uploaded_file)
    return upload_service.response_file(renamed_file)

from fastapi import APIRouter, Depends, BackgroundTasks
from routers.schemas import EncodeRequest
from services import encode_service

router = APIRouter()


@router.post("/encode", response_model=dict)
async def create_upload_file(req: EncodeRequest, background_tasks: BackgroundTasks):
    filename = encode_service.encode_csv(req.filename, hash_cols=req.columns)
    result = encode_service.upload_to_azure(filename)
    background_tasks.add_task(encode_service.remove_uploaded_file, filename)
    return result

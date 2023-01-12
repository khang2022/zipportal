from fastapi import APIRouter

from .encode import router as encode_router
from .upload import router as upload_router

router = APIRouter()

router.include_router(encode_router)
router.include_router(upload_router)

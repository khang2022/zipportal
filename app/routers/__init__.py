
from routers.api.encode import router as encode_router
from routers.api.upload import router as upload_router
from fastapi import APIRouter

router = APIRouter()

router.include_router(encode_router)
router.include_router(upload_router)
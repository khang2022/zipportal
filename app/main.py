import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from base.configs import settings
from base.log import logger
from routers import encode_router, upload_router

app = FastAPI(
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
)
app.logger = logger
BACKEND_CORS_ORIGINS = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.add_middleware(LimitUploadSize, max_upload_size=500)

app.include_router(upload_router)
app.include_router(encode_router)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )

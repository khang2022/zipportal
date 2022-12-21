import uvicorn
from fastapi_utils.tasks import repeat_every
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread
from base.configs import settings
from base.log import logger
from routers import router
from services import file_service


app = FastAPI(
    openapi_url=f"/openapi.json",
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


app.include_router(router, prefix=settings.API_V1_STR)


@app.on_event("startup")
@repeat_every(seconds=1 * 60)  # 1 hour
async def startup_event_setup():
    file_service.scan_expiry_files()


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )

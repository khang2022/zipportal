import uvicorn

from typing import Callable

from fastapi_utils.tasks import repeat_every
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from threading import Thread
from base.configs import settings
from base.log import logger
from routers import router
from routers.upload import create_upload_file
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

# Workaround to change the schema name
def update_schema_name(app: FastAPI, function: Callable, name: str) -> None:
    """
    Updates the Pydantic schema name for a FastAPI function that takes
    in a fastapi.UploadFile = File(...) or bytes = File(...).

    This is a known issue that was reported on FastAPI#1442 in which
    the schema for file upload routes were auto-generated with no
    customization options. This renames the auto-generated schema to
    something more useful and clear.

    Args:
        app: The FastAPI application to modify.
        function: The function object to modify.
        name: The new name of the schema.
    """
    for route in app.routes:
        if route.endpoint is function:
            route.body_field.type_.__name__ = name
            break

update_schema_name(app, create_upload_file, "CreateUploadSchema")


@app.on_event("startup")
@repeat_every(seconds=1 * 60)  # 1 hour
async def startup_event_setup():
    file_service.scan_expiry_files()


if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8080,
    )

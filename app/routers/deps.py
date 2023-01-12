from fastapi import HTTPException
from starlette import status
from starlette.requests import Request

# from starlette.responses import Response
from base.configs import settings


async def limit_file_size(request: Request):
    if request.method == "POST":
        if "content-length" not in request.headers:
            raise HTTPException(status_code=status.HTTP_411_LENGTH_REQUIRED)
        content_length = int(request.headers["content-length"])
        print(f"content_length {content_length}")
        print(f"settings.FILE_LIMIT {settings.FILE_LIMIT}")
        if content_length > settings.FILE_LIMIT:
            print("limit_file_size")
            raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE)

        form = await request.form()

        allow_list = [
            "text/csv"
        ]
        if form["uploaded_file"].content_type not in allow_list:
            raise HTTPException(415, detail="Invalid document type")

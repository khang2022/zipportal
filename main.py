import os
from pathlib import Path
from starlette_validation_uploadfile import ValidateUploadFileMiddleware
from fastapi import (
    FastAPI,
    Path,
    File,
    UploadFile,
    Request,
    HTTPException,
    Depends,
)
import pandas as pd
from datetime import datetime
import shutil
from typing import List


app = FastAPI()


async def validate_upload_file(uploaded_file: UploadFile = File(...)):
    allow_list = [
        "text/csv",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ]
    if uploaded_file.content_type  in allow_list:
        raise HTTPException(415, detail="Invalid document type")
    if len(await uploaded_file.read()) >= 314572800:  # 300Mbyte
        raise HTTPException(413, detail="Request entity too large")
    return uploaded_file


def rename_file(uploaded_file):
    now = datetime.now()
    insert_name = now.strftime("%m%d%Y%H%M%S")
    index = uploaded_file.filename.find(".")
    uploaded_file.filename = (
        uploaded_file.filename[:index] + insert_name + uploaded_file.filename[index:]
    )
    return uploaded_file

def save_file(uploaded_file):
        renamed_file = rename_file(uploaded_file)
        parent_dir = os.path.join(os.getcwd(), "tmp")
        file_location = f"tmp/{renamed_file.filename}"
        with open(file_location, "a+",encoding='utf-8') as file_object:
            shutil.copyfileobj(renamed_file.file, file_object, length=300*1024*1024)
        
        print(f"file '{renamed_file.filename}' saved at '{file_location}'")


def response_file(filename):
    file_path = os.path.join(os.getcwd(), "tmp",filename)
    preview = None
    if filename.endswith(".xlsx"):
        df_excel = pd.read_excel(file_path, nrows=20, engine="openpyxl").fillna("")
        preview = df_excel.to_dict("records")
    elif filename.endswith(".csv"):
        print(".csv")
        df_csv = pd.read_csv(file_path ,nrows=20).fillna("")
        preview = df_csv.to_dict("records")

    return preview


@app.post("/upload")
async def create_upload_file(uploaded_file=Depends(validate_upload_file)):
    save_file(uploaded_file)
    return response_file(uploaded_file.filename)
    


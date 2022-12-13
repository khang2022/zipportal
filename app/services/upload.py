import os
import pandas as pd
from datetime import datetime
import datetime
from fastapi import HTTPException, UploadFile
from azure.storage.blob.aio import BlobServiceClient
from dotenv import load_dotenv
import time


load_dotenv()

STORAGEACCOUNTURL = os.getenv("STORAGEACCOUNTURL")
STORAGEACCOUNTKEY = os.getenv("STORAGEACCOUNTKEY")
LOCALFILENAME = os.getenv("LOCALFILENAME")
CONTAINERNAME = os.getenv("BLOBNAME")


class UploadService:
    def save_file(self, uploaded_file):
        renamed_file = (
            datetime.datetime.now().strftime("%m%d%Y%H%M%S")
            + "_"
            + str(uploaded_file.filename)
        )
        path = os.path.join(os.getcwd(), "tmp")
        if not os.path.exists(path):
            os.makedirs(path)
        file_location = f"tmp/{renamed_file}"
        with open(file_location, "wb+") as file_object:
            file_object.write(uploaded_file.file.read())
        return renamed_file

    def response_file(self, filename):
        file_path = os.path.join(os.getcwd(), "tmp", filename)
        preview = None
        if filename.endswith(".xlsx"):
            df_excel = pd.read_excel(file_path, nrows=20, engine="openpyxl").fillna("")
            preview = df_excel.to_dict("records")
        elif filename.endswith(".csv"):
            print(".csv")
            df_csv = pd.read_csv(file_path, nrows=20).fillna("")
            preview = df_csv.to_dict("records")

        return preview

    async def upload_to_azure(self, file: UploadFile, file_name: str, file_type: str):
        blob_service_client = BlobServiceClient(
            account_url=STORAGEACCOUNTURL, credential=STORAGEACCOUNTKEY
        )

        container_name = "zeitgeist"
        async with blob_service_client:
            container_client = blob_service_client.get_container_client(container_name)
            try:
                blob_client = container_client.get_blob_client(file_name)
                f = await file.read()
                await blob_client.upload_blob(f)

            except Exception as e:
                print(e)
                return HTTPException(401, "Something went terribly wrong..")

    async def download_blob(self):
        t1 = time.time()
        blob_service_client_instance = BlobServiceClient(
            account_url=STORAGEACCOUNTURL, credential=STORAGEACCOUNTKEY
        )
        async with blob_service_client_instance:
            blob_client_instance = blob_service_client_instance.get_blob_client(
                CONTAINERNAME, BLOBNAME, snapshot=None
            )
            with open(LOCALFILENAME, "wb") as my_blob:
                blob_data = blob_client_instance.download_blob()
                blob_data.readinto(my_blob)
            t2 = time.time()
            print("It takes %s seconds to download " + BLOBNAME % (t2 - t1))


upload_service = UploadService()

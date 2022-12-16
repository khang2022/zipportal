import gc
import shutil
import hashlib
import os
import dask.dataframe as dd
from azure.storage.blob import BlobServiceClient
from base.configs import settings
from base.log import logger
from base.tools import time_benchmark, memory_benchmark


class EncodeService:
    def __init__(self):
        self.azure_client = BlobServiceClient(
            account_url=settings.BLOB_STORAGE_HOST,
            credential=settings.ACCOUNT_SHARED_KEY,
        )

    def _hash_unicode(self, a_string):
        a_string = str(a_string)
        return hashlib.sha256(a_string.encode("utf-8")).hexdigest()

    def _moving_file(self, filename):
        file_path = os.path.join(os.getcwd(), "tmp", filename)
        new_dir_path = path = os.path.join(os.getcwd(), "tmp_read")
        if not os.path.exists(new_dir_path):
            os.makedirs(new_dir_path)
        if os.path.exists(file_path):
            shutil.move(file_path, new_dir_path)
            logger.info(f"moving file {filename} from {file_path} to  {new_dir_path}")

    @time_benchmark
    @memory_benchmark
    def encode_csv(self, filename, hash_cols: list):
        self._moving_file(filename)
        df = dd.read_csv(f"tmp_read/{filename}", blocksize="200mb")
        for i in range(df.npartitions):
            tmp = df.partitions[i]
            tmp[hash_cols] = tmp[hash_cols].applymap(self._hash_unicode)
            tmp.compute()
            path = os.path.join(os.getcwd(), "tmp_hash")
            if not os.path.exists(path):
                os.makedirs(path)
            new_file_name = f"hashed_{filename}"
            tmp.to_csv(f"./tmp_hash/{new_file_name}", single_file=True, mode="a")
            del tmp
            gc.collect()

        logger.info(f"Successfully encode file {filename}")
        return new_file_name

    def upload_to_azure(self, file_name: str):
        upload_file_path = os.path.join(os.getcwd(), "tmp_hash", file_name)
        logger.info(f"file is located in  {upload_file_path}")
        container_client = self.azure_client.get_container_client(
            settings.CONTAINER_NAME
        )

        try:
            blob_client = container_client.get_blob_client(file_name)
            with open(file=upload_file_path, mode="rb") as data:
                blob_client.upload_blob(data)
            logger.info(f"Successfully upload file {file_name} to azure storage")
            return {"result": "upload Successful !"}

        except Exception as e:
            logger.error(e)
            return {"result": e.message}

    def remove_uploaded_file(self, file_name):
        upload_file_path_hashed = os.path.join(os.getcwd(), "tmp_hash", file_name)
        tmp_file = file_name.removeprefix("hashed_")
        upload_file_path = os.path.join(os.getcwd(), "tmp_read", tmp_file)
        if os.path.exists(upload_file_path_hashed):
            os.remove(upload_file_path_hashed)
            logger.info(f"remove file {file_name} successfully")
        if os.path.exists(upload_file_path):
            os.remove(upload_file_path)
            logger.info(f"remove file {tmp_file} successfully")


encode_service = EncodeService()

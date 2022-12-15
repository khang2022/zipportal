import gc
import hashlib
from http.client import HTTPException

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

    @time_benchmark
    @memory_benchmark
    def encode_csv(self, filename, hash_cols: list):
        df = dd.read_csv(f"tmp/{filename}", blocksize="200mb")
        for i in range(df.npartitions):
            tmp = df.partitions[i]
            tmp[hash_cols] = tmp[hash_cols].applymap(self._hash_unicode)
            tmp.compute()
            tmp.to_csv(f"./hashed_{filename}", single_file=True, mode="a")
            del tmp
            gc.collect()

        logger.info(f"Successfully encode file {filename}")

    async def upload_to_azure(self, file, file_name: str):
        async with self.azure_client:
            container_client = self.azure_client.get_container_client(
                settings.CONTAINER_NAME
            )
            try:
                blob_client = container_client.get_blob_client(file_name)
                f = await file.read()
                await blob_client.upload_blob(f)

            except Exception as e:
                return HTTPException(
                    500, "Couldn't upload file to container, please retry it"
                )


encode_service = EncodeService()

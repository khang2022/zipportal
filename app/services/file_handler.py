import datetime
import os
import schedule
import time
import pandas as pd
from base.configs import settings
from base.log import logger


class FileHandlerService:
    def save_file(self, uploaded_file):
        renamed_file = (
            datetime.datetime.now().strftime("%m%d%Y%H%M%S")
            + "_"
            + str(uploaded_file.filename)
        )
        logger.info(f"Saved file with name {renamed_file}")
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
            df_csv = pd.read_csv(file_path, nrows=20).fillna("")
            preview = df_csv.to_dict("records")

        return {"filename": filename, "preview": preview}

    def _get_list_files(self):
        upload_file_path = os.path.join(os.getcwd(), "tmp")
        if os.path.exists(upload_file_path):
            for (root, dirs, files) in os.walk(upload_file_path, topdown=True):
                return files

    def _remove_expiry_time(self, list_file):
        list_file = self._get_list_files()
        now = time.time()
        logger.info(f"Scaning expriry file")
        if not list_file:
            logger.info("Nothing to remove!")
        else:
            for file in list_file:
                path = os.path.join(os.getcwd(), "tmp", file)
                if os.path.exists(path):
                    expiry_time = os.stat(path).st_ctime + (settings.TIME_LIMIT * 60)
                    if now >= expiry_time:
                        os.remove(path)
                        logger.info(f"file {file} is expiry time this was deleted")

    def scan_expiry_files(self):
        list_file = self._get_list_files()
        schedule.every(1).minutes.do(self._remove_expiry_time, list_file)
        while True:
            schedule.run_pending()


file_service = FileHandlerService()

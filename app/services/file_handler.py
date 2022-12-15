import datetime
import os

import pandas as pd

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


file_service = FileHandlerService()

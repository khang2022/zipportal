from fastapi import File, UploadFile, HTTPException


async def validate_upload_file(uploaded_file: UploadFile = File(...)):
    allow_list = [
        "text/csv",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ]
    if uploaded_file.content_type not in allow_list:
        raise HTTPException(415, detail="Invalid document type")
    return uploaded_file

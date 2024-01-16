from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "success"}


@app.post("/uploadfile")
async def create_upload_file(file: UploadFile = File(...)):
    print(file.filename)
    return {"message": "success", "id": "test123"}


@app.get("/getresult")
async def get_result(task_id: str):
    return FileResponse("./README.md", filename="result.tsv")

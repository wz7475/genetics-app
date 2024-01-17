from fastapi import FastAPI, UploadFile, File, Body
from fastapi.responses import FileResponse
from time import sleep

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "success"}


@app.post("/uploadFile")
async def create_upload_file(file: UploadFile = File(...)):
    print(file.filename)
    return {"message": "success", "id": "test123"}


@app.post("/getResult")
async def get_result(task_id: str = Body()):
    print(task_id)
    return FileResponse("./README.md", filename="result.tsv")


@app.post("/getStatus")
async def get_status(task_id: str = Body()):
    print(task_id)
    sleep(0.5)
    return {"status": "expired"}  # pending/ready

from fastapi import FastAPI, UploadFile, File, Body
from fastapi.responses import FileResponse
from time import sleep

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


@app.post("/getStatus")
async def get_status(task_id: str = Body()):
    # return {"status": "pending"}
    sleep(0.5)
    return {"status": "expired"}

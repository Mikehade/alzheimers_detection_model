from fastapi import FastAPI, APIRouter, File, UploadFile
from pydantic import BaseModel
from random import choice
from uuid import uuid4
import uvicorn
from ultralytics import YOLO

app = FastAPI()
router = APIRouter()


# change the contents of the below class to affect the input fields
class Values(BaseModel):
    visit: int
    mr_delay: int
    m_f: int
    hand: int
    age: int
    educ: int
    ses: float
    mmse: float
    cdr: float
    etiv: int
    nwbv: float
    asf: float

@router.post("/values")
async def values(values: Values):
    print(values)
    print(values.visit)
    return {"response": choice(['yes', 'no'])}

@router.post("/image")
async def image(file: UploadFile = File(...)):
    with open(f"{file.filename}", "wb") as buffer:
        buffer.write(file.file.read())

    return {"message": "File received"}

app.include_router(router, prefix="")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=5000,
        reload=True
    )
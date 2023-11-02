from fastapi import FastAPI, APIRouter, File, UploadFile
from pydantic import BaseModel
from random import choice
from uuid import uuid4

app = FastAPI()
router = APIRouter()


# change the contents of the below class to affect the input fields
class Values(BaseModel):
    visit: str
    mr_delay: str
    m_f: str
    hand: str
    age: str
    educ: str
    ses: str
    mmse: str
    cdr: str
    etiv: str
    nwbv: str
    asf: str

@router.post("/values")
async def values(values: Values):
    print(values)
    return {"response": choice(['yes', 'no'])}

@router.post("/image")
async def image(file: UploadFile = File(...)):
    with open(f"{file.filename}", "wb") as buffer:
        buffer.write(file.file.read())

    return {"message": "File received"}

app.include_router(router, prefix="")
from fastapi import FastAPI, APIRouter, File, UploadFile
from pydantic import BaseModel
from random import choice
from uuid import uuid4
import uvicorn
from ultralytics import YOLO
from model_inferences import mri_detector, mri_classifier, mri_rf_classifier
from PIL import Image
import joblib
import io
from numpy import array
import subprocess
from time import sleep

app = FastAPI(title="AI-Enabled Pipeline for Alzheimer's Disease Diagnosis API")
router = APIRouter()

rf_classification_model  = joblib.load(f"./model_weights/alzheimers_random_forest_92.joblib")

verification_model = YOLO("./model_weights/mri_verification_model.pt")

classification_model = YOLO("./model_weights/mri_image_classification_model.pt")


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

@app.get("/", status_code=200)
def hello() -> str:
    """
    Route for welcoming"""

    return "Welcome to the AI-Enabled Pipeline for Alzheimer's Disease Diagnosis"


@router.post("/values")
async def values(values: Values):
    #print(values)
    #print(values.visit)

    values_list = [values.visit, 
                    values.mr_delay,
                    values.m_f,
                    values.hand,
                    values.age,
                    values.educ,
                    values.ses,
                    values.mmse,
                    values.cdr,
                    values.etiv,
                    values.nwbv,
                    values.asf]

    params = array(values_list).reshape(1, -1)

    classifier_instance = mri_rf_classifier(rf_classification_model)
    prediction = classifier_instance.get_prediction(params)


    return {"response": prediction}

@router.post("/image")
async def image(file: UploadFile = File(...)):
    print(type(file))
    #with open(f"{file.filename}", "wb") as buffer:
        #buffer.write(file.file.read())

    # Reset the "cursor" to the beginning of the file
    file.file.seek(0)

    # Get image content
    file_image = file.file.read()

    # Load image
    img = Image.open(io.BytesIO(file_image))

    # Get byte of file
    img_bytes = io.BytesIO()

    img.save(img_bytes, format="JPEG")

    validation_report = mri_detector(verification_model)
    validate_mri_image = validation_report.get_detections(img)
    #print(validate_mri_image)

    if validate_mri_image is True:
        classification_report = mri_classifier(classification_model)
        classify_mri_image = classification_report.get_detections(img)

        #print(classify_mri_image)

        return {"message": classify_mri_image}

    return {"message": "Not a Valid MRI Image"}

app.include_router(router, prefix="")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        port=5005,
        reload=True
    )

    #sleep(30) # delay for 2 minutes
    #subprocess.Popen(["streamlit", "run", "start.py"])

    
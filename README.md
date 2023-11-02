# alzheimers_detection_model
Pipeline for detecting Alzheimer's disease

This pipeline is developed as an AI-Enabled pipeline for assisting Alzheimer's disease disease diagnosis by utilizing a combination of structured data from OASIS on [Kaggle](https://www.kaggle.com/code/hyunseokc/detecting-early-alzheimer-s) and unstructured data using MRI images on [Kaggle](https://www.kaggle.com/datasets/yasserhessein/dataset-alzheimer). A combination of Random Forest classifier and MobleNet image classifier was utilized which was then combined with a Flask API

### How to launch application

- clone alzheimers_detection repository
- cd to the cloned repository
- create virtual environment  (__python -m venv venv__)
- activate virtual environment (Windows: __venv/Scripts/activate__, Linux/Mac: __source venv/bin/activate__)
- install requirements.txt file (__pip install -r requirements.txt__)
- cd to kaggle api (__cd api/kaggle__)
- lunch flask app (__flask run__ or __python app.py__)

Numeric data for testing first stage is available in kaggle/tabular_classification/kaggle_test_data.csv
Image data for testing second stage based on results of first can be found in kaggle/image_classification/test_images


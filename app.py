from flask import Flask, render_template, request, redirect
from random import random, choice
import joblib
import numpy as np

#f"{main_path}/pretrain_resnet_model.json"
from tensorflow.keras.models import Sequential, model_from_json
import tensorflow as tf


from keras.callbacks import Callback, ModelCheckpoint
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout
from keras.wrappers.scikit_learn import KerasClassifier
import keras.backend as K
from PIL import Image
from keras.preprocessing import image

#path = "/home/AlzheimersKaggle/alzheimers_detection/api/kaggle" #for hosting on pythonanywhere
path = "."   #for local hosting
# load json and create model
json_file = open(f"{path}/mobilenet_83_model.json", 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights(f"{path}/mobilenet_83_model.h5")
#print("Loaded model from disk")

def f1_score(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    recall = true_positives / (possible_positives + K.epsilon())
    f1_val = 2*(precision*recall)/(precision+recall+K.epsilon())
    return f1_val

METRICS = [
      tf.keras.metrics.BinaryAccuracy(name='accuracy'),
      tf.keras.metrics.Precision(name='precision'),
      tf.keras.metrics.Recall(name='recall'),
      tf.keras.metrics.AUC(name='auc'),
        f1_score,
]
loaded_model.compile(optimizer='rmsprop', loss='categorical_crossentropy',metrics=METRICS)




loaded_rf = joblib.load(f"{path}/alzheimers_random_forest_92.joblib")



app = Flask(__name__)

def parse(input): 
    input = input.split(',')
    input = input[:len(input) -1]
    for i in input:
        if i == '':
            return []
    return input

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diagnose', methods=['GET', 'POST'])
def diagnose():
    if request.method == 'POST':
        # Values contain The provided values
        values = parse(request.form.get('values'))

        if values == []:
            return "invalid"

        #print(values)
        params = np.array(values).reshape(1, -1)
        prediction = loaded_rf.predict(params)
        result = int(prediction[0])
        encoding_dict = {0:"Positive-Demented", 1:"Non Demented", 2:"Converted"}
        """
        if result == 0:
            diagnosis = "Demented"
        elif result == 1:
            diagnosis = "Non Demented"
        elif result == 2:
            diagnosis = "Converted"  """
        if result in [0, 1, 2]:
            diagnosis = encoding_dict[result]
            if diagnosis == "Non Demented":
                recommend_list = ["Live Brain Healthy Lifestyle", 
                "Engage in Mentally stimulating activities",
                "Continue regular health checkups",
                "Stay Socially active"]
            elif diagnosis == "Converted":
                recommend_list = ["Some medications would be prescribed",
                "Engage in cognitive training and rehabilitation programs",
                "Implement safety measures at home to reduce accidents",
                "Join support groups"]
            else:
                recommend_list = ["More diagnosis predictions will be carried out on MRI scan"]
        else:
            diagnosis = "Invalid"

        response = {
            "response": diagnosis.lower(), 
            "values": recommend_list,
            "response_data": f"The result of this diagnosis is {diagnosis}"
            }   #choice(['yes', 'no'])
        # returning random value yes or no
        return (response)
    else:
        return render_template('diagnose.html', cols = ['Visit', 'MR Delay', 'M/F', 'Hand',
                    'Age', 'EDUC', 'SES', 'MMSE', 'CDR', 'eTIV', 'nWBV', 'ASF'])


@app.route('/image', methods=['GET', 'POST'])
def image():
    if request.method == "POST":
        file = request.files['image']
        file = file.save("image.jpg")
        image = "image.jpg"
        #image = Image.open(image)
        #image = tf.keras.utils.load_img(image)
        image = "image.jpg"  #26 (27).jpg     VeryMildDemented/26 (44).jpg  MildDemented/26 (27).jpg
        # image = Image.open(image)
        #print(image)
        image = tf.keras.utils.load_img(image, target_size=(224, 224))  # Resize the image to (224, 224)
        input_arr = tf.keras.preprocessing.image.img_to_array(image)
        input_arr = np.expand_dims(input_arr, axis=0)  # Add an extra dimension for batch
        #print(input_arr)
        input_arr = input_arr.astype('float32') / 255.  # Normalize the image
        res_img = loaded_model.predict(input_arr)
        #print(res_img)


        # Get the index of the maximum probability value
        predicted_class_index = np.argmax(res_img)
        print(predicted_class_index)

        # Define the class labels corresponding to the indices
        #class_labels = ['Class1', 'Class2', 'Class3', 'Class4']
        class_labels = ['Mild Demented','Moderate Demented','Non Demented','Very Mild Demented']
        # Get the predicted class label
        predicted_class_label = class_labels[predicted_class_index]

        if predicted_class_label == "Non Demented":
            recommend_list = ["Live Brain Healthy Lifestyle", 
                "Engage in Mentally stimulating activities",
                "Continue regular health checkups",
                "Stay Socially active"]
        elif predicted_class_label == "Mild Demented":
            recommend_list = ["Medications would be prescribed", 
                "Therapy could be carried out",
                "Caregiver would be required for patient"]
        elif predicted_class_label == "Moderate Demented":
            recommend_list =  ["Medications would be prescribed", 
                "Home Care Services would be required for effective treatment",
                "Supportive environment would be required"]
        else:
            recommend_list =  ["Some medications would be prescribed",
                "Engage in cognitive training and rehabilitation programs",
                "Implement safety measures at home to reduce accidents",
                "Join support groups"]

        return {
            "result": f"The result of this diagnosis is {predicted_class_label}",
            "recommend": recommend_list
            }

    return render_template('image.html')


if __name__ == '__main__':
    app.run(debug=True)
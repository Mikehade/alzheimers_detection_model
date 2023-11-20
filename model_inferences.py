from ultralytics import YOLO


class mri_detector:
    """
    Class for detecting mri in images
    """

    def __init__(self, model: object):
        self.model = model

    def get_detections(self, input_file: str) -> (bool, str):
        """detect if image is MRI
        """
        # model = self.model
        # model = YOLO(self.model)  # instantiate the model
        prediction = None
        model = self.model
        results = model.predict(input_file)  # obtain predictions
        predictions = []  # declare list to store all predictions
        confidences = []  # declare list to store confidence percentage for all predictions

        for result in results:
            confs_list = [
                round(x, 2) for x in result.boxes.conf.tolist()
            ]  # get list of all confidences
            track = 0
            # for loop to get all predictions and their confidences
            for i in result.boxes.cls:
                predictions.append(model.names[int(i)])
                confidences.append(confs_list[track])
                #print(model.names[int(i)], confs_list[track])
                track += 1

        print(predictions, confidences)
        # Get the maximum key
        dict_pred = dict(zip(confidences, predictions))

        # Get the maximum key
        max_key = max(dict_pred.keys())

        # Get the value of the maximum key
        prediction = dict_pred[max_key]

        #check for predictions with high confidence level
        if prediction is not None:
            if max_key < 0.95:
                prediction = None


        validation = False
        
        if "mri" == prediction:
            validation = True

        return validation



class mri_classifier:
    """
    Class for classifying mri diagnosis
    """

    def __init__(self, model: object):
        self.model = model

    def get_detections(self, input_file: str) -> (bool, str):
        """Detect damaged parts in car

        Parameters
        ----------
        input_file:str
        section: str

        Returns
        -------
        validation : bool
        """
        # model = self.model
        # model = YOLO(self.model)  # instantiate the model
        prediction = None
        model = self.model

        verification = model(input_file)
        
        probabilities = verification[0].probs.data.tolist()

        preds = list(verification[0].names.values())

        if probabilities:

            #get prediction of max confidence
            probability = max(probabilities)

            max_ind = probabilities.index(probability)

            prediction = preds[max_ind]

            #print(prediction, probability)
        
            #check for predictions with high confidence level
            if prediction is not None:
                if probability < 0.50:
                    prediction = None


        return prediction


class mri_rf_classifier:

    def __init__(self, model: object):
        self.model = model

    def get_prediction(self, data: list):
        model = self.model

        prediction = model.predict(data)
        result = int(prediction[0])
        encoding_dict = {0:"Positive-Demented", 1:"Non Demented", 2:"Converted"}
        

        return encoding_dict[result]
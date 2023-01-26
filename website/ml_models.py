from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

from keras.applications.imagenet_utils import preprocess_input
from keras.models import load_model
import keras.utils as image
import numpy as np

def process_image(img_path):
    i = image.load_img(img_path, target_size=(128,128))
    i = image.img_to_array(i)/255.0
    i = i.reshape(1, 128,128,3)
    i = preprocess_input(i)
    return i

class skinGerald:
    def predict_label(img_path):
        model = load_model('website/model/Erika_Model.h5')
        model.make_predict_function()

        p = model.predict(process_image(img_path))
        predsresult = skinGerald.Check_Highest_Prediction(p)

        print(p)
        print("result", predsresult)
        return predsresult

    def Check_Highest_Prediction(prediction_array):
        Highest_value = -10000 # get the highest prediction from the array
        classname = ""
        classindex = 0
        for arrayvalue in prediction_array[0]: # validate each of the value
            classindex+=1
            if arrayvalue > Highest_value:
                Highest_value = arrayvalue
                if classindex == 1:
                    classname = "actinic keratosis"
                elif classindex == 2:
                    classname = "basal cell carcinoma"
                elif classindex == 3:
                    classname = "dermatofibroma"
                elif classindex == 4:
                    classname = "melanoma"
                elif classindex == 5:
                    classname = "nevus"
                else:
                    classname = "vascular lesion"
        return classname

class burn:
    def predict_label(img_path):
        model = load_model('website/model/BurnModel.h5')
        model.make_predict_function()

        p = model.predict(process_image(img_path))
        predResult = burn.Return_Prediction(p)

        print(p)
        print("result", predResult)
        return predResult

    def Return_Prediction(pred_array):
        HighestValue = 0
        burnclass = ""
        index = 0
        for arrayValue in pred_array[0]: 
            index+=1
            if arrayValue > HighestValue:
                HighestValue = arrayValue
                if index == 0:
                    burnclass = "This is First degree burn"
                elif index == 1:
                    burnclass = "This is Second degree burn"  
                else:
                    burnclass = "This is Third degree burn"
        return burnclass

class chatbot:
    def load_classifier():
        label_names = ['B-COUGH', 'I-COUGH', 'B-BREATHLESSNESS', 'I-BREATHLESSNESS', 'B-DIZZINESS', 'I-DIZZINESS', 'B-HEADACHE', 'I-HEADACHE', 'B-CHILLS', 'I-CHILLS', 'B-CHEST_PAIN', 'I-CHEST_PAIN', 'B-BACK_PAIN', 'I-BACK_PAIN', 'B-MUSCLE_PAIN', 'I-MUSCLE_PAIN', 'B-JOINT_PAIN', 'I-JOINT_PAIN', 'B-NECK_PAIN', 'I-NECK_PAIN', 'B-STOMACH_PAIN', 'I-STOMACH_PAIN', 'O']
        id2label = { i: label for i, label in enumerate(label_names) }
        label2id = {v: k for k, v in id2label.items()}

        my_model = AutoModelForTokenClassification.from_pretrained(
            "chatbot",
            num_labels=23,
            id2label=id2label,
            label2id=label2id,
            ignore_mismatched_sizes=True
        )
        tokenizer = AutoTokenizer.from_pretrained("samrawal/bert-base-uncased_clinical-ner")

        # instantiates a pipeline, which uses the model for inference

        token_classifier = pipeline(
            "token-classification", model=my_model, 
            tokenizer=tokenizer,
            aggregation_strategy="first",
            device=0
        )
        
        return token_classifier
    
    def predict_diagnosis(text):
        token_classifier = chatbot.load_classifier()
        return token_classifier(text)

class food:
    def predict_label(img_path):
        dic = {0 : 'Chicken Wings', 1: 'Fish and Chips', 2: 'French Fries', 3: 'French Toast', 4: 'Garlic Bread', 5: 'Macaroni and Cheese', 6: 'Pizza',  7: 'Pork Chop', 8: 'Spaghetti Carbonara', 9: 'Steak'}

        model = load_model('website/model/Food_Model.h5')
        model.make_predict_function()

        p = model.predict(process_image(img_path))

        print(p)
        print(p[0].max())
        print(dic[np.argmax(p[0])])
        return dic[np.argmax(p[0])]
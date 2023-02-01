from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

from keras.applications.imagenet_utils import preprocess_input
from keras.models import load_model
import keras.utils as image
import numpy as np

from flask import Flask, Blueprint, render_template, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

from .forms import LoginForm, RegisterForm
from .models import Users, SkinConditionHistory
from . import db

from datetime import datetime

def process_image(img_path):
    i = image.load_img(img_path, target_size=(128,128))
    i = image.img_to_array(i)
    i = i.reshape(1, 128,128,3)
    i = preprocess_input(i)
    return i

class skin:
    def Check_Highest_Prediction(prediction_array):
        print("Put into dic")
        predictecdic = skin.put_into_dic(prediction_array[0])

        top1 = list(dict(predictecdic).keys())[0]
        top2 = list(dict(predictecdic).keys())[1]
        top3 = list(dict(predictecdic).keys())[2]

        return top1,top2,top3
        
    def predict_label(img_path):
        classlist = ['Actinic Keratosis','basal cell carcinoma','dermatofibroma','melanoma','nevus','vascular lesion']
        model = load_model('website/model/Erika_Model.h5')

        print("Call make_prediction_function()")
        #model.make_predict_function()

        print("Image Path part 2: ", img_path)

        p = model.predict(process_image(img_path))
        print("Original Array: ", p)
        top1,top2,top3 = skin.Check_Highest_Prediction(p)
        print("top1: ", classlist[top1])
        print("top2: ", classlist[top2])
        print("top3: ", classlist[top3])
        return classlist[top1],classlist[top2],classlist[top3]

    def put_into_dic(prediction_array):
        mydict={}
        for index, i in enumerate(prediction_array):
            print(i)
            mydict[index]=f"{i}"
		
        sorteddic = sorted(mydict.items(), key=lambda x:x[1])
        ##print("DICT", mydict)
        print("DICTSORT", sorteddic)

        return sorteddic

    def create_history(img_path, top1, top2, top3,passuser):
        new_skinhistory = SkinConditionHistory(username=passuser, topone = top1, toptwo = top2, topthree = top3, imguploadpath = img_path, dateprediction = str(datetime.now()))
        db.session.add(new_skinhistory)
        db.session.commit()


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
        classlist = ['Chicken Wings','Fish and Chips','French Fries','French Toast','Garlic Bread','Macaroni and Cheese','Pizza','Pork Chop','Spaghetti Carbonara','Steak']

        model = load_model('website/model/Food_Model.h5')
        print("Call make_prediction_function()")
        #model.make_predict_function()

        p = model.predict(process_image(img_path))
        print("Original Array: ", p)
        return classlist[p]
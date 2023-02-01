from flask import Flask,request

from keras.applications.imagenet_utils import preprocess_input
from keras.models import load_model
import keras.utils as image
import numpy as np
from PIL import Image
import os

app = Flask(__name__)

# functions
def process_image(img):
    i = image.load_img(img, target_size=(128,128))
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
        
    def predict_label(i):
        classlist = ['Actinic Keratosis','basal cell carcinoma','dermatofibroma','melanoma','nevus','vascular lesion']
        model = load_model('Erika_Model.h5')

        print("Call make_prediction_function()")

        p = model.predict(i)
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
        print("DICTSORT", sorteddic)

        return sorteddic

class food:
    def Check_Highest_Prediction(prediction_array):
        print("Put into dic")
        predictecdic = food.put_into_dic(prediction_array[0])

        top1 = list(dict(predictecdic).keys())[0]

        return top1

    def predict_label(i):
        classlist = ['Chicken Wings','Fish and Chips','French Fries','French Toast','Garlic Bread','Macaroni and Cheese','Pizza','Pork Chop','Spaghetti Carbonara','Steak']
        model = load_model('Food_Model.h5')

        print("Call make_prediction_function()")

        p = model.predict(i)
        top1 = food.Check_Highest_Prediction(p)
        print("top1: ", classlist[top1])
        return classlist[top1]
        
    def put_into_dic(prediction_array):
        mydict={}
        for index, i in enumerate(prediction_array):
            print(i)
            mydict[index]=f"{i}"
		
        sorteddic = sorted(mydict.items(), key=lambda x:x[1])
        print("DICTSORT", sorteddic)

        return sorteddic


@app.route("/")
def hello_world():
    return 'Flask Dockerized'

@app.route("/skin-condition-model", methods=["GET","POST"])
def returnskinconditionmodel():
    # Use POST and GET method to process and pass results to gebongka
    if request.method == "POST":
        print("Skin Cancer prediction ongoing ================ ")

        # Request to get the file(s) that were passed through the request.post()
        body = request.files
        print("body:", body)
        print("body list:", body.getlist("upload_file"))
        print("body list file:", body.getlist("upload_file")[0])

        # Image is stored in flask filestorage. We need to obtain the image and save it into the docker directory to pass into our function
        # "upload_file" is the key we used to pass in the url
        imgfrombody2 = Image.open(body.getlist("upload_file")[0])
        # We need to save the image first and delete it after (to not make container too big)
        # Give a fix naming for easier reference
        imgfrombody2.save("skin-conditon.png")

        print("Saving image to static folder....")
        img_path = "skin-conditon.png"
        print("Image Path: ", img_path)
        print("- Sucessfully Saved Image to static folder -")

        top1,top2,top3 = skin.predict_label(process_image(img_path))
        print("- Model prediction completed. Displaying results now -")
        print("Skin Cancer prediction Completed ================ ")

        # Delete image after using
        os.remove("skin-conditon.png")
        # Return as a string, to be split in gebongka
        results = top1+";"+top2+";"+top3
        return results
    
    return "Error"

@app.route("/nutrition-analyser-model", methods=["GET","POST"])
def returnnutritionanalysermodel():
    # Use POST and GET method to process and pass results to gebongka
    if request.method == "POST":
        print("Food prediction ongoing ================ ")

        # Request to get the file(s) that were passed through the request.post()
        body = request.files
        print("body:", body)
        print("body list:", body.getlist("upload_file"))
        print("body list file:", body.getlist("upload_file")[0])

        # Image is stored in flask filestorage. We need to obtain the image and save it into the docker directory to pass into our function
        # "upload_file" is the key we used to pass in the url
        imgfrombody2 = Image.open(body.getlist("upload_file")[0])
        # We need to save the image first and delete it after (to not make container too big)
        # Give a fix naming for easier reference
        imgfrombody2.save("nutrition-analyser.png")

        print("Saving image to static folder....")
        img_path = "nutrition-analyser.png"
        print("Image Path: ", img_path)
        print("- Sucessfully Saved Image to static folder -")

        top1 = food.predict_label(process_image(img_path))
        print("- Model prediction completed. Displaying results now -")
        print("Food prediction Completed ================ ")

        # Delete image after using
        os.remove("nutrition-analyser.png")
        # Return as a string, to be split in gebongka
        results = top1
        return results
    
    return "Error"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
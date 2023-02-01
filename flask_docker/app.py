from flask import Flask, request

from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline
from keras.applications.imagenet_utils import preprocess_input
from keras.models import load_model
import keras.utils as image
from PIL import Image
import os

app = Flask(__name__)

# ----- model functions -----

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

class chatbot:
    def load_classifier():
        label_names = ['B-COUGH', 'I-COUGH', 'B-BREATHLESSNESS', 'I-BREATHLESSNESS', 'B-DIZZINESS', 'I-DIZZINESS', 'B-HEADACHE', 'I-HEADACHE', 'B-CHILLS', 'I-CHILLS', 'B-CHEST_PAIN', 'I-CHEST_PAIN', 'B-BACK_PAIN', 'I-BACK_PAIN', 'B-MUSCLE_PAIN', 'I-MUSCLE_PAIN', 'B-JOINT_PAIN', 'I-JOINT_PAIN', 'B-NECK_PAIN', 'I-NECK_PAIN', 'B-STOMACH_PAIN', 'I-STOMACH_PAIN', 'O']
        id2label = { i: label for i, label in enumerate(label_names) }
        label2id = {v: k for k, v in id2label.items()}

        model = AutoModelForTokenClassification.from_pretrained(
            "",
            num_labels=23,
            id2label=id2label,
            label2id=label2id,
            ignore_mismatched_sizes=True
        )
        tokenizer = AutoTokenizer.from_pretrained("samrawal/bert-base-uncased_clinical-ner")

        # instantiates a pipeline, which uses the model for inference

        token_classifier = pipeline(
            "token-classification", model=model, 
            tokenizer=tokenizer,
            aggregation_strategy="first",
            device=0
        )
        
        return token_classifier
    
    def predict_diagnosis(text):
        token_classifier = chatbot.load_classifier()
        return token_classifier(text)

# Gerald's Part ============================================
class burn:
    def predict_label(img_path):
        model = load_model('BurnModel.h5')
        model.make_predict_function()

        pr = model.predict(img_path)
        predResult = burn.Return_Prediction(pr)

        print(pr)
        print("result", predResult)
        return predResult

    def Return_Prediction(pred_array):
        HighestValue = -100
        burnclass = ""
        index = 0
        
        for arrayValue in pred_array[0]: 
            print("THis is index ", index)
            print("THis is Value ", arrayValue)
            if arrayValue > HighestValue:
                HighestValue = arrayValue
                if index == 0:
                    burnclass = "This is First degree burn"
                elif index == 1:
                    burnclass = "This is Second degree burn"  
                else:
                    burnclass = "This is Third degree burn"
            index+=1
        return burnclass


# ----- model routes -----

@app.route("/")
def hello_world():
    return 'Flask Dockerized'

# Erika's Part =====================================================

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

# Deborah's Part =====================================================

@app.route("/submit-diagnosis", methods = ['GET', 'POST'])
def diagnose_symptoms():
	if request.method == 'POST':
		symptom_text = request.form['symptom']
		result = chatbot.predict_diagnosis(symptom_text)
	return result

# Gerald's Part ========================================================
@app.route("/burn-grading-model", methods=["GET","POST"])
def returnBurnGradingModel():
    print("Im about to fo to POST ")
    # Use POST and GET method to process and pass results to gebongka
    if request.method == "POST":
        print("Burn Grading model prediction ongoing ================ ")

        body = request.files
        print("body:", body)
        print("body list:", body.getlist("upload_file"))
        print("body list file:", body.getlist("upload_file")[0])

        imgfrombody2 = Image.open(body.getlist("upload_file")[0])
        imgfrombody2.save("burn-grading.png")

        print("Saving image to static folder....")
        img_path = "burn-grading.png"
        print("Image Path: ", img_path)
        print("- Sucessfully Saved Image to static folder -")

        topBurn = burn.predict_label(process_image(img_path))
        print("- Model prediction completed. Displaying results now -")
        print("Burn Grading Model prediction Completed ================ ")

        # Delete image 
        os.remove("burn-grading.png")

        results = topBurn
        return results
    
    return "Error"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
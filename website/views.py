from flask import Flask, Blueprint, render_template, request, Response
from flask_login import login_required, current_user

from .ml_models import skin, chatbot

from .models import NutritionInformation

import requests
import cv2
import datetime
import os

global capture
capture=0 

views = Blueprint('views', __name__)

# ----- general function -----

def gen_frames():  # generate frame by frame from camera
    camera = cv2.VideoCapture(0)
    global capture
    while True:
        success, frame = camera.read() 
        if success:    
            if(capture):
                capture=0
                now = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
                p = os.path.sep.join(['website\static', "shot_{}.png".format(str(now).replace(":",''))])
                cv2.imwrite(p, frame)
                print('Saving camera image here')
                
            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame,1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass
                
        else:
            pass

# ----- general routes -----

@views.app_errorhandler(404)
def handle_404(err):
    return render_template("page-not-found.html")

@views.route('/')
def index():
    return render_template("index.html")

@views.route('/features')
def features():
    return render_template("features.html")

# ----- model routes -----

# Erika's Part =====================================================

# Load skinCancer html
# HTML is where user submits their image and receive the prediction from the model
@views.route("/skin-condition", methods=['GET', 'POST'])
def skin_condition():
	return render_template("models/skin-condition.html")

# GET/POST method for prediction
@views.route("/submit-skin", methods = ['GET', 'POST'])
@login_required
def submit_skin():
	# When submitting
	if request.method == 'POST':
		print("Skin Cancer prediction ongoing ================ ")

		# Get image from form
		print("Obtaining image given.....")
		img = request.files['my_image']
		print("- Successfully obtained Image -")

		# Create Image path to store and retrieve
		# Use random number to allow same-image upload
		print("Saving image to static folder....")
		img_path = "website/static/" + img.filename
		print("Image Path: ", img_path)
		img.save(img_path)
		print("- Sucessfully Saved Image to static folder -")

		# Store the image in a temporary variable to be passed into the docker
		# Depending on the number of image(s) you wish to pass. If you wish to 
		# pass more than on image, {'upload_file':open(img1,'rb'),'upload_file':open(img2,'rb)}
		# in docker, requesting files will return a immutablemultidict. use .getlist('upload_file') which will return the files in a list
		files = {'upload_file':open(img_path,'rb')}
		print("file: ", files)

		print("Model is now predicting image....")
		print("Passing image to docker....")
		# Request post with the url link to the docker and attach the file
		dockerresults = requests.post("http://127.0.0.1:5000/skin-condition-model",files=files)
		# Resuls will be a string
		print("from docker",dockerresults.text)

		# split the top 3 results into an array
		splittedresults = dockerresults.text.split(";")

		print("Top 1 is: ", splittedresults[0])
		print("Top 2 is: ", splittedresults[1]) 
		print("Top 3 is: ", splittedresults[2])
		#top1,top2,top3 = skin.predict_label(img_path)
		print("- Model prediction completed. Displaying results now -")
		print("Skin Cancer prediction Completed ================ ")

		# Creation of save history
		savehistory = skin.create_history(img.filename,splittedresults[0],splittedresults[1],splittedresults[2], current_user.username)
		print("Save history results: ", savehistory)

	return render_template("models/skin-condition.html", prediction1 = splittedresults[0], prediction2 = splittedresults[1], prediction3 = splittedresults[2], img_path = "/static/" + img.filename)

@views.route("/RequestModel")
def obtainskinConditionModel():
	return render_template("save-history.html")

@views.route("/history-skin-condition")
def loadhistoryskincondition():
	return render_template("history-skin-condition.html")

# Deborah's Part =====================================================

@views.route("/chatbot-diagnosis", methods=['GET', 'POST'])
def chatbot_diagnosis():
	return render_template("models/chatbot-diagnosis.html")

@views.route("/submit-diagnosis", methods = ['GET', 'POST'])
def diagnose_symptoms():
	if request.method == 'POST':
		symptom = request.form['symptom']

		# using api call
		# data = {'symptom': symptom}
		# docker_results = requests.post("http://127.0.0.1:5000/chatbot-diagnosis", data=data)
		# print("result - docker", docker_results)
		# print("result - docker text", docker_results.text)
		# result = chatbot.predict_diagnosis(docker_results.text)[0]['entity_group']

		# using chatbot model locally
		try:
			result = chatbot.predict_diagnosis(symptom)[0]['entity_group']
			diagnosis = result.replace("_", " ").capitalize()
			result = "I have detected that you are experiencing: " + diagnosis
			print(diagnosis)
		except:
			result = "Sorry, I didn't get that. Please try again."
			diagnosis = ""
			result = ""

	return render_template("models/chatbot-diagnosis.html", symptom=symptom, diagnosis=diagnosis, result=result)

# Linfeng's Part ===============================================

@views.route("/nutrition-analyser", methods=['GET', 'POST'])
@login_required
def nutrition_analyser():
	camera = cv2.VideoCapture(0)

	# Boolean of image capture
	capture_bool = 0
	return render_template("models/nutrition-analyser.html", capture_bool=capture_bool)

@views.route('/video_feed')
def video_feed():
    print('here')
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

# GET/POST method for prediction by Camera
@views.route("/submit-nutrition-capture", methods = ['GET', 'POST'])
def analyse_nutrition_capture():
	# When submitting
	if request.method == 'POST':
		print("Nutrition Analyser prediction ongoing ================ ")

		# Get image from form
		print("Obtaining image given.....")
		global capture
		capture=1
		
		# Boolean of image capture
		capture_bool = 1

		# Gettinig image path
		now = datetime.datetime.now().isoformat(sep=" ", timespec="seconds")
		img_path = "website/static/" + "shot_{}.png".format(str(now).replace(":",''))
		print("Image Path: ", img_path)	

	return render_template("models/nutrition-analyser.html", img_link = img_path, capture_bool=capture_bool)

# GET/POST method for prediction by Camera
@views.route("/submit-nutrition-capture-predict", methods = ['GET', 'POST'])
def analyse_nutrition_capture_predict():
	# When submitting
	if request.method == 'POST':
		print("Nutrition Analyser prediction ongoing ================ ")

		# Boolean of image capture
		capture_bool = 0

		# Get image name
		print("Obtaining image given.....")
		img_path = request.form.get('image_path')
		print("Image Path: ", img_path)
		print("- Successfully obtained Image -")

		# Store the image in a temporary variable to be passed into the docker
		# in docker, requesting files will return a immutablemultidict. use .getlist('upload_file') which will return the files in a list
		files = {'upload_file':open(img_path,'rb')}
		print("file: ", files)

		print("Model is now predicting image....")
		print("Passing image to docker....")
		# Request post with the url link to the docker and attach the file
		dockerresults = requests.post("http://127.0.0.1:5000/nutrition-analyser-model",files=files)
		# Resuls will be a string
		print("from docker",dockerresults)		

		# Nutrition Information from database
		allnutritioninformationrows = NutritionInformation.query.all()	

		# Creation of save history
		savehistory = food.create_history(img_path, dockerresults.text, current_user.username)
		print("Save history results: ", savehistory)

	return render_template("models/nutrition-analyser.html", prediction = dockerresults.text, img_path = img_path[8:], capture_bool=capture_bool, NI=allnutritioninformationrows)

# GET/POST method for prediction by File Upload
@views.route("/submit-nutrition-upload", methods = ['GET', 'POST'])
def analyse_nutrition_upload():
	# When submitting
	if request.method == 'POST':
		print("Nutrition Analyser prediction ongoing ================ ")

		# Boolean of image capture
		capture_bool = 0

		# Get image from form
		print("Obtaining image given.....")
		img = request.files['my_image']
		print("- Successfully obtained Image -")

		# Create Image path to store and retrieve
		# Use random number to allow same-image upload
		print("Saving image to static folder....")
		img_path = "website/static/" + img.filename
		print("Image Path: ", img_path)
		img.save(img_path)
		print("- Sucessfully Saved Image to static folder -")

		# Store the image in a temporary variable to be passed into the docker
		# in docker, requesting files will return a immutablemultidict. use .getlist('upload_file') which will return the files in a list
		files = {'upload_file':open(img_path,'rb')}
		print("file: ", files)

		print("Model is now predicting image....")
		print("Passing image to docker....")
		# Request post with the url link to the docker and attach the file
		dockerresults = requests.post("http://127.0.0.1:5000/nutrition-analyser-model",files=files)
		# Resuls will be a string
		print("from docker",dockerresults)
		print("from docker result",dockerresults.text)

		# Nutrition Information from database
		allnutritioninformationrows = NutritionInformation.query.all()		

		# Creation of save history
		savehistory = food.create_history(img_path, dockerresults.text, current_user.username)
		print("Save history results: ", savehistory)	

	return render_template("models/nutrition-analyser.html", prediction = dockerresults.text, img_path = "/static/" + img.filename, capture_bool=capture_bool, NI=allnutritioninformationrows)


@views.route("/burn-grading", methods=['GET', 'POST'])
def burn_grading():
	return render_template("models/burn-grading.html")

@views.route("/submit-grading", methods = ['GET', 'POST'])
def grade_burn():

	imgFileName = ""
	dockres = ""
	if request.method == 'POST':
		print("Part A")
		img = request.files['my_image']
		imgFileName = img.filename
		img_path = "website/static/" + imgFileName
		img.save(img_path)
		print("This is image filename ", imgFileName)
		files = {'upload_file':open(img_path,'rb')}
		print("file: ", files)

		print("Model is now predicting image....")
		print("Passing image to docker....")
		# Request post with the url link to the docker and attach the file
		dockres = requests.post("http://127.0.0.1:5000/burn-grading-model",files=files)
		# Resuls will be a string
		print("from docker",dockres.text)

		# print("This is P ", p)

	return render_template("models/burn-grading.html", prediction = dockres.text, img_path = "/static/" + imgFileName)

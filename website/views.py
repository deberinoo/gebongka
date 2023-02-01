from flask import Blueprint, render_template, request
from flask_login import login_required, current_user

from .ml_models import burn, skin, chatbot, food

import requests

views = Blueprint('views', __name__)

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
		result = chatbot.predict_diagnosis(symptom)[0]['entity_group']
		result = result.replace("_", " ").capitalize()
		print(result)

	return render_template("models/chatbot-diagnosis.html", symptom=symptom, result=result)

# Linfeng's Part ===============================================

@views.route("/nutrition-analyser", methods=['GET', 'POST'])
def nutrition_analyser():
	return render_template("models/nutrition-analyser.html")

@views.route("/submit-nutrition", methods = ['GET', 'POST'])
def analyse_nutrition():
	if request.method == 'POST':
		img = request.files['my_image']

		# Create Image path to store and retrieve
		# Use random number to allow same-image upload
		print("Saving image to static folder....")
		img_path = "website/static/" + img.filename
		print("Image Path: ", img_path)
		img.save(img_path)

		p = food.predict_label(img_path)

	return render_template("models/nutrition-analyser.html", prediction = p, img_path = "/static/" + img.filename)


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

	return render_template("models/burn-grading.html", prediction = dockres, img_path = "/static/" + imgFileName)

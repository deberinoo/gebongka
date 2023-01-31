from flask import Blueprint, render_template, request
from flask_login import login_required

from .ml_models import skin, burn, chatbot, food

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

@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html")

# ----- model routes -----

# Erika's Part =====================================================

# Load skinCancer html
# HTML is where user submits their image and receive the prediction from the model
@views.route("/skin-condition", methods=['GET', 'POST'])
def skin_condition():
	return render_template("models/skin-condition.html")

# GET/POST method for prediction
@views.route("/submit-skin", methods = ['GET', 'POST'])
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
		
		print("Model is now predicting image....")
		top1,top2,top3 = skin.predict_label(img_path)
		print("- Model prediction completed. Displaying results now -")
		print("Skin Cancer prediction Completed ================ ")

	return render_template("models/skin-condition.html", prediction1 = top1, prediction2 = top2, prediction3 = top3, img_path = "/static/" + img.filename)

# Deborah's Part =====================================================

@views.route("/chatbot-diagnosis", methods=['GET', 'POST'])
def chatbot_diagnosis():
	return render_template("models/chatbot-diagnosis.html")

@views.route("/submit-diagnosis", methods = ['GET', 'POST'])
def diagnose_symptoms():
	if request.method == 'POST':
		symptom_text = request.form['symptom']
		print(symptom_text)
		print(chatbot.predict_diagnosis(symptom_text))
	return render_template("models/chatbot-diagnosis.html")

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

# @views.route("/burn-grading", methods=['GET', 'POST'])
# def burn_grading():
# 	return render_template("burn-grading.html")


# @views.route("/submit-burn", methods = ['GET', 'POST'])
# def grade_burn():
# 	if request.method == 'POST':
# 		img = request.files['my_image']

# 		img_path = "website/static/" + img.filename	
# 		img.save(img_path)

# 		p = burn.predict_label(img_path)

# 	return render_template("burn-grading.html", prediction = p, img_path = "/static/" + img.filename)

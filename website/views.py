from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from flask import request

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

@views.route("/skin-condition", methods=['GET', 'POST'])
def skin_condition():
	return render_template("models/skin-condition.html")

@views.route("/submit-skin", methods = ['GET', 'POST'])
def predict_skin_condition():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "website/static/" + img.filename	
		img.save(img_path)

		p = skin.predict_label(img_path)

	return render_template("models/skin-condition.html", prediction = p, img_path = "/static/" + img.filename)

@views.route("/nutrition-analyser", methods=['GET', 'POST'])
def nutrition_analyser():
	return render_template("models/nutrition-analyser.html")

@views.route("/submit-nutrition", methods = ['GET', 'POST'])
def analyse_nutrition():
	if request.method == 'POST':
		img = request.files['my_image']

		img_path = "website/static/" + img.filename	
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
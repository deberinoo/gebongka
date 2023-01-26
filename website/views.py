# Import flask
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from flask import request
from flask import jsonify
# Import tensorflow and other related libraries
import numpy as np
import pandas as pd
import cv2
from tensorflow import keras
from keras.models import load_model
from PIL import Image as im
# Import class from diifferent .py files
from .skin import skin
# Import Other libraries
import random
import string

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

# Erika's Part =====================================================

# Load skinCancer html
# HTML is where user submits their image and receive the prediction from the model
@views.route("/skinCancer", methods=['GET', 'POST'])
def main():
	return render_template("skinCancer.html")

# GET/POST method for prediction
@views.route("/submit", methods = ['GET', 'POST'])

def get_output():

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




	return render_template("skinCancer.html", prediction1 = top1, prediction2 = top2, prediction3 = top3, img_path = "/static/" + img.filename)

# End of Erika's Part ===============================================
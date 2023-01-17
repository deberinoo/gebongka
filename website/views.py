from flask import Blueprint, render_template
from flask_login import login_required, current_user

from flask import request
from flask import jsonify
import numpy as np
import pandas as pd
import cv2
from tensorflow import keras
from keras.models import load_model
from PIL import Image as im

from .skin import skin

views = Blueprint('views', __name__)

# ----- general routes -----

@views.app_errorhandler(404)
def handle_404(err):
    return render_template("page-not-found.html")

@views.route('/')
def index():
    return render_template("index.html")

@views.route('/apps')
def apps():
    return render_template("apps.html")

@views.route('/about-us')
def about_us():
    return render_template("about-us.html")

@views.route('/features')
def features():
    return render_template("features.html")

@views.route('/pages')
def pages():
    return render_template("pages.html")    

@views.route('/profile')
@login_required
def profile():
    return render_template("profile.html")

@views.route('/predictImage', methods=['POST'])
def predict_image():
    model = load_model("website/Erika_Model.h5")

    # Load image from file
    filestream = request.files["file"].read()
    imgbytes = np.fromstring(filestream, np.uint8)
    img = cv2.imdecode(imgbytes, cv2.IMREAD_COLOR)

    # Process the image
    img = cv2.resize(img, (224, 224))
    img = keras.applications.vgg16.preprocess_input(img)
    img = img.reshape(1, 224, 224, 3)

    # Predict and return result
    prediction = skin.make_predictions(img, model)
    result = skin.Check_Highest_prediction(prediction)

    return jsonify({"result" : [
        result
    ]})
from tensorflow import keras
from keras.models import load_model
from keras.preprocessing import image as image_utils
from keras.applications.imagenet_utils import preprocess_input

import numpy as np
import pandas as pd
import cv2

from matplotlib import pyplot as plt
import matplotlib.image as mpimg

class skin():
  def show_image(image_path):
    image = mpimg.imread(image_path)
    plt.imshow(image)

  def make_predictions(image_path, model): 
    skin.show_image(image_path)
    image = image_utils.load_img(image_path, target_size=(128, 128))
    image = image_utils.img_to_array(image)
    image = image.reshape(1,128,128,3)
    image = preprocess_input(image)
    preds = model.predict(image) # This will return an array of the prediction from all 6 classes
    predsresult = skin.Check_Highest_Prediction(preds) # as we want the class name , check_highest_prediction helps in getting the highest prediction and outputing that class instead of just an array
    return predsresult # output the class name

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

# @app.route('/predictImage', methods=['POST'])
# def predictImage():
#   # Load image from file
#   filestream = request.files['file'].read()
#   imgbytes = np.fromstring(filestream, np.uint8)
#   img = cv2.imdecode(imgbytes, cv2.IMREAD_COLOR)

#   # Process the image
#   img = cv2.resize(img, (224, 224))
#   img = keras.applications.vgg16.preprocess_input(img)
#   img = img.reshape(1, 224, 224, 3)

#   # Predict and return result
#   prediction = model.make_predictions(img)
#   result = model.Check_Highest_prediction(prediction)

#   return jsonify({"result" : [
#     result
#   ]})
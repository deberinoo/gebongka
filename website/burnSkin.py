from tensorflow import keras
from keras.models import load_model
import keras.utils as image
import numpy as np
from keras.applications.imagenet_utils import preprocess_input

class BurnSkin:

	def predict_label(img_path):
		dic = {0 : 'First Degree Burn', 1 : 'Second Degree Burn', 2 : 'Third Degree Burn'}

		model = load_model('website/model/BurnModel.h5')

		model.make_predict_function()

		i = image.load_img(img_path, target_size=(128,128))
		i = image.img_to_array(i)/255.0
		i = i.reshape(1, 128,128,3)
		i = preprocess_input(i)
		p = model.predict(i)
		print(p)
		predResult = Return_Prediction(p)
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
    


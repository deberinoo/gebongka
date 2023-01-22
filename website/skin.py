from tensorflow import keras
from keras.models import load_model
import keras.utils as image
import numpy as np
from keras.applications.imagenet_utils import preprocess_input


class skin:

	def predict_label(img_path):
		dic = {0 : 'Actinic Keratosis', 1 : 'basal cell carcinoma', 2 : 'dermatofibroma', 3: 'melanoma', 4: 'nevus', 5:'vascular lesion'}

		model = load_model('website/model/Erika_Model.h5')

		model.make_predict_function()

		i = image.load_img(img_path, target_size=(128,128))
		i = image.img_to_array(i)/255.0
		i = i.reshape(1, 128,128,3)
		i = preprocess_input(i)
		p = model.predict(i)
		print(p)
		predsresult = Check_Highest_Prediction(p)
		print("result", predsresult)
		return predsresult

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
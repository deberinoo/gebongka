# Import tensorflow libraries and other related libraries
import tensorflow as tf
from tensorflow import keras
import keras.layers as layers
from keras.models import load_model
import keras.utils as image
import numpy as np
from keras.applications.imagenet_utils import preprocess_input
import os
import h5py

class skin:

	def predict_label(img_path):
		classlist = ['Actinic Keratosis','basal cell carcinoma','dermatofibroma','melanoma','nevus','vascular lesion']

		
		model = load_model('website/model/Erika_Model.h5')

		print("Call make_prediction_function()")
		model.make_predict_function()

		print("Image Path part 2: ", img_path)

		i = image.load_img(img_path, target_size=(128,128))
		i = image.img_to_array(i)
		i = i.reshape(1, 128,128,3)
		i = preprocess_input(i)
		p = model.predict(i)
		print("Original Array: ", p)
		top1,top2,top3 = Check_Highest_Prediction(p)
		print("top1: ", classlist[top1])
		print("top2: ", classlist[top2])
		print("top3: ", classlist[top3])
		return classlist[top1],classlist[top2],classlist[top3]

def Check_Highest_Prediction(prediction_array):
	print("Put into dic")
	predictecdic = put_into_dic(prediction_array[0])

	top1 = list(dict(predictecdic).keys())[0]
	top2 = list(dict(predictecdic).keys())[1]
	top3 = list(dict(predictecdic).keys())[2]

	return top1,top2,top3

def put_into_dic(prediction_array):
	mydict={}
	for index, i in enumerate(prediction_array):
		print(i)
		mydict[index]=f"{i}"
		
	sorteddic = sorted(mydict.items(), key=lambda x:x[1])
	##print("DICT", mydict)
	print("DICTSORT", sorteddic)

	return sorteddic
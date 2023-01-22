from tensorflow import keras
from keras.models import load_model
import keras.utils as image
import numpy as np
from keras.applications.imagenet_utils import preprocess_input


class food:

	def predict_label(img_path):
		dic = {0 : 'Chicken Wings', 1: 'Fish and Chips', 2: 'French Fries', 3: 'French Toast', 4: 'Garlic Bread', 5: 'Macaroni and Cheese', 6: 'Pizza',  7: 'Pork Chop', 8: 'Spaghetti Carbonara', 9: 'Steak'}

		model = load_model('website/model/Food_Model.h5')

		model.make_predict_function()

		i = image.load_img(img_path, target_size=(128,128))
		i = image.img_to_array(i)/255.0
		i = i.reshape(1, 128,128,3)
		i = preprocess_input(i)
		p = model.predict(i)
		print(p)
		print(p[0].max())
		print(dic[np.argmax(p[0])])
		return dic[np.argmax(p[0])]
from tensorflow import keras
from keras.models import load_model
import keras.utils as image
import numpy as np

class skin:
	def predict_label(img_path):
		dic = {0 : 'Actinic Keratosis', 1 : 'basal cell carcinoma', 2 : 'dermatofibroma', 3: 'melanoma', 4: 'nevus', 5:'vascular lesion'}

		model = load_model('model/Erika_Model.h5')

		model.make_predict_function()

		i = image.load_img(img_path, target_size=(128,128))
		i = image.img_to_array(i)/255.0
		i = i.reshape(1, 128,128,3)
		p = model.predict(i)
		print(p)
		print(p[0].max())
		print(dic[np.argmax(p[0])])
		return dic[np.argmax(p[0])]
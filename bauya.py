class Bauya:

	MODEL_HDF5 = './model_resnet50_100ep-Copy1.h5'
	CAT = ['羊蹄甲 bv', '洋紫荊 bp', '艷紫荊 bb']
	RES = 224

	model = None
	graph = None

	def __init__(self):
		from keras.models import load_model
		import tensorflow as tf
		self.graph = tf.get_default_graph()
		self.model = load_model(self.MODEL_HDF5)

	def _prepareImg(self, f):
		import cv2
		import numpy as np
		img = cv2.imread(f, 1)
		img = cv2.resize(img, (self.RES,self.RES))
		img = np.reshape(img, (-1, self.RES,self.RES,3)) /255.
		return img

	def judge(self, filename):
		import numpy as np
		img = self._prepareImg(filename)
		pred = None
		with self.graph.as_default():
			pred = np.argmax(self.model.predict(img))
		return pred, self.CAT[pred]

if __name__ == "__main__":
	import sys

	if (len(sys.argv) == 2):
		filename = sys.argv[1]
		judge = Bauya()
		cat, cat_str = judge.judge(filename)
		print(cat, cat_str)
	else:
		print('usage: python ' + sys.argv[0] + ' image_filename')

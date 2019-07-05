import cv2
import os
from keras.models import model_from_json
from src.keras_utils import detect_lp
from detectChar import detect_chars
import numpy as np
import scipy.misc
import joblib

# WPOD-NET
cwd = os.getcwd()
print("loading WPOD-Net...")
json_file = open('/home/nam/Desktop/Git/license-plate-recognition/wpod-net/models-wpod-net/lp-detector/wpod-net_update1.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights("/home/nam/Desktop/Git/license-plate-recognition/wpod-net/models-wpod-net/lp-detector/wpod-net_update1.h5")

clf = joblib.load('/home/nam/Desktop/Git/license-plate-recognition/detectChar/RecogChar.joblib')

i = 0
# path_images = "/home/nam/Desktop/folder/data/car_long"
path_images = "/home/nam/Desktop/folder/data/GreenParking"
for root, dir, file in os.walk(path_images):
	for f in file:
		image = cv2.imread(root + "/" + f)
		h, w = image.shape[0:2]
		ratio = float(max(image.shape[:2])) / min(image.shape[:2])
		# side = int(ratio * 576)
		side = int(ratio * 288)
		bound_dim = min(side + (side % (2 ** 4)), 608) #800 608
		Llp, LlpImgs, time = detect_lp(model, image / 255., bound_dim, 2 ** 4, (240, 80), 0.5)
		# print("Co {} bien so".format(len(LlpImgs)))
		for idx, l in enumerate(Llp):
			# print(time)

			pl = LlpImgs[idx] * 255

			pl = scipy.misc.toimage(pl)
			pl = np.array(pl)

			Chars = detect_chars.detect(pl, clf)

			if len(Chars) > 3:
				tlx, tly = l.tl()
				brx, bry = l.br()
				image = cv2.rectangle(image, (int(tlx * w), int(tly * h)), (int(brx * w), int(bry * h)), (255, 255, 0), 2)

				font = cv2.FONT_HERSHEY_SIMPLEX

				cv2.putText(image, Chars, (int(tlx*w), int(bry*h) + 15), font, 0.5, (255, 255, 0), 1, cv2.LINE_AA)

				cv2.imshow("image", image)


				# cv2.imshow("pl", pl)
				c = cv2.waitKey(0)
				if chr(c) == "l":
					cv2.imwrite("/home/nam/Desktop/Git/license-plate-recognition/data/l/" + str(i) + ".jpg", pl)
					i += 1

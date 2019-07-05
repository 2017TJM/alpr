import cv2
import os
from keras.models import model_from_json
from src.keras_utils import detect_lp
import sys

# WPOD-NET
cwd = os.getcwd()
print("loading WPOD-Net...")
json_file = open(os.path.join(sys.path[0], 'models-wpod-net/lp-detector/wpod-net_update1.json'), 'r')
loaded_model_json = json_file.read()
json_file.close()
model = model_from_json(loaded_model_json)
model.load_weights(sys.path[0] + "/models-wpod-net/lp-detector/wpod-net_update1.h5")
# model.load_weights("/models-wpod-net/lp-detector/my-trained-model_backup50.h5")
# model.load_weights("/home/nam/Documents/my-trained-model_final.h5")


path_images = sys.path[1] + "/data/imgCars"
# path_images = ""

for root, dir, file in os.walk(path_images):
	for f in file:
		image = cv2.imread(root + "/" + f)
		ratio = float(max(image.shape[:2])) / min(image.shape[:2])
		# side = int(ratio * 576)
		side = int(ratio * 288)
		bound_dim = min(side + (side % (2 ** 4)), 608) #800 608
		Llp, LlpImgs, time = detect_lp(model, image / 255., bound_dim, 2 ** 4, (240, 80), 0.5)
		print("Co {} bien so".format(len(LlpImgs)))
		# print(time)
		if (len(LlpImgs)):
			for i in LlpImgs:
				cv2.imshow("pl", i)
				cv2.waitKey(0)


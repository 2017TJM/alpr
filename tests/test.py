import cv2
import numpy as np
import preprocess
import Char
import os

for root, dir, file in os.walk("/home/nam/Desktop/Git/license-plate-recognition/data/l"):
    for f in file:
        image = cv2.imread(os.path.join(root, f))
        cv2.imshow("Original", image)  # 80 240
        Chars = []
        imgGrayscale, imgThresh = preprocess.preprocess(image)
        cv2.imshow("thresh", imgThresh)

        contours, hi = cv2.findContours(imgThresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        imcontours = np.zeros_like(image)
        # imcontours = cv2.drawContours(imcontours, contours, -1, (255, 255, 0), 1)
        # cv2.imshow("contours", imcontours)

        Sigs = []
        for contour in contours:
            sig = Char.char(contour)
            if preprocess.checkChar(sig, image.shape[0:2]):
                Chars.append(sig)
        for c in Chars:
            imcontours1 = cv2.drawContours(imcontours, c.contour, -1, (255, 255, 0), 1)
            cv2.rectangle(imcontours1, (c.x, c.y), (c.x + c.w, c.y + c.h), (255, 255, 0), 1)

        cv2.imshow("afterCheckChar", imcontours1)
        cv2.waitKey(0)
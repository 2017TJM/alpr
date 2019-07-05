import cv2
import numpy as np
import os
# mau = cv2.imread("/home/nam/Desktop/folder/data/font/Blur/anhMau.jpg", 0)
# cv2.imshow("Mau", mau)

"""
for root, dir, file in os.walk("/home/nam/Desktop/folder/data/font1"):
    file.sort(key = lambda x: x.split(".")[0])
    for f in file:
        if f == "A.JPG": continue
        path = "/home/nam/Desktop/folder/data/font1/" + f
        img = cv2.imread(path, 0)
        (h, w) = img.shape[:2]
        (cX, cY) = (w // 2, h // 2)
        morong1 = 13
        for angle in range(-30, 30):
            if angle < 0:
                morong1 -= 1/5
            if angle > 0:
                morong1 += 1/5
            morong = int(morong1)
            M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)

            im = cv2.warpAffine(img, M, (w, h), borderValue = (255, 255, 0))

            canny_output = cv2.Canny(img, 100, 50 * 2)
            contours, _ = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            contours_poly = [None] * len(contours)
            boundRect = [None] * len(contours)
            centers = [None] * len(contours)
            for i, c in enumerate(contours):
                contours_poly[i] = cv2.approxPolyDP(c, 3, True)
                boundRect[i] = cv2.boundingRect(contours_poly[i])
                centers[i], _ = cv2.minEnclosingCircle(contours_poly[i])
            Rect = []
            for i in range(len(contours)):
                if centers[i][0] > w / 3 and centers[i][0] < 2 * w / 3 and centers[i][1] > h/3 and centers[i][1] < 2 * h / 3:
                    tx = int(boundRect[i][0])-morong
                    ty = int(boundRect[i][1])-morong + int(morong/3)
                    bx = int(boundRect[i][0] + boundRect[i][2])+morong
                    by = int(boundRect[i][1] + boundRect[i][3])+morong - int(morong/3)
                    Rect.append((tx, ty, bx, by))
                    # cv2.rectangle(im, (tx, ty), \
                    #              (bx, by), (0, 255, 0), 2)
            tx = np.min([i[0] for i in Rect])
            ty = np.min([i[1] for i in Rect])
            bx = np.max([i[2] for i in Rect])
            by = np.max([i[3] for i in Rect])

            cv2.rectangle(im, (tx, ty), \
                          (bx, by), (0, 255, 0), 2)
            cv2.imshow('Contours', im)

            cv2.waitKey(0)
"""
def rotato(img):
    im = img
    (h, w) = img.shape[:2]
    (cX, cY) = (w // 2, h // 2)
    morong1 = 13
    for angle in range(-30, 30):
        if angle < 0:
            morong1 -= 1 / 5
        if angle > 0:
            morong1 += 1 / 5
        morong = int(morong1)
        M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)

        im = cv2.warpAffine(img, M, (w, h), borderValue=(255, 255, 0))

        canny_output = cv2.Canny(img, 100, 50 * 2)
        contours, _ = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        contours_poly = [None] * len(contours)
        boundRect = [None] * len(contours)
        centers = [None] * len(contours)
        for i, c in enumerate(contours):
            contours_poly[i] = cv2.approxPolyDP(c, 3, True)
            boundRect[i] = cv2.boundingRect(contours_poly[i])
            centers[i], _ = cv2.minEnclosingCircle(contours_poly[i])
        Rect = []
        for i in range(len(contours)):
            if centers[i][0] > w / 3 and centers[i][0] < 2 * w / 3 and centers[i][1] > h / 3 and centers[i][
                1] < 2 * h / 3:
                tx = int(boundRect[i][0]) - morong
                ty = int(boundRect[i][1]) - morong + int(morong / 3)
                bx = int(boundRect[i][0] + boundRect[i][2]) + morong
                by = int(boundRect[i][1] + boundRect[i][3]) + morong - int(morong / 3)
                Rect.append((tx, ty, bx, by))
                # cv2.rectangle(im, (tx, ty), \
                #              (bx, by), (0, 255, 0), 2)
        tx = np.min([i[0] for i in Rect])
        ty = np.min([i[1] for i in Rect])
        bx = np.max([i[2] for i in Rect])
        by = np.max([i[3] for i in Rect])

        # cv2.rectangle(im, (tx, ty), \
        #               (bx, by), (0, 255, 0), 2)
        im = im[ty:by, tx:bx]
        cv2.imshow("im", im)
        cv2.waitKey(0)
    return im
def sp_noise(image,prob):

    output = image.copy()
    for i in range(2, image.shape[0]-2):
        for j in range(2, image.shape[1]-2):
            rdn = np.random.random()
            if rdn < prob:
                output[i][j] = np.sum(image[i-2:i+2, j-2:j+2])/25 * 2
            else:
                output[i][j] = image[i][j]

    output = cv2.GaussianBlur(output, (5, 5), 0)

    output = cv2.GaussianBlur(output, (5, 5), 0)
    return output

# thay doi kernel size 1 - 3
# thay doi prob 0.2 - 0.6

# kernel = np.ones((3, 3),np.uint8)
sig = 0
for root, dir, file in os.walk("/home/nam/Desktop/folder/data/font1"):
# for root, dir, file in os.walk("/home/nam/Desktop/folder/data/font/Blur"):
    file.sort(key=lambda x:x.split(".")[0])
    for f in file:
        idx = 0
        img = cv2.imread(root + "/" + f, 0)
        cv2.imshow("imga", img)
        (h, w) = img.shape[:2]
        (cX, cY) = (w // 2, h // 2)
        morong1 = 13
        for angle in range(-30, 30):
            if angle < 0:
                morong1 -= 1 / 5
            if angle > 0:
                morong1 += 1 / 5
            if angle % 10 != 0: continue
            im = img.copy()
            morong = int(morong1)
            M = cv2.getRotationMatrix2D((cX, cY), angle, 1.0)

            im = cv2.warpAffine(im, M, (w, h), borderValue=(255, 255, 0))

            canny_output = cv2.Canny(im, 100, 50 * 2)
            contours, _ = cv2.findContours(canny_output, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            contours_poly = [None] * len(contours)
            boundRect = [None] * len(contours)
            centers = [None] * len(contours)
            for i, c in enumerate(contours):
                contours_poly[i] = cv2.approxPolyDP(c, 3, True)
                boundRect[i] = cv2.boundingRect(contours_poly[i])
                centers[i], _ = cv2.minEnclosingCircle(contours_poly[i])
            Rect = []
            for i in range(len(contours)):
                if centers[i][0] > w / 3 and centers[i][0] < 2 * w / 3 and centers[i][1] > h / 3 and centers[i][
                    1] < 2 * h / 3:
                    tx = int(boundRect[i][0] - morong + morong/2)
                    ty = int(boundRect[i][1] - morong + morong / 3)
                    bx = int(boundRect[i][0] + boundRect[i][2] + morong - morong/2)
                    by = int(boundRect[i][1] + boundRect[i][3] + morong - morong / 3)
                    Rect.append((tx, ty, bx, by))

            if Rect == []: continue
            tx = max(0, np.min([i[0] for i in Rect]))
            ty = max(0, np.min([i[1] for i in Rect]))
            bx = min(w, np.max([i[2] for i in Rect]))
            by = min(h, np.max([i[3] for i in Rect]))
            im = im[ty:by, tx:bx]
            cv2.imshow("im", im)
            # cv2.waitKey(0)
            for kernel_size in range(1, 4):
                kernel = np.ones((kernel_size, kernel_size), np.uint8)
                for prob in [0.2, 0.3, 0.4, 0.5, 0.6]:
                    # cv2.imshow("img", img)
                    dilation = cv2.dilate(im, kernel)
                    # cv2.imshow("dilation", dilation)
                    imgNoise = sp_noise(dilation, prob)
                    # cv2.imshow("n", imgNoise)

                    if sig == 10:
                        sig = 65
                    if sig < 10:
                        a = 0
                        # cv2.imshow("1", imgNoise)
                        cv2.imwrite("/home/nam/Desktop/folder/data/font/Blur/" + str(sig) + "/a_" + str(idx) + ".jpg", imgNoise)
                    else:
                        a = 0
                        # cv2.imshow("1", imgNoise)
                        cv2.imwrite("/home/nam/Desktop/folder/data/font/Blur/" + chr(sig) + "/a_" + str(idx) + ".jpg", imgNoise)
                    idx += 1
                    # cv2.waitKey(0)

        sig += 1


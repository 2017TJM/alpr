import cv2
import math
import numpy as np


GAUSSIAN_SMOOTH_FILTER_SIZE = (5, 5)
ADAPTIVE_THRESH_BLOCK_SIZE = 19
ADAPTIVE_THRESH_WEIGHT = 5

def preprocess(img):
    imgGrayscale = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgMaxContrastGrayscale = maximizeContrast(imgGrayscale)

    imgBlurred = cv2.GaussianBlur(imgMaxContrastGrayscale, GAUSSIAN_SMOOTH_FILTER_SIZE, 0)

    imgThresh = cv2.adaptiveThreshold(imgBlurred, 255.0, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, ADAPTIVE_THRESH_BLOCK_SIZE, ADAPTIVE_THRESH_WEIGHT)

    return imgGrayscale, imgThresh

def maximizeContrast(imgGrayscale):

    structuringElement = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    imgTopHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_TOPHAT, structuringElement)
    imgBlackHat = cv2.morphologyEx(imgGrayscale, cv2.MORPH_BLACKHAT, structuringElement)

    imgGrayscalePlusTopHat = cv2.add(imgGrayscale, imgTopHat)
    imgGrayscalePlusTopHatMinusBlackHat = cv2.subtract(imgGrayscalePlusTopHat, imgBlackHat)
    return imgGrayscalePlusTopHatMinusBlackHat

def findMatching(char, Chars):
	charsMath = []
	for c in Chars:
		if c == char:
			continue
		rArea = float(abs(char.Area - c.Area)/char.Area)
		rWidth = float(abs(char.w - c.w)/char.w)
		rHeight = float(abs(char.h - c.h)/char.h)
		if rArea < 0.5 and rWidth < 0.8 and rHeight < 0.4:
			charsMath.append(c)
	return charsMath

def findListMatching(Chars):
	listMatching = []
	for char in Chars:
		list = findMatching(char, Chars)
		list.append(char)
		if len(list) < 3:
			continue
		listMatching.append(list)
	for l in listMatching:
		l.sort(key = lambda a:a.centerX)

	listMatching = set(tuple(i) for i in listMatching)
	return listMatching

def checkChar(char, shape):
	if char.Area < (shape[0] * shape[1] / 5)and char.w > 2 and char.h > 15 and 0.1 < char.w/char.h and char.w/char.h <2:
		return True
	return False




















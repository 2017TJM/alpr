import cv2
import math
import joblib


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

def remove(chars):
	ct = chars
	for c in chars:
		for c1 in chars:
			if c == c1:
				continue
			if contains(c, c1):
				if c in ct:
					ct.remove(c)
			Trung, Strung = trung(c, c1)
			if Trung:
				Areatb = sum([cha.Area for cha in chars])/len(chars)
				if c.Area/c1.Area < 1/3 and Strung/c.Area > 1/2 and c.Area < Areatb *2/3:
					if c in ct:
						ct.remove(c)
				if c1.Area/c.Area < 1/3 and Strung/c1.Area > 1/2 and c1.Area < Areatb *2/3:
					if c1 in ct:
						ct.remove(c1)
	x = ct
	for c in ct:
		for c1 in ct:
			if c == c1:
				continue
			if contains(c, c1):
				x.remove(c)
	ct = x
	return ct

def contains(char1, char2):
	if ((char1.x + char1.w) < (char2.x + char2.w)) and (char1.x > char2.x) and (char1.y > char2.y) and (
		(char1.y + char1.h) < (char2.y + char2.h)):
		return True
	return False

def trung(char1, char2):
	t1x, t1y, b1x, b1y = char1.x, char1.y, char1.x + char1.w, char1.y + char1.h
	t2x, t2y, b2x, b2y = char2.x, char2.y, char2.x + char2.w, char2.y + char2.h
	dx = min(b1x, b2x) - max(t1x, t2x)
	if (dx <= 0):
		return False, 0
	dy = min(b1y, b2y) - max(t1y, t2y)
	if (dy <= 0):
		return False, 0
	return True, dx*dy
def distanceBetweenChars(firstChar, secondChar):
    intX = firstChar.centerX - secondChar.centerX
    intY = firstChar.centerY - secondChar.centerY
    return math.sqrt((intX ** 2) + (intY ** 2))

# so sanh yt, yb
def sosanh(char1, char2):
	if abs(char1.y - char2.y) < 10 and abs(char1.y + char1.h - char2.y - char2.h) < 10 :
		return True
	return False

def findMatching(char, Chars):
	charsMath = []
	for c in Chars:
		if c == char:
			continue
		rArea = float(abs(char.Area - c.Area)/char.Area)
		rWidth = float(abs(char.w - c.w)/char.w)
		rHeight = float(abs(char.h - c.h)/char.h)
		angle = angleBetweenChars(char, c)
		if rArea < 0.5 and rWidth < 0.8 and rHeight < 0.5 and angle < 8:# and sosanh(c, char):
			charsMath.append(c)
	return charsMath
def findListMatching(Chars):
	listMatching = []
	for char in Chars:
		listt = findMatching(char, Chars)
		listt.append(char)
		if len(listt) < 2:
			continue
		listMatching.append(listt)
	for l in listMatching:
		l.sort(key = lambda a:a.centerX)

	listMatching = set(tuple(i) for i in listMatching)
	return listMatching

def angleBetweenChars(firstChar, secondChar):
    fltAdj = float(abs(firstChar.centerX - secondChar.centerX))
    fltOpp = float(abs(firstChar.centerY - secondChar.centerY))

    if fltAdj != 0.0:
        fltAngleInRad = math.atan(fltOpp / fltAdj)
    else:
        fltAngleInRad = 1.5708
    fltAngleInDeg = fltAngleInRad * (180.0 / math.pi)
    return fltAngleInDeg
def distanceBetweenChars(firstChar, secondChar):
    intX = firstChar.centerX - secondChar.centerX
    intY = firstChar.centerY - secondChar.centerY
    return math.sqrt((intX ** 2) + (intY ** 2))

def chon(Chars):
	listChars = list(Chars)
	l = list(Chars)
	for list1 in l:
		for list2 in l:
			num = 0
			if list1 == list2:
				continue
			for i in list1:
				if i in list2:
					num += 1
			if(num > 1):
				if(len(list1) < len(list2)) and list1 in listChars:
					listChars.remove(list1)
				elif(len(list2) < len(list1) and list2 in listChars):
					listChars.remove(list2)
				else:
					if sum(i.Area for i in list1) < sum(i.Area for i in list2) and list1 in listChars:
						listChars.remove(list1)
					elif sum(i.Area for i in list2) < sum(i.Area for i in list1) and list2 in listChars:
						listChars.remove(list2)
	for l in listChars:
		if(len(l) < 4): listChars.remove(l)
		l = list(l)
		l.sort(key = lambda x:x.centerX)
	listChars.sort(key = lambda x: x[0].y)

	return listChars

indx = 0
indxstr = "iii"

def getChar(Chars, imgPl, clf):
	Sigs = ""
	global indx
	global indxstr
	h, w = imgPl.shape[:2]
	for char in Chars:
		tx = lambda x: max(x-2, 0)
		ty = lambda y: max(y-2, 0)
		bx = lambda x: min(x+2, w)
		by = lambda y: min(y+2, h)
		im = imgPl[ty(char.y):by(char.y+char.h), tx(char.x):bx(char.x+char.w)]
		# cv2.imshow("im", im)
		im = cv2.resize(im, (40, 45))
		im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
		# cv2.imshow("resize", im)
		# c = cv2.waitKey(0)
# DETECT
# 		clf = joblib.load('/home/nam/Desktop/Git/license-plate-recognition/detectChar/RecogChar.joblib')
		imgPre = im
		imgPre = cv2.resize(imgPre, (40, 45))
		imgPre = imgPre / 255.
		imgPre = imgPre.reshape((1, 40*45))
		sig = clf.predict(imgPre)
		if sig != ["None"]:
			Sigs += sig[0]

	return Sigs


def checkChar(char, shape):
	if char.Area < (shape[0] * shape[1] / 5)and char.w > 2 and char.h > 10 and 0.1 < char.w/char.h and char.w/char.h <3\
		and char.w < 50 and char.h < 70 and char.Area > 60:
		return True
	return False

def chonTheoH(listt):

	htb = sum(l.h for l in listt) / len(listt)
	hmax = max(l.h for l in listt)

	listt = list(listt)
	for l in listt:
		if l.h == hmax:
			if hmax >= 1.2 * htb:
				listt.remove(l)
	return listt

def morong(listt):
	ytTb = sum([l.y for l in listt])/len(listt)
	ytMin = min([l.y for l in listt])

	ybTb = sum([(l.y + l.h) for l in listt])/len(listt)
	# xtTb = sum([l.x for l in listt])/len(listt)
	hmax = max([l.h for l in listt])
	htb = sum([l.h for l in listt]) / len(listt)
	if sosanhyt(ytTb, listt) and not sosanhyb(ybTb, listt):
		for l in listt:
			if l.h < htb:
				l.h = hmax + 1

	if not sosanhyt(ytTb, listt) and sosanhyb(ybTb, listt):
		for l in listt:
			if l.y > ytTb:
				l.y = ytMin
				l.h = hmax

	return listt

def sosanhyt(yttb, listt):
	for l in listt:
		if abs(l.y - yttb) > 4:
			return False
	return True
def sosanhyb(ybtb, listt):
	for l in listt:
		if abs(l.y + l.h - ybtb) > 4:
			return False
	return True

def checkHop(sig1, sig2):
	if abs(sig1.x - sig2.x) > 8 or abs(sig1.x+sig1.w - sig2.x-sig2.w) > 8 or (sig1.h + sig2.h) > 35:#\
			# or distanceBetweenChars(sig1, sig2) > 15:
		return False
	return True
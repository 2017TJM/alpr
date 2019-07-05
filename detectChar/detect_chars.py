import cv2
import os
import pre
# from detectChar import pre
import numpy as np
import char
# from detectChar import char
import math



kernel = np.ones((3, 3))


for root, dir, file in os.walk("/home/nam/Desktop/Git/license-plate-recognition/data/l"):
	for f in file:
# def detect(image, clf):
# 	Charssss = []
# 	if True:
		image = cv2.imread(os.path.join(root, f))
		cv2.imshow("Original", image) #80 240
		Chars = []
		imgGrayscale, imgThresh = pre.preprocess(image)
		cv2.imshow("thresh", imgThresh)

		# imgThresh = cv2.morphologyEx(imgThresh, cv2.MORPH_CLOSE, kernel)
		# cv2.imshow("close", imgThresh)

		contours, hi = cv2.findContours(imgThresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

		imcontours = np.zeros_like(image)
		imcontours = cv2.drawContours(imcontours, contours, -1, (255, 255, 0), 1)
		cv2.imshow("contours", imcontours)

		Sigs = []
		for contour in contours:
			sig = char.char(contour)
			Sigs.append(sig)

		imcontours = np.zeros_like(image)
		for sig in Sigs:
			imcontours = cv2.rectangle(imcontours, (sig.x, sig.y), (sig.x + sig.w, sig.y + sig.h), (255, 255, 0), 1)
		cv2.imshow("rectangleContour", imcontours)


		for s1 in Sigs:
			for s2 in Sigs:
				if s1 == s2:
					continue
				if (s1.Area < 60 or s2.Area < 60) or math.sqrt((s1.x - s2.x)**2 + (s1.y - s2.y)**2) > 50:
					continue
				if not pre.checkHop(s1, s2):
					continue
				if pre.trung(s1, s2)[0]:
					continue
				if pre.distanceBetweenChars(s1, s2) > 40:
					continue


				# imcontours = np.zeros_like(image)
				# imcontours = cv2.rectangle(imcontours, (s1.x, s1.y), (s1.x + s1.w, s1.y + s1.h),
				# 							   (255, 255, 0), 1)
				# imcontours = cv2.rectangle(imcontours, (s2.x, s2.y), (s2.x + s2.w, s2.y + s2.h),
				# 						   (255, 255, 0), 1)
				# cv2.imshow("s1s2", imcontours)
				# cv2.waitKey(0)
				# if pre.checkHop(s1, s2) and (s1.Area > 30 or s2.Area > 30) and not pre.trung(s1, s2)[0]\
				# 	and (abs(s1.y + s1.h - s2.y) < 8 or abs(s2.y + s2.h - s1.y) < 8):
				if True:
					if s1.y <= s2.y:
						s1.x = min(s1.x, s2.x)
						s1.y = min(s1.y, s2.y)
						s1.h = max(s1.y + s1.h, s2.y + s2.h) - min(s1.y, s2.y)
						s1.w = max(s1.x + s1.w, s2.x + s2.w) - min(s1.x, s2.x)
						if s2 in Sigs:
							Sigs.remove(s2)
						# imcontours = np.zeros_like(image)
						# imcontours = cv2.rectangle(imcontours, (s1.x, s1.y), (s1.x + s1.w, s1.y + s1.h),
						# 						   (255, 255, 0), 1)
						# cv2.imshow("s1", imcontours)
						# cv2.waitKey(0)
					if s2.y < s1.y:
						s2.x = min(s1.x, s2.x)
						s2.y = min(s1.y, s2.y)
						s2.h = max(s1.y + s1.h, s2.y + s2.h) - min(s1.y, s2.y)
						s2.w = max(s1.x + s1.w, s2.x + s2.w) - min(s1.x, s2.x)
						if s1 in Sigs:
							Sigs.remove(s1)
						# imcontours = np.zeros_like(image)
						# imcontours = cv2.rectangle(imcontours, (s2.x, s2.y), (s2.x + s2.w, s2.y + s2.h),
						# 						   (255, 255, 0), 1)
						# cv2.imshow("s2", imcontours)
						# cv2.waitKey(0)

		imcontours = np.zeros_like(image)
		for sig in Sigs:
			imcontours = cv2.rectangle(imcontours, (sig.x, sig.y), (sig.x + sig.w, sig.y + sig.h), (255, 255, 0), 1)
		cv2.imshow("afterCheckHop", imcontours)


		for sig in Sigs:
			if pre.checkChar(sig, image.shape[0:2]):
				Chars.append(sig)

		imcontours1 = np.zeros_like(image)
		for c in Chars:
			imcontours1 = cv2.drawContours(imcontours1, c.contour, -1, (255, 255, 0), 1)
			cv2.rectangle(imcontours1, (c.x, c.y), (c.x + c.w, c.y + c.h), (255, 255, 0), 1)

		cv2.imshow("afterCheckChar", imcontours1)

		Chars = pre.remove(Chars)

		imcontours1 = np.zeros_like(image)
		for c in Chars:
			imcontours1 = cv2.drawContours(imcontours1, c.contour, -1, (255, 255, 0), 1)
			cv2.rectangle(imcontours1, (c.x, c.y), (c.x + c.w, c.y + c.h), (255, 255, 0), 1)
		cv2.imshow("removed", imcontours1)

		listChars = pre.findListMatching(Chars)

		imcontours1 = np.zeros_like(image)
		for l in listChars:
			for c in l:
				imcontours1 = cv2.drawContours(imcontours1, c.contour, -1, (255, 255, 0), 1)
				cv2.rectangle(imcontours1, (c.x, c.y), (c.x + c.w, c.y + c.h), (255, 255, 0), 1)
		cv2.imshow("findMatch", imcontours1)

		for li in listChars:
			for lj in listChars:
				if li == lj:
					continue
				if li in lj:
					listChars.remove(li)

		# for li in listChars:
		# 	li = pre.morong(li)
		#
		# imcontours1 = np.zeros_like(image)
		# for l in listChars:
		# 	for c in l:
		# 		imcontours1 = cv2.drawContours(imcontours1, c.contour, -1, (255, 255, 0), 1)
		# 		cv2.rectangle(imcontours1, (c.x, c.y), (c.x + c.w, c.y + c.h), (255, 255, 0), 1)
		# cv2.imshow("morong", imcontours1)

		# remove ki tu trung
		# listChars = pre.chon(listChars)
		# # #
		# imcontours1 = np.zeros_like(image)
		# for l in listChars:
		# 	for c in l:
		# 		imcontours1 = cv2.drawContours(imcontours1, c.contour, -1, (255, 255, 0), 1)
		# 		cv2.rectangle(imcontours1, (c.x, c.y), (c.x + c.w, c.y + c.h), (255, 255, 0), 1)
		# cv2.imshow("Chon", imcontours1)

		for listt in listChars:
			imcontours3 = np.zeros_like(image)
			imcontours2 = np.zeros_like(image)

			# Crop ky tu
			# chars = pre.getChar(listt, image, clf)
			# Charssss.append(chars)
			# print("s: ", chars)

			# wtb = sum([l.w for l in listt])/len(listt)
			# wmax = max([l.w for l in listt])/len(listt)
			# htb = sum([l.h for l in listt])/len(listt)
			# hmax = max([l.h for l in listt])/len(listt)
			# centYtb = sum([l.centerY for l in listt])/len(listt)
			# AreaTb = sum([l.Area for l in listt])/len(listt)

			# Mo rong ki tu bi mat
			# for l in listt:
			# 	if l.h < htb:
			# 		if l.y >= centYtb - l.h/2:
			# 			l.y = int(l.y - htb*5/4 + l.h)
			# 			l.h = int(htb*4/3)
			# 		if l.y + l.h <= centYtb + l.h/2:
			# 			l.h = int(htb*4/3)


			for c in listt:
				imcontours3 = cv2.drawContours(imcontours3, c.contour, -1, (255, 255, 0), 1)
				cv2.rectangle(imcontours3, (c.x, c.y), (c.x + c.w, c.y + c.h), (255, 255, 0), 1)
			cv2.imshow("list", imcontours3)


			listt = pre.morong(listt)

			imcontours1 = np.zeros_like(image)
			for c in listt:
				imcontours1 = cv2.drawContours(imcontours1, c.contour, -1, (255, 255, 0), 1)
				cv2.rectangle(imcontours1, (c.x, c.y), (c.x + c.w, c.y + c.h), (255, 255, 0), 1)
			cv2.imshow("morong", imcontours1)



			# listt = pre.chonTheoH(listt)
			#
			# for c in listt:
			# 	imcontours2 = cv2.drawContours(imcontours2, c.contour, -1, (255, 255, 0), 1)
			# 	cv2.rectangle(imcontours2, (c.x, c.y), (c.x + c.w, c.y + c.h), (255, 255, 0), 1)
			# cv2.imshow("list_sau", imcontours2)
			# cv2.waitKey(0)

		# Doan ki tu

		# Tong hop lai
		# for Char in Charssss:
		# 	print(Char)
		flatList = []
		for l in listChars:
			# l = pre.chonTheoH(l)
			for ii in l:
				flatList.append(ii)
		imcontours4 = image.copy()
		flatList = list(set(flatList))
		for c in flatList:
			# imcontours4 = cv2.drawContours(imcontours4, c.contour, -1, (0, 255, 255), 1)
			cv2.rectangle(imcontours4, (c.x, c.y), (c.x + c.w, c.y + c.h), (0, 255, 0), 2)
		cv2.imshow("Detected", imcontours4)
		cv2.waitKey(0)
	# print(Charssss)
	# # for c in Charssss:
	# # 	print(c)
	# Charssss = ''.join(Charssss)
	# return Charssss


###			CHECK HOP -> REMOVE KY TU TRUNG -> DETECT -> SX LAI
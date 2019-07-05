import cv2
import math

class char:
	def __init__(self, ct):
		self.contour = ct
		x, y, w, h = cv2.boundingRect(self.contour)
		self.x = x
		self.y = y
		self.w = w
		self.h = h

		self.Area = w * h

		self.centerX = x + w/2
		self.centerY = y + h/2

		# self.Diagonal = math.sqrt(w ** 2 + h ** 2)

		self.Ratio = w/h
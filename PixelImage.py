import os
import cv2
import numpy as np
from pathlib import Path
from tkinter import filedialog
import pickle as pck
from math import sqrt
import csv

RGBMatTemp = (
	("Blanc", [255,255,255]),
    ("Orange", [225, 101, 54]),
    ("Rouge", [208, 46, 73]),
    ("Jaune", [224, 209, 78]),
    ("Mauve", [171, 147, 207]),
    ("Rose", [222, 120, 182]),
    ("Cyan", [119, 200, 227]),
    ("Lime", [141, 196, 102]),
    ("Marron", [133, 77, 76])
)


class PixelImage:
	def __init__(self, img_path=None, pixel_size=(20, 20)):
		self.img_path = img_path
		self.pixel_size = pixel_size
		self.img = None
		self.output = None
		if self.img_path is None:
			self.img_path = filedialog.askopenfile(title="Selectionnez votre image :", filetypes=[("Image","*.png"),("Image","*.jpg")]).name

	def load_image(self):
		self.img = cv2.imread(self.img_path)

	def save_output(self, output_path):
		if self.output is not None:
			cv2.imwrite(str(output_path), self.output)
		else:
			raise ValueError("Output image not generated yet.")

	def display_images(self):
		if self.output is not None:
			cv2.imshow('Input', self.img)
			cv2.imshow('Output', self.output)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
		else:
			raise ValueError("Output image not generated yet.")
		
	def pixelisation(self, show = False, out = False) -> list:
		'''
		Pixelise the image, return a list of list of RGB values.
		If show is True, display the input and output images.
		If out is True, save the output image as "test_pixelated.jpg".

		TO DO : add a parameter to choose the output path and name.
		'''
		height, width = self.img.shape[:2]
		w, h = self.pixel_size

		temp = cv2.resize(self.img, (w, h), interpolation=cv2.INTER_LINEAR)

		OutVisu = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)

		OutUtil = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)

		if show:
			cv2.imshow('Input', self.img)
			cv2.imshow('Output', OutVisu)

		if out : cv2.imwrite("test_pixelated.jpg", OutVisu)

		ImageMat = open('ImageMat.txt', 'wb')
		pck.dump(OutUtil.tolist(),ImageMat)

		OutVisu.tolist()
		return OutUtil.tolist()
	
	def nearest_colour_v2(self, subjects, query):
		min_distance = float('inf')
		closest_colour = None
		
		for colour in subjects:
			distance = sum((colour[i] - query[i]) ** 2 for i in range(3))

			if distance < min_distance:
				min_distance = distance
				closest_colour = colour
		return closest_colour
	
	def load_smarties_colours(self):
		rgb_smarties = [colour[1] for colour in RGBMatTemp]
		return rgb_smarties

	def RGB2Smarties_v2(self, RGBMat: list) -> np.ndarray:
		rgb_smarties = self.load_smarties_colours()
		if not rgb_smarties:
			raise ValueError("Aucune couleur smarties chargée")
		smarties_matrix = []
		for row in RGBMat:
			smarties_row = []
			for pixel in row:
				closest = self.nearest_colour_v2(rgb_smarties, pixel)
				smarties_row.append(closest)
			smarties_matrix.append(smarties_row)

		return np.array(smarties_matrix, dtype=np.uint8)


if True :
	poubelle = PixelImage(img_path="image/dep.jpg", pixel_size=(20,20))
	poubelle.load_image()
	Mat = poubelle.pixelisation()
	smartiesImage = poubelle.RGB2Smarties_v2(Mat)
	print("Shape de l'image Smarties:", smartiesImage.shape)
	print("Type:", smartiesImage.dtype)
	
	cv2.imshow('i', smartiesImage)


cv2.waitKey(0)
cv2.destroyAllWindows()
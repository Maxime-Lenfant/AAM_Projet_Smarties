import os
import cv2
import numpy as np
from pathlib import Path
from tkinter import filedialog
import pickle as pck
from math import sqrt
import csv

RGBMatTemp = (
    ("Orange", [225, 101, 54]),
    ("Rouge", [208, 46, 73]),
    ("Jaune", [224, 209, 78]),
    ("Mauve", [171, 147, 207]),
    ("Rose", [222, 120, 182]),
    ("Cyan", [119, 200, 227]),
    ("Lime", [141, 196, 102]),
    ("Marron", [133, 77, 76])
)

RGBMatTemp = (
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

	def nearest_colour(self, subjects, query ):
		'''
		Find the nearest colour in subjects to the query colour.
		'''
		indice = 100000
		for CouleurSmarties in subjects :
			s = 0
			for i in range(3):
				s += (CouleurSmarties[1][i] - query[i])**2
			if indice > s :
				indice = s
				top = CouleurSmarties
			#indice = min( subjects, key = lambda subject: sum( (s[1] - q) ** 2 for s, q in zip( tuple(CouleurSmarties), tuple(query) ) ) )
		return CouleurSmarties
	
	def RGB2Smarties(self, RGBMat:list) ->list :
		#Ouverture du fichier contenant les couleurs des smarties vers une liste
		RGB_Smart_Mat = [] # Matrice des couleurs des Smarties en RGB	
		Smarties_Mat_Select = [] # Matrice des smarties selectionnés
		with open('couleurs.csv', newline='') as csvCoul :
			reader = csv.reader(csvCoul, delimiter=';')
			for row in reader :
				RGB_Smart_Mat.append(RGBMatTemp[1])
			#RGB_Smart_Mat = tuple(RGB_Smart_Mat)

		#Conversion en cherchant la couleur de smarties la plus proche.
		tempROW = []
		for row in RGBMat:
			for pixel in row:
				tempROW.append(self.nearest_colour(RGB_Smart_Mat, pixel))
			Smarties_Mat_Select.append(tempROW)
			tempROW = []
		return Smarties_Mat_Select


if True :
	poubelle = PixelImage(img_path="image/tilted.png")
	poubelle.load_image()
	Mat = poubelle.pixelisation()
	for i in range(len(Mat)):
		print(Mat[i])
		for j in range(len(Mat[i])):
			if j >19 :
				Mat[i].pop(i)

	hexMat = poubelle.RGB2Smarties(Mat)
	for i in range(len(hexMat)):
		print(hexMat[i])
	gen = np.array(hexMat,dtype=np.uint16)
	cv2.imshow('i',gen)


cv2.waitKey(0)
cv2.destroyAllWindows()
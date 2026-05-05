import os
import cv2
import numpy as np
from pathlib import Path
from tkinter import filedialog
import pickle as pck

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
		
	def pixelisation(self):
		height, width = self.img.shape[:2]
		w, h = (15, 15)
		temp = cv2.resize(self.img, (w, h), interpolation=cv2.INTER_LINEAR)

		output = cv2.resize(temp, (width, height), interpolation=cv2.INTER_NEAREST)

		output2 = cv2.resize(temp, (w, h), interpolation=cv2.INTER_NEAREST)

		cv2.imshow('Input', self.img)
		cv2.imshow('Output', output)
		#cv2.imwrite("test_pixelated.jpg", output)
		ImageMat = open('ImageMat.txt', 'wb')
		pck.dump(output2.tolist(),ImageMat)

		output.tolist()
		cv2.waitKey(0)
		cv2.destroyAllWindows()


poubelle = PixelImage(img_path="image/tilted.png")
poubelle.load_image()
poubelle.pixelisation()

from PIL import Image, ImageDraw, ImageOps
from natsort import natsorted
from libxmp import XMPFiles, consts
import numpy as np
from skimage.io import imread
import ast
import tifffile
import json
import os

class Cleaner():

	def crop_array(img_arr):
		"""
		Crops image removing white pixels

		Parameters
		----------
		img_arr : Image
			image
		"""

		y1, x1 = np.nonzero(img_arr[:int(img_arr.shape[0]/2), :int(img_arr.shape[1]/2)]<255)
		y2, x2 = np.nonzero(img_arr[int(img_arr.shape[0]/2):, int(img_arr.shape[1]/2):]<255)

		y1m = min(y1)
		x1m = min(x1)
		y2m = int(img_arr.shape[1]/2)+max(y2)
		x2m = int(img_arr.shape[0]/2)+max(x2)

		return img_arr[y1m:y2m+1, x1m:x2m+1]

	def threshold_array(img_array, thresholds=[255, 250, 90, 75], values=[255, 200, 75, 0]):
		"""
		Thresholds the image

		Parameters
		----------
		img_array : Image
			image
		thresholds : list
			thresholds to apply
		values : list
			values to transform into
		"""

		arr_t = np.zeros_like(img_array)

		for t, v in zip(thresholds, values):
			arr_t = np.where(img_array <= t, v, arr_t)

		return img_array

	def remove_unreliable_pixels_array(img_array, px=0):
		"""
		Removes unreliable pixels from image

		Parameters
		----------
		img_array : Image
			image
		px : int
			pixels to remove
		"""

		h, w = img_array.shape
		img = Image.fromarray(img_array)

		alpha = Image.new('L', img_array.shape, 0)
		draw = ImageDraw.Draw(alpha)
		draw.pieslice([px, px, w-px, h-px], 0, 360, fill=255)
		alpha = ImageOps.invert(alpha)

		img.paste(alpha, (0, 0), alpha)

		return np.array(img)

	def clean_array(self, img_array, px=0):

		img_array = Cleaner.crop_array(img_array)
		img_array = Cleaner.remove_unreliable_pixels_array(img_array, px)
		img_array = Cleaner.threshold_array(img_array)

		return img_array
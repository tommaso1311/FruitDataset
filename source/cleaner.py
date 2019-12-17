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

		img_arr = np.array(img_arr)

		y1, x1 = np.nonzero(img_arr[:int(img_arr.shape[0]/2), :int(img_arr.shape[1]/2)]<255)
		y2, x2 = np.nonzero(img_arr[int(img_arr.shape[0]/2):, int(img_arr.shape[1]/2):]<255)

		y1m = min(y1)
		x1m = min(x1)
		y2m = int(img_arr.shape[1]/2)+max(y2)
		x2m = int(img_arr.shape[0]/2)+max(x2)

		return img_arr[y1m:y2m+1, x1m:x2m+1]

	def threshold_array(img_arr, thresholds=[255, 250, 90, 75], values=[255, 200, 75, 0]):
		"""
		Thresholds the image

		Parameters
		----------
		img_arr : Image
			image
		thresholds : list
			thresholds to apply
		values : list
			values to transform into
		"""

		img_arr = np.array(img_arr)

		arr_t = np.zeros_like(img_arr)

		for t, v in zip(thresholds, values):
			arr_t = np.where(img_arr <= t, v, arr_t)

		return img_arr

	def remove_unreliable_pixels_array(img_arr, px=0):
		"""
		Removes unreliable pixels from image

		Parameters
		----------
		img_arr : Image
			image
		px : int
			pixels to remove
		"""

		img_arr = np.array(img_arr)

		h, w = img_arr.shape
		img = Image.fromarray(img_arr)

		alpha = Image.new('L', img_arr.shape, 0)
		draw = ImageDraw.Draw(alpha)
		draw.pieslice([px, px, w-px, h-px], 0, 360, fill=255)
		alpha = ImageOps.invert(alpha)

		img.paste(alpha, (0, 0), alpha)

		return np.array(img)

	def clean_array(self, img_arr, px=0):

		img_arr = Cleaner.crop_array(img_arr)
		img_arr = Cleaner.remove_unreliable_pixels_array(img_arr, px)
		img_arr = Cleaner.threshold_array(img_arr)

		return img_arr

	def clean(px=0, load_path="dataset/generated/", save_path="dataset/cleaned/",
		answers_path="dataset/answers/"):
		"""
		Cleans the images previously generated

		Parameters
		----------
		img : Image
			image
		load_path : string
			loading path
		save_path : string
			saving path
		"""

		png_list = [file for file in os.listdir(load_path) if file.endswith(".png")]
		txt_list = [file for file in os.listdir(load_path) if file.endswith(".txt")]

		for file in png_list:

			img = Image.open(load_path+file).convert('L')

			img = Cleaner.crop_array(img)
			img = Cleaner.remove_unreliable_pixels_array(img, px)
			img = Cleaner.threshold_array(img)

			img = Image.fromarray(img)

			try:
				img.save(save_path+file)
			except:
				os.mkdir(save_path)
				img.save(save_path+file)

		for file in txt_list:
			try:
				os.rename(load_path+file, answers_path+file)
			except:
				os.mkdir(answers_path)
				os.rename(load_path+file, answers_path+file)

	def merge(index=0, images_path="dataset/cleaned/", answers_path="dataset/answers/",
				final_path="dataset/dataset/"):
		"""
		Merge images and answers in a single tiff file

		Parameters
		----------
		images_path : string
			path of cleaned images
		answers_path : string
			path of answers
		final_path : string
			final saving path
		"""

		imgs_names = natsorted([file for file in os.listdir(images_path) if (file.endswith(".png") and int(file.split("_")[0])==index)])
		answers_names = natsorted([file for file in os.listdir(answers_path) if (file.endswith(".txt") and int(file.split("_")[0])==index)])
		
		imgs = []
		for name in imgs_names:
			img = imread(images_path+name, as_gray=True)
			imgs.append(img)
		answers = [[int(line) for line in open(answers_path+name) if int(line)] for name in answers_names]

		arr = np.array(imgs)

		try:
			tifffile.imsave(final_path+"{0}.tiff".format(index), arr)
		except:
			os.mkdir(final_path)
			tifffile.imsave(final_path+"{0}.tiff".format(index), arr)

		xmpfile = XMPFiles(file_path=final_path+"{0}.tiff".format(index), open_forupdate=True)

		xmp = xmpfile.get_xmp()
		xmp.set_property(consts.XMP_NS_DC, "description[1]", str(answers))
		xmpfile.put_xmp(xmp)
		xmpfile.close_file()

if __name__ == "__main__":
	print("This is a package not a program.")
from math import pi, sqrt, cos, sin
from source.utils import rotation_ll
import numpy as np

class SphericalFruit():
	"""docstring for SphericalFruit"""

	def __init__(self, index=0, n_pixels=200000, colors=['darkseagreen','saddlebrown']):

		self.index = index
		self.n_pixels = n_pixels
		self.colors = colors

		self.n_defects = 0

		self.pixels_coordinates = SphericalFruit.generate_pixels_coordinates(n_pixels)
		self.pixels_values = np.array([0]*n_pixels, dtype=int)
		self.pixels_cluster = np.array([0]*n_pixels, dtype=int)

	def generate_pixels_coordinates(n_pixels):

		points = []
		offset = 2/n_pixels
		increment = pi * (3 - sqrt(5))

		for i in range(n_pixels):

			y = ((i * offset)-1)+(offset/2)
			r = sqrt(1-y*y)

			phi = (i%n_pixels)*increment

			x = cos(phi)*r
			z = sin(phi)*r

			coordinates = [v for v in [x, y, z]]
			coordinates.append(1)
			points.append(coordinates)

		return np.array(points)

	def rotate_pixels_ll(self, lon_angle, lat_angle):

		point = np.array([0, 0, 0])
		points = rotation_ll(self.pixels_coordinates, point, lon_angle, lat_angle)
		return points
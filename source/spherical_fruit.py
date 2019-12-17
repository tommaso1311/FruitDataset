from math import pi, sqrt, cos, sin
from source.utils import rotation_ll
from source.cleaner import Cleaner
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors
from skimage import color
import os

class SphericalFruit():

	def __init__(self, index=0, n_pixels=200000, colors=['darkseagreen','saddlebrown']):

		self.index = index
		self.n_pixels = n_pixels
		self.colors = colors

		self.n_defects = 0

		self.pixels_coordinates = SphericalFruit.generate_pixels_coordinates(n_pixels)
		self.pixels_values = np.array([0]*n_pixels, dtype=int)
		self.pixels_cluster = np.array([0]*n_pixels, dtype=int)

		self.cleaner = Cleaner()

	def generate_pixels_coordinates(n_pixels):
		"""
		Create the image pixels by generating random points over a sphere

		Parameters
		----------
		samples : int
			number of points

		Returns
		-------
		points : array
			array of points coordinates
		"""

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
		"""
		Rotates the pixels of a certain longitude and latitude angle

		Parameters
		----------
		lon_angle : float
			longitude angle
		lat_angle : float
			latitude angle

		Returns
		-------
		points : array
			rotated pixels
		"""

		point = np.array([0, 0, 0])
		points = rotation_ll(self.pixels_coordinates, point, lon_angle, lat_angle)
		return points

	def generate_defects_coordinates(self, min_defects, max_defects):
		"""
		Get the random defects coordinates

		Parameters
		----------
		min_defects : int
			minimum number of defects
		max_defects : int
			maximum number of defects

		Returns
		-------
		defects_coordinates : array
			array of defects coordinates
		"""

		n_defects = np.random.randint(min_defects, max_defects)
		idx = np.random.choice(self.pixels_coordinates.shape[0], n_defects, replace=False)
		defects_coordinates = self.pixels_coordinates[idx, :]
		return defects_coordinates

	def add_defects(self, defect_type=1, min_defects=1, max_defects=5):
		"""
		Add random defects to the fruit

		Parameters
		----------
		defect_type : int
			type of the defect
		min_defects : int
			minimum number of defects
		max_defects : int
			maximum number of defects
		"""

		defects_coordinates = self.generate_defects_coordinates(min_defects, max_defects)

		for defect in defects_coordinates:

			self.n_defects += 1

			defects_distances = np.linalg.norm(defects_coordinates-defect, axis=1)
			points_distances = np.linalg.norm(self.pixels_coordinates-defect, axis=1)

			max_radius = np.min(defects_distances[np.nonzero(defects_distances)])/2 if (len(defects_distances)>1) else 0.3
			radius = np.random.random()*max_radius
			mask = points_distances < radius

			self.pixels_values[mask] = defect_type
			self.pixels_cluster[mask] = self.n_defects

	def generate_defects(self, defects_list=[(1, 2)]):

		for defect_type, min_max in enumerate(defects_list, 1):
			self.add_defects(defect_type, min_max[0], min_max[1])

	def plot3d(self, save=False, axis=True):
		"""
		Plots the fruit in a 3d ambient

		Parameters
		----------
		save : bool
			saving the fruit
		axis : bool
			plot with axis
		"""

		fig = plt.figure(figsize=(4,4))
		ax = plt.axes(projection='3d')

		for i, c in enumerate(self.colors):
			mask = np.where(self.pixels_values==i)
			ax.scatter3D(self.pixels_coordinates[mask][:,0], self.pixels_coordinates[mask][:,1],
						self.pixels_coordinates[mask][:,2], color=c)

		if axis:
			ax.set_xlabel('X axis')
			ax.set_ylabel('Y axis')
			ax.set_zlabel('Z axis')
		else:
			plt.axis('off')

		ax.view_init(45, -135)

		if save:
			plt.savefig("img3d.png")
		else:
			plt.show()

		plt.close()

	def plot2d(self, n=0, size=(4,4), pov=(0, 0), save=False,
				save_path="dataset/generated/", save_defects=False):
		"""
		Plots a projection of the fruit

		Parameters
		----------
		size : tuple
			image size
		pov : tuple
			angles of point of view of the projection
		save : bool
			saving the fruit
		save_path : string
			save path
		save_defects : bool
			save defects
		"""

		fig, ax = plt.subplots(figsize=size)

		rotated_pixels_coordinates = self.rotate_pixels_ll(pov[0], pov[1])

		mask = rotated_pixels_coordinates[:, 2]<0
		projected_pixels_coordinates = rotated_pixels_coordinates[mask]
		projected_pixels_values = self.pixels_values[mask]
		projected_pixels_cluster = self.pixels_cluster[mask]

		if save_defects:
			clusters = np.unique(projected_pixels_cluster)
			try:
				np.savetxt(save_path+"{0}_{1}.txt".format(self.index, n), clusters, "%d")
			except:
				os.mkdir(save_path)
				np.savetxt(save_path+"{0}_{1}.txt".format(self.index, n), clusters, "%d")

		for i, c in enumerate(self.colors):
			mask = np.where(projected_pixels_values==i)
			ax.scatter(projected_pixels_coordinates[mask][:,0],
						projected_pixels_coordinates[mask][:,1], color=c, marker='.')

		plt.axis('off')
		plt.gca().invert_yaxis()
		plt.margins(0,0)

		if save:
			try:
				plt.savefig(save_path+"{0}_{1}.png".format(self.index, n),
						pad_inches=0, bbox_inches='tight')
			except:
				os.mkdir(save_path)
				plt.savefig(save_path+"{0}_{1}.png".format(self.index, n),
						pad_inches=0, bbox_inches='tight')

		else:
			plt.show()

		plt.close()

	def plot_complete_rotation(self, step=5, **kwargs):
		"""
		Used to plot a complete view of the fruit

		Parameters
		----------
		step : int
			step of the point of view
		"""

		for angle in range(0, 360, step):
			self.plot2d(n=angle, pov=(angle, 0), save=True, **kwargs)

	def save_shots(self, shots=5, physics="random", angle=None,
					save_path="dataset/generated/", **kwargs):
		"""
		Used to save shots of the fruit

		Parameters
		----------
		shots : int
			number of shots
		physics : string
			type of rotation
		angle : tuple
			angles of the fruit rotation
		save_path : string
			saving path
		"""

		lon_angle, lat_angle = (0, 0)

		for i in range(shots):

			if physics == "random":
				lon_angle = np.random.randint(0, 360)
				lat_angle = np.random.randint(-90, 90)

			elif physics == "rolling":
				lon_angle = lon_angle + np.random.randint(-15, 45)
				# lat_angle = lat_angle + np.random.randint(-10, 10)

			elif physics == "custom":
				lon_angle = angle[0][i]
				lat_angle = angle[1][i]

			self.plot2d(n=i, pov=(lon_angle, lat_angle), save=True, save_path=save_path,
						save_defects=True, **kwargs)

	def generate_shot_online(self, size, pov):

		fig, ax = plt.subplots(figsize=size)

		rotated_pixels_coordinates = self.rotate_pixels_ll(pov[0], pov[1])

		mask = rotated_pixels_coordinates[:, 2]<0
		projected_pixels_coordinates = rotated_pixels_coordinates[mask]
		projected_pixels_values = self.pixels_values[mask]
		projected_pixels_cluster = self.pixels_cluster[mask]

		clusters = np.unique(projected_pixels_cluster).tolist()

		for i, c in enumerate(self.colors):
			mask = np.where(projected_pixels_values==i)
			ax.scatter(projected_pixels_coordinates[mask][:,0],
						projected_pixels_coordinates[mask][:,1], color=c, marker='.')

		plt.axis('off')
		plt.gca().invert_yaxis()
		plt.margins(0,0)

		fig.canvas.draw()

		fig_array = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
		fig_array = fig_array.reshape(fig.canvas.get_width_height()[::-1] + (3,))

		fig_array = color.rgb2gray(fig_array)*255

		fig_array = self.cleaner.clean_array(fig_array)

		return fig_array, clusters

	def generate_shots_online(self, n_shots, size=(4, 4), lon_angle_rot=(0, 1), lat_angle_rot=(0, 1)):

		lon_angle, lat_angle = (0, 0)

		shots_arr = []
		clusters_list = []

		for _ in range(n_shots):
			lon_angle += np.random.randint(lon_angle_rot[0], lon_angle_rot[1])
			lat_angle += np.random.randint(lat_angle_rot[0], lat_angle_rot[1])
			current_shot, clusters_shot = self.generate_shot_online(size, (lon_angle, lat_angle))

			shots_arr.append(current_shot)
			clusters_list.append(clusters_shot)

		return np.array(shots_arr), clusters_list

if __name__ == "__main__":
	print("This is a package not a program.")
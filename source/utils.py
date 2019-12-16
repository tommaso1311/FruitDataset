from math import cos, sin, radians
import numpy as np

def create_rotation_matrix(point, axis, angle):

	angle = radians(angle)
	c = cos(angle)
	s = sin(angle)
	u0, u1, u2 = axis

	translation_matrix1 = np.eye(4)
	translation_matrix1[:3, 3] = -point

	rotation_matrix = np.array([[c+u0*u0*(1-c), u0*u1*(1-c)-u2*s, u0*u2*(1-c)+u1*s, 0],
								[u1*u0*(1-c)+u2*s, c+u1*u1*(1-c), u1*u2*(1-c)-u0*s, 0],
								[u2*u0*(1-c)-u1*s, u2*u1*(1-c)+u0*s, c+u2*u2*(1-c), 0],
								[0, 0, 0, 1]])

	translation_matrix2 = np.eye(4)
	translation_matrix2[:3, 3] = point

	trasformation_matrix = rotation_matrix@translation_matrix1
	trasformation_matrix = translation_matrix2@trasformation_matrix

	return trasformation_matrix

def rotation_ll(points_matrix, point, lon_angle, lat_angle):

	axis1 = np.array([0, 1, 0])
	axis2 = np.array([1, 0, 0])

	rotation_matrix1 = create_rotation_matrix(point, axis1, lon_angle)
	rotation_matrix2 = create_rotation_matrix(point, axis2, lat_angle)
	rotation_matrix = rotation_matrix2@rotation_matrix1

	points_matrix = rotation_matrix@points_matrix.T

	return points_matrix.T
from source.spherical_fruit import SphericalFruit
import matplotlib.pyplot as plt

fruit = SphericalFruit()
fruit.generate_defects([(2, 3)])

arr, answers = fruit.generate_shots_online(6, lon_angle_rot=(40, 60))

print(arr.shape, answers)

for img in arr:
	fig, ax = plt.subplots(figsize=(4, 4))
	plt.imshow(img, cmap='gray', vmin=0, vmax=255)
	plt.show()
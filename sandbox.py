from source.spherical_fruit import SphericalFruit
import matplotlib.pyplot as plt

fruit = SphericalFruit()
# fruit.rotate_pixels_ll(5, 5)
fruit.generate_defects([(5, 10)])

arr, clusters = fruit.temp()

print(arr.shape, clusters)

fig, ax = plt.subplots(figsize=(4, 4))
plt.imshow(arr)
plt.show()
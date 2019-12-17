from source.spherical_fruit import SphericalFruit
import matplotlib.pyplot as plt

fruit = SphericalFruit()
fruit.generate_defects([(5, 10)])

arr, answers = fruit.generate_shots(6)

print(arr.shape, answers)

# fig, ax = plt.subplots(figsize=(4, 4))
# plt.imshow(arr, cmap='gray', vmin=0, vmax=255)
# # plt.imshow(arr)
# plt.show()
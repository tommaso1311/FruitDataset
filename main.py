from source.spherical_fruit import SphericalFruit
from source.cleaner import Cleaner
from source.utils import create_gif

import multiprocessing as mp
import numpy as np

# n_procs = mp.cpu_count()
n_procs = 6

def create_fruit(index):

	np.random.seed()
	f = SphericalFruit(index)
	f.add_defects(min_defects=2, max_defects=3)
	f.save_shots(shots=6, physics="rolling")
	print("generated fruit", index)

def generate(starting_index, final_index):

	procs = []
	for i in range(starting_index, final_index):
		p = mp.Process(target=(create_fruit), args=(i,))
		p.start()
		procs.append(p)

	for p in procs:
		p.join()

def main():

	# saves the complete plot of a simple fruit with custom colors
	# f = SphericalFruit(colors=["sandybrown","saddlebrown", 'olive'])
	# f.add_defects(1, 5, 8)
	# f.add_defects(2, 3, 6)
	# f.plot_complete_rotation(save_path="dataset/complete/")
	# create_gif(save_path="dataset/", duration=0.04)

	# saves randomly generated fruits with default colors
	start = 0
	stop = 12
	for i in range(start, stop, n_procs):
		generate(i, i+n_procs)

	# cleans the generated fruit and saves them
	Cleaner.clean()
	for i in range(start, stop):
		Cleaner.merge(i)
	print("dataset created")

if __name__ == "__main__":
	main()
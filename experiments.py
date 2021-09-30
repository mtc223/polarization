import ardriver as ar
import nidriver as ni
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
import time

#Commands to be used
#ni.read()
#ar.turn(motor,angle)

#single motor experiment done with lambda/4, lambda/2, polarizer
def exp0():
	data = np.ndarray(shape=(360,1),dtype=float)
	for m0 in range(data.shape[0]):
		time.sleep(1.5)
		data[m0] = ni.read()
		ar.ser_turn(0,1)
		print(data[m0])
	return data

#double motor experiment
def exp1():
	data = np.array((360,360))
	for m0 in range(359):
		for m1 in range(359):
			#turn inner motor 1 degree
			ar.ser_turn(1,1)
			data[m0][m1] = ni.read();
		ar.turn(0,1)
	return data

def savedata(data, filename):
	file1 = open(filename,"w+")
	for line in data:
		file1.write(str(line[0]))
		file1.write("\n")
	file1.close()

def savedata2d(data, filename):
	file1 = open(filename,"w+")
	for line in data:
		for element in line:
			file1.write(element)
			file1.write(" ")
		file1.write("\n")
	file1.close()



def graphdata(data):
	# Set up grid and test data
	nx, ny = 360,360
	x = range(nx)
	y = range(ny)

	hf = plt.figure()
	ha = hf.add_subplot(111, projection='3d')

	X, Y = numpy.meshgrid(x, y)  # `plot_surface` expects `x` and `y` data to be 2D
	ha.plot_surface(X, Y, data)

	plt.show()

savedata(exp0(),"exp0_pol.txt")
#exp0_pt4 Experiment 0 Phase transition lambda/4
#exp0_pol Experiment 0 Polarization Filter
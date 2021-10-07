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
def exp0(filename):
	with open(filename,"w+") as writer:
		data = np.ndarray(shape=(360,1),dtype=float)
		for m0 in range(data.shape[0]):
			time.sleep(1.5)
			data[m0] = ni.read()
			ar.ser_turn(0,1)
			print(m0,data[m0])
			writer.write(str(data[m0]))
			writer.write("\n")
	return data

#double motor experiment
def exp1(filename):
	with open(filename,"w+") as writer:
		data = np.ndarray(shape=(72,72),dtype=float)
		for m0 in range(data.shape[0]):
			for m1 in range(data.shape[1]):
				data[m0][m1] = ni.read()
				print(m0,m1,data[m0][m1])
				writer.write(str(data[m0][m1]))
				writer.write("\n")
				time.sleep(1.5)
				ar.ser_turn(1,5)
			time.sleep(1.5)
			ar.ser_turn(0,5)	
	return data

def graphdata1(filename,title):
	with open(filename,"r+") as reader:
		Y = np.ndarray(shape=(360,1),dtype=float)
		for i in range(360):
			Y[i] = reader.readline()
		X = range(Y.shape[0])
		plt.scatter(X,Y)
		plt.title(title)
		plt.show()


def graphdata2(filename,title):
	with open(filename,"r+") as reader:
		Z = np.ndarray(shape=(72,72),dtype=float)
		for m0 in range(Z.shape[0]):
			for m1 in range(Z.shape[1]):
				Z[m0][m1] = float(reader.readline())
		X = np.outer(np.linspace(0, 360, 72), np.ones(72))
		Y = X.copy().T
		fig = plt.figure()
		ax = plt.axes(projection = '3d')
		ax.set_xlabel("Polarization Filter Angle")
		ax.set_ylabel("Lambda/4 Retarder Angle")
		ax.set_zlabel("Power (mW)")
		ax.plot_surface(X,Y,Z, cmap='viridis', edgecolor='green')
		ax.set_title(title)
		plt.show()

def graphdata21(filename,title):
	with open(filename,"r+") as reader:
		Z = np.ndarray(shape=(72,72),dtype=float)
		for m0 in range(Z.shape[0]):
			for m1 in range(Z.shape[1]):
				Z[m0][m1] = float(reader.readline())
	plt.scatter(X,Y)
	plt.title(title)
	plt.show()
	hf = plt.figure()
	ha = hf.add_subplot(111, projection='3d')

	X, Y = numpy.meshgrid(x, y)  # `plot_surface` expects `x` and `y` data to be 2D
	ha.plot_surface(X, Y, data)

	plt.show()

#exp0("exp0_pt4.txt") #Experiment 0 Phase transition lambda/4
#exp0("exp0_pol.txt") #Experiment 0 Polarization Filter
#exp1("exp1_pol4.txt") #Experiment 1 Two motors, Polarization and lambda/4
graphdata2("exp1_pol4.txt","Experiment 3 lambda/4 into Polarization Filter")
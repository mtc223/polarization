import serial

ser = serial.Serial("COM11",9600,timeout=1)

#Initialize the serial com
def ser_init(com):
	ser.port = com

#Returns the status of the ports
def ser_ports():
	ser.write(b'in')
	line = ser.readline()
	while (line==b''):
		line = ser.readline()
	return line.decode('ascii')

#Sets a certain pin to be in
def ser_in(pin):
	comm = f'in:{pin}'
	ser.write(comm.encode())

#Sets a certain pint to be out at a certain voltage
def ser_out(pin,volts):
	comm = f'out:{pin}:{volts}'
	ser.write(comm.encode())

#Turns a motor
def ser_turn(motor,angle):
	comm = f'turn:{motor}:{angle}'
	ser.write(comm.encode())

#Reads from arduino for a certain duration
def ser_read(duration):
	comm = f'read:{duration}'
	ser.write(comm.encode())
	line = ser.readline()
	while (line==b''):
		line = ser.readline()
	reading = line.decode('ascii')[:-2]
	data = ()
	line = ser.readline()
	while (not line==b''):
		data = data + (line.decode('ascii')[:-3].split(","),)
		line = ser.readline()
	return (reading, data)


def test(pin):
	test_data = ()
	x = range(0,200)
	for i in x:
		ser_out(pin,i)
		(read, data) = ser_read(50)
		for row in data:
			test_data = test_data + ((i, row[0], row[1]),)
	graph(test_data,(0,2))
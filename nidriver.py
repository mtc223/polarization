import pyvisa

rm = pyvisa.ResourceManager()
instrument = rm.open_resource(rm.list_resources()[-1])
	
def read():
	return instrument.query("D?")

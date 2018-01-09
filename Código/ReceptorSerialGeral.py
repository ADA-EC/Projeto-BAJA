import serial
from abc import ABC
from abc import abstractmethod


class ReceptorSerialGeral(ABC):

	def __init__(self, PORT, BaudRate):
		# configura a conexão serial
		# detalhes em "https://pythonhosted.org/pyserial/pyserial_api.html"
		ser = serial.Serial(
			port=PORT,
			baudrate=BaudRate,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS
		)
		print ('Foo method in class B')
		# abre a conexão serial
		#ser.open()
	
	def Leitura(self):
		pass

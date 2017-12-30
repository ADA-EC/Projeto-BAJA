import serial


class ReceptorSerialGeral(object):

	def __init__(self, PORT='COM6', BaudRate = 9600):
		# configura a conexão serial
		# detalhes em "https://pythonhosted.org/pyserial/pyserial_api.html"
		ser = serial.Serial(
			port=PORT,
			baudrate=BaudRate,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS
		)
		
		# abre a conexão serial
		ser.open()
	
	@abstractmethod	
	def Leitura(self):
		pass

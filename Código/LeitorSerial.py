from ReceptorSerialGeral import ReceptorSerialGeral

class LeitorSerial(ReceptorSerialGeral):
	
	def __init__(self, PORT='COM6', BaudRate = 9600):
		super().__init__(PORT,BaudRate)
	
	#Aqui deve ser retornado o dicionário com as leitura feitas
	def Leitura(self):
		pass
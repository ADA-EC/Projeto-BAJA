import serial
import pandas as pd
import numpy as np
from datetime import datetime
from time import sleep

class LeitorSerial():

	tstart = datetime.now()

	# cria o DataFrame com as colunas que serão preenchidas
	col_labels = ('Tempo',
          'Box',
          'Velocidade',
          'Rotacao',
          'Distribuicao',
          'Combustivel',
          'Posicao',
          'Choke')
	df = pd.DataFrame(columns=col_labels)

	def __init__(self, PORT='COM6', BaudRate = 9600):

		# atribui a tstart o tempo do sistema na criação do LeitorSerial
		tstart = datetime.now()

		"""
		# configura a conexão serial
		# detalhes em "https://pythonhosted.org/pyserial/pyserial_api.html"
		ser = serial.Serial(
			port=PORT,
			baudrate=BaudRate,
			parity=serial.PARITY_NONE,
			stopbits=serial.STOPBITS_ONE,
			bytesize=serial.EIGHTBITS
		)
		"""

		print ('Iniciou Leitor Serial')

		# abre a conexão serial
		#ser.open()

	#Aqui deve ser retornado o dicionário com as leitura feitas
	def Leitura(self):
		readings = [np.float(x) for x in self.LeituraAleatoria().split(';')[:-1]]
		time = (datetime.now()-self.tstart).total_seconds()
		readings.insert(0, time)
		self.df = self.df.append(dict(zip(self.col_labels, readings)), ignore_index=True)
		sleep(0.1)


	def LeituraAleatoria(self):
		l = [str(x) for x in np.random.randint(0, 100, size=7)]
		l += ['\n']
		return ';'.join(l)

	def salvar_excel(self, filename):
	    # Salvar
	    #global VELOCIDADE
	    #global ROTACAO
	    #global tempo
	    #global DISTRIBUICAO
	    #global COMBUSTIVEL
	    #global Kmrodados
	    #global POSICAO
	    #global TempoM2

		## por enquanto:
		filename = 'output.xlsx'

		writer = pd.ExcelWriter(filename)
		df_exc = self.df[['Velocidade', 'Rotacao', 'Tempo', 'Distribuicao', 'Combustivel', 'KmRodadosTotal', 'Posicao']]
		df_exc.to_excel(writer,'Sheet1')
		writer.save()

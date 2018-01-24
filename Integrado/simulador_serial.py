## Simulador de Leitura para o Projeto-Baja
## As leituras tem média de 1 segundo, com variações aleatorias
import serial
import time
import numpy as np

# Porta de entrada
PORT = '/dev/pts/4'

def LeituraAleatoria():
    l = [str(x) for x in np.random.randint(0, 100, size=7)]
    l += ['\n']
    return bytes(';'.join(l), 'utf-8')

ser = serial.Serial(PORT)

while True:
    # Pega uma amostra da Distribuicao Gamma,
    # com media=1
    wait_time = np.random.gamma(10,0.1)
    # Aguarda esse tempo em segundos (pode ser float)
    time.sleep(wait_time)
    # Escreve uma leitura aleatoria na porta serial
    line = LeituraAleatoria()
    print(line)
    ser.write(line)

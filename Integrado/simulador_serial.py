## Simulador de Leitura para o Projeto-Baja
## As leituras tem média de 1 segundo, com variações aleatorias
import serial
import time
import numpy as np
import sys

# Porta de entrada
PORT = None

if len(sys.argv) > 1:
    PORT = sys.argv[1]

def LeituraAleatoria():
    l = np.random.randint(0, 100, size=7)
    box_values = [0,0,0,0,48,48,49]
    l[0] = box_values[np.random.choice(len(box_values))]# BOX
    l[-1] %= 2 # choke is either 0 or 1
    l = [str(x) for x in l]
    l += ['\n']
    line = ';'.join(l)
    return bytes(line, 'utf-8')

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

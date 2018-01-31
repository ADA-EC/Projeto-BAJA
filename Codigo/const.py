## Porta serial a ser utilizada. Por exemplo, '/dev/ttyCOM6'
# Se outra porta serial for passada como parametro na execuçao do programa
# esta porta sera sobrescrita
SER_PORT = None

## Nome de cada campo que é recebido pelo receptor serial + tempo
SER_LABELS = ('Tempo',
          'Box',
          'Velocidade',
          'Rotacao',
          'Distribuicao',
          'Combustivel',
          'Posicao')

## Baud rate da porta serial
SER_BAUD_RATE = 9600

## Delay das animacoes do matplotlib em (ms)
# Pode-se aumentar esse tempo caso seja necessario melhorar o desempenho
PLOT_DELAY = 500 #(ms)

## Numero de pontos dos graficos (rolling window size)
# Deve ser grande o suficiente de maneira que:
#     PLOT_WIN*(1/PLOT_DELAY) > SAMPLE_RATE,   Em que SAMPLE_RATE é
#                                              a taxa de aquisicao de dados,
#             que eh um parametro externo, definida pelo dispositivo serial.
#
# Caso contrario, algumas amostras serao sempre puladas nos graficos.
PLOT_WIN = 15

## Tempo de responsividade das funcionalidades 'update' em (ms)
UPDATE_DELAY = 200 # (ms)

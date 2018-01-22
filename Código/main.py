from LeitorSerial import LeitorSerial
import pandas as pd
import numpy as np

# Porta de saida
PORT='/dev/pts/1'


#Aqui ficará a função que será chamada para executar os códigos do projeto
#Nela deve conter chamadas às funções de leitura, interpretação e depois exibição
def main():
    leitor = LeitorSerial(PORT=PORT)
    leitor.df['KmRodadosAtual'] = np.nan
    leitor.df['KmRodadosTotal'] = np.nan
    KmRodadosTotal = 0
    for i in range(5):
        leitor.Leitura()

        #Atribui a CHOKE o ultimo Choke registrado
        CHOKE = leitor.df.Choke.iloc[-1]
        if CHOKE == 1:
            print('preto')
            pass  #Tem que botar alguma coisa da interface em preto
        elif CHOKE ==0:
            print('vermelho')
            pass  #Tem que botar alguma coisa da interface em vermelho
        else:
            print('Other')
            print(CHOKE)

        #Trecho comentado até termos integração com frontend
        '''
        #Atribui a BotaoBOX o valor do Botão BOX
        BotaoBOX = pegar na interface

        #Atribui a BOX o ultimo Box registrado
        BOX = leitor.df.Box.iloc[-1]
        if BotaoBOX == 1:
            if BOX == 0 or BOX == 48:
                leitor.MandaUm() #Função ainda não implementada para transmitir '1' na porta serial
            elif BOX == 49:
                print('vermelho')
                pass  #Tem que botar alguma coisa da interface em vermelho
        elif BotaoBOX == 0:
            if BOX == 49:
                leitor.MandaZero() #Função ainda não implementada para transmitir '0' na porta serial
            elif BOX == 48:
                print('preto')
                pass  #Tem que botar alguma coisa da interface em preto
        '''

        # Calculo de distancia percorrida
        # Uma vez que é necessário o acesso aos dois últimos registros,
        # é preciso impedir que esse cálculo seja feito na primeira iteração
        if i==0:
            leitor.df.KmRodadosTotal.iloc[-1] = 0
        else:
            #Retorna a velocidade média em m/s
            VelMediaMPS = ((leitor.df.Velocidade.iloc[-1] + leitor.df.Velocidade.iloc[-2])/2)/3.6
            #Retorna os Km Rodados nesta iteração
            KmRodadosAtual = VelMediaMPS * (leitor.df.Tempo.iloc[-1] - leitor.df.Tempo.iloc[-2])/1000
            leitor.df.KmRodadosAtual.iloc[-1] = KmRodadosAtual
            #Soma os Km Rodados nesta iteração ao total
            KmRodadosTotal += KmRodadosAtual
            leitor.df.KmRodadosTotal.iloc[-1] = KmRodadosTotal



        '''
        Aqui deve ficar as partes da interface
        '''


    print(leitor.df)
    leitor.salvar_excel('output.xlsx')


#Chama a função main se o script for executado como main e não faz nada se for chamado por outro script
if __name__ == "__main__":
    main()

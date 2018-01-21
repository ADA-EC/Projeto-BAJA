from LeitorSerial import LeitorSerial
import Interpretadores
import pandas as pd


def salvar_excel(df):
    # Salvar
    #global VELOCIDADE
    #global ROTACAO
    #global tempo
    #global DISTRIBUICAO
    #global COMBUSTIVEL
    #global Kmrodados
    #global POSICAO
    #global TempoM2
    writer = pd.ExcelWriter('output.xlsx')
    df.to_excel(writer,'Sheet1')
    writer.save()
    


#Aqui ficará a função que será chamada para executar os códigos do projeto
#Nela deve conter chamadas às funções de leitura, interpretação e depois exibição
def main():
    leitor = LeitorSerial()
    for i in range(5):
        leitor.Leitura()
        
        #Atribui a CHOKE o ultimo Choke registrado
        CHOKE = leitor.df.Choke[len(leitor.df)-1]
        if CHOKE == 1:
            print('preto')
            pass  #Tem que botar alguma coisa da interface em preto
        elif CHOKE ==0:
            print('vermelho')
            pass  #Tem que botar alguma coisa da interface em vermelho
        else:
            print('Outra bosta')
            print(CHOKE)
        
        #Trecho comentado até termos integração com frontend
        ''' 
        #Atribui a BotaoBOX o valor do Botão BOX
        BotaoBOX = pegar na interface
        
        #Atribui a BOX o ultimo Box registrado
        BOX = leitor.df.Box[len(leitor.df)-1]
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
            KmRodadosTotal = 0
        else:
            #Calcula o index da ultima leitura (se garantirmos um i será substituído)
            IndexAtual = len(leitor.df)-1
            #Retorna a velocidade média em m/s
            VelMediaMPS = ((leitor.df.Velocidade[IndexAtual] + leitor.df.Velocidade[IndexAtual - 1])/2)/3.6
            #Retorna os Km Rodados nesta iteração
            KmRodadosAtual = VelMediaMPS * (leitor.df.Tempo[IndexAtual] - leitor.df.Tempo[IndexAtual-1])/1000
            #Soma os Km Rodados nesta iteração ao total
            KmRodadosTotal += KmRodadosAtual
        
        
        '''
        Aqui deve ficar as partes da interface
        '''
    
    
    print(leitor.df)
    

#Chama a função main se o script for executado como main e não faz nada se for chamado por outro script
if __name__ == "__main__":
    main()
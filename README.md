# Projeto BAJA
O Projeto BAJA consiste em uma interface criada para receber e exibir dados de telemetria do grupo EESC USP Baja SAE.
Foi feito em Python para ser alternativa leve à interface antiga do grupo, feita em MatLab.


# Escolha da porta serial
Pode-se informar uma porta serial na execução do programa:

```
python3 baja.py /dev/ttyCOM6
```

Caso uma porta serial não seja informada, uma janela de dialogo é aberta, perguntando a porta a ser utilizada. A porta serial padrão pode ser configurada modificando a constante SER_PORT no arquivo "const.py".


# Como rodar no Windows:

1) Instalar o [Anaconda](https://www.anaconda.com/download/)(versão para Python 3.6 ou versão mais recente de Python3):

2) Instalar tk/tcl (responsável pela GUI) e pyserial (responsável pela comunicação serial).
Para isso rodar o Anaconda, que abrirá um terminal. Nele rodar as seguintes linhas de comando:

```
conda install -c anaconda tk
conda install -c anaconda pyserial
```

3) No arquivo "baja.py" clicar com o botão direito e depois em "Abrir com", depois selecionar o arquivo "python.exe" dentro da pasta de instalação do Anaconda(para facilitar selecionar como padrão para arquivos .py)

4) Caso haja problemas de permissão, principalmente para a função de salvar ou acessar os PORTs do computador, rodar o programa como Administrador.



# Como rodar em Ubuntu(por terminal):


1) Instalar pip para Python3 (caso ja não tenha instalado). Usar linha de comando:
```
sudo apt-get install python3-pip
```

2) Instalar os pacotes de Python necessários para rodar o programa. Rodar as linhas de comando:
```
sudo pip3 install numpy
sudo pip3 install matplotlib
sudo pip3 install pandas
sudo pip3 install pyserial
```

3) Pelo terminal ir até a pasta com o script e rodar a linha de comando:
```
python3 baja.py
```

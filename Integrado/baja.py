import numpy as np
import sys
import serial
import pandas as pd

from datetime import datetime
from time import sleep

import matplotlib.backends.tkagg as tkagg
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backend_bases import key_press_handler
import matplotlib.pyplot as plt

from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk

try:
    import threading
except ImportError:
    import dummy_threading as threading


# Endereco do PORT de entrada. i.e. /dev/ttyCOM6
# Se PORT for None, faz leituras aleatorias.
PORT = None

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

    def __init__(self, port='COM6', BaudRate = 9600):
		# atribui a tstart o tempo do sistema na criação do LeitorSerial
        self.tstart = datetime.now()

        if PORT is not None:
            # configura a conexão serial
            # detalhes em "https://pythonhosted.org/pyserial/pyserial_api.html"
            self.ser = serial.Serial(
            port=port,
            baudrate=BaudRate,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS)
            # abre a conexão serial
            ser.open()
        print('[Leitor Serial iniciado]')

    def Leitura(self):
        line = str(self.ser.readline(),'utf-8')
        readings = [np.float(x) for x in line.split(';')[:-1]]
        time = (datetime.now()-self.tstart).total_seconds()
        readings.insert(0, time)
        self.df = self.df.append(dict(zip(self.col_labels, readings)), ignore_index=True)


    def LeituraAleatoria(self):
        l = [str(x) for x in np.random.randint(0, 100, size=7)]
        l += ['\n']
        line = ';'.join(l)
        readings = [np.float(x) for x in line.split(';')[:-1]]
        time = (datetime.now()-self.tstart).total_seconds()
        readings.insert(0, time)
        self.df = self.df.append(dict(zip(self.col_labels, readings)), ignore_index=True)

    def SalvarExcel(self, filename='output.xlsx'):
        writer = pd.ExcelWriter(filename)
        df_exc = self.df[['Tempo','Velocidade', 'Rotacao', 'Distribuicao', 'Combustivel', 'KmRodadosTotal', 'Posicao']]
        df_exc.to_excel(writer,'Sheet1')
        writer.close()
        print(self.df)


class Frontend:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#d9d9d9' # X11 color: 'gray85'
        font20 = "-family {Segoe UI} -size 24 -weight bold -slant "  \
            "roman -underline 0 -overstrike 0"
        font21 = "-family {Segoe UI} -size 17 -weight normal -slant "  \
            "roman -underline 0 -overstrike 0"
        font24 = "-family {Segoe UI} -size 18 -weight normal -slant "  \
            "roman -underline 0 -overstrike 0"

        top.geometry("1366x705+112+149")
        top.title("Telemetria EESC USP BAJA")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

        # make sure widget instances are deleted
        top.protocol("WM_DELETE_WINDOW", on_close)

        self.Canvas1 = Canvas(top)
        self.Canvas1.place(relx=0.02, rely=0.11, relheight=0.46, relwidth=0.31)
        self.Canvas1.configure(background="white")
        self.Canvas1.configure(borderwidth="2")
        self.Canvas1.configure(highlightbackground="#d9d9d9")
        self.Canvas1.configure(highlightcolor="black")
        self.Canvas1.configure(insertbackground="black")
        self.Canvas1.configure(relief=RIDGE)
        self.Canvas1.configure(selectbackground="#c4c4c4")
        self.Canvas1.configure(selectforeground="black")
        self.Canvas1.configure(width=378)

        self.Canvas2 = Canvas(top)
        self.Canvas2.place(relx=0.34, rely=0.11, relheight=0.46, relwidth=0.31)
        self.Canvas2.configure(background="white")
        self.Canvas2.configure(borderwidth="2")
        self.Canvas2.configure(highlightbackground="#d9d9d9")
        self.Canvas2.configure(highlightcolor="black")
        self.Canvas2.configure(insertbackground="black")
        self.Canvas2.configure(relief=RIDGE)
        self.Canvas2.configure(selectbackground="#c4c4c4")
        self.Canvas2.configure(selectforeground="black")
        self.Canvas2.configure(width=378)

        self.Canvas3 = Canvas(top)
        self.Canvas3.place(relx=0.66, rely=0.11, relheight=0.46, relwidth=0.31)
        self.Canvas3.configure(background="white")
        self.Canvas3.configure(borderwidth="2")
        self.Canvas3.configure(highlightbackground="#d9d9d9")
        self.Canvas3.configure(highlightcolor="black")
        self.Canvas3.configure(insertbackground="black")
        self.Canvas3.configure(relief=RIDGE)
        self.Canvas3.configure(selectbackground="#c4c4c4")
        self.Canvas3.configure(selectforeground="black")
        self.Canvas3.configure(width=378)

        self.Label2 = Label(top)
        self.Label2.place(relx=0.03, rely=0.68, height=57, width=191)
        self.Label2.configure(activebackground="#f9f9f9")
        self.Label2.configure(activeforeground="black")
        self.Label2.configure(background="#d9d9d9")
        self.Label2.configure(disabledforeground="#a3a3a3")
        self.Label2.configure(font=font21)
        self.Label2.configure(foreground="#000000")
        self.Label2.configure(highlightbackground="#d9d9d9")
        self.Label2.configure(highlightcolor="black")
        self.Label2.configure(relief=RIDGE)
        self.Label2.configure(text='''0''')

        self.Label3 = Label(top)
        self.Label3.place(relx=0.19, rely=0.68, height=57, width=191)
        self.Label3.configure(activebackground="#f9f9f9")
        self.Label3.configure(activeforeground="black")
        self.Label3.configure(background="#d9d9d9")
        self.Label3.configure(disabledforeground="#a3a3a3")
        self.Label3.configure(font=font21)
        self.Label3.configure(foreground="#000000")
        self.Label3.configure(highlightbackground="#d9d9d9")
        self.Label3.configure(highlightcolor="black")
        self.Label3.configure(relief=RIDGE)
        self.Label3.configure(text='''0''')

        self.Label4 = Label(top)
        self.Label4.place(relx=0.35, rely=0.68, height=57, width=191)
        self.Label4.configure(activebackground="#f9f9f9")
        self.Label4.configure(activeforeground="black")
        self.Label4.configure(background="#d9d9d9")
        self.Label4.configure(disabledforeground="#a3a3a3")
        self.Label4.configure(font=font21)
        self.Label4.configure(foreground="#000000")
        self.Label4.configure(highlightbackground="#d9d9d9")
        self.Label4.configure(highlightcolor="black")
        self.Label4.configure(relief=RIDGE)
        self.Label4.configure(text='''0''')

        self.Label5 = Label(top)
        self.Label5.place(relx=0.51, rely=0.68, height=57, width=191)
        self.Label5.configure(activebackground="#f9f9f9")
        self.Label5.configure(activeforeground="black")
        self.Label5.configure(background="#d9d9d9")
        self.Label5.configure(disabledforeground="#a3a3a3")
        self.Label5.configure(font=font21)
        self.Label5.configure(foreground="#000000")
        self.Label5.configure(highlightbackground="#d9d9d9")
        self.Label5.configure(highlightcolor="black")
        self.Label5.configure(relief=RIDGE)
        self.Label5.configure(text='''0''')

        self.Label6 = Label(top)
        self.Label6.place(relx=0.67, rely=0.68, height=57, width=191)
        self.Label6.configure(activebackground="#f9f9f9")
        self.Label6.configure(activeforeground="black")
        self.Label6.configure(background="#d9d9d9")
        self.Label6.configure(disabledforeground="#a3a3a3")
        self.Label6.configure(font=font21)
        self.Label6.configure(foreground="#000000")
        self.Label6.configure(highlightbackground="#d9d9d9")
        self.Label6.configure(highlightcolor="black")
        self.Label6.configure(relief=RIDGE)
        self.Label6.configure(text='''0''')

        self.Label7 = Label(top)
        self.Label7.place(relx=0.83, rely=0.68, height=57, width=191)
        self.Label7.configure(activebackground="#f9f9f9")
        self.Label7.configure(activeforeground="black")
        self.Label7.configure(background="#d9d9d9")
        self.Label7.configure(disabledforeground="#a3a3a3")
        self.Label7.configure(font=font21)
        self.Label7.configure(foreground="#000000")
        self.Label7.configure(highlightbackground="#d9d9d9")
        self.Label7.configure(highlightcolor="black")
        self.Label7.configure(relief=RIDGE)
        self.Label7.configure(text='''0''')

        self.Message2 = Message(top)
        self.Message2.place(relx=0.03, rely=0.6, relheight=0.07, relwidth=0.14)
        self.Message2.configure(background="#d9d9d9")
        self.Message2.configure(font=font24)
        self.Message2.configure(foreground="#000000")
        self.Message2.configure(highlightbackground="#d9d9d9")
        self.Message2.configure(highlightcolor="black")
        self.Message2.configure(text='''Distribuição''')
        self.Message2.configure(width=250)

        self.Message3 = Message(top)
        self.Message3.place(relx=0.18, rely=0.6, relheight=0.07, relwidth=0.16)
        self.Message3.configure(background="#d9d9d9")
        self.Message3.configure(font=font24)
        self.Message3.configure(foreground="#000000")
        self.Message3.configure(highlightbackground="#d9d9d9")
        self.Message3.configure(highlightcolor="black")
        self.Message3.configure(text='''Vel. Atual(Km/h)''')
        self.Message3.configure(width=250)

        self.Message4 = Message(top)
        self.Message4.place(relx=0.35, rely=0.6, relheight=0.07, relwidth=0.14)
        self.Message4.configure(background="#d9d9d9")
        self.Message4.configure(font=font24)
        self.Message4.configure(foreground="#000000")
        self.Message4.configure(highlightbackground="#d9d9d9")
        self.Message4.configure(highlightcolor="black")
        self.Message4.configure(text='''Km Rodados''')
        self.Message4.configure(width=250)

        self.Message5 = Message(top)
        self.Message5.place(relx=0.50, rely=0.6, relheight=0.07, relwidth=0.16)
        self.Message5.configure(background="#d9d9d9")
        self.Message5.configure(font=font24)
        self.Message5.configure(foreground="#000000")
        self.Message5.configure(highlightbackground="#d9d9d9")
        self.Message5.configure(highlightcolor="black")
        self.Message5.configure(text='''Rot. Atual(RPM)''')
        self.Message5.configure(width=250)

        self.Message6 = Message(top)
        self.Message6.place(relx=0.67, rely=0.6, relheight=0.07, relwidth=0.14)
        self.Message6.configure(background="#d9d9d9")
        self.Message6.configure(font=font24)
        self.Message6.configure(foreground="#000000")
        self.Message6.configure(highlightbackground="#d9d9d9")
        self.Message6.configure(highlightcolor="black")
        self.Message6.configure(text='''Tempo Ligado''')
        self.Message6.configure(width=250)

        self.Message7 = Message(top)
        self.Message7.place(relx=0.83, rely=0.6, relheight=0.07, relwidth=0.14)
        self.Message7.configure(background="#d9d9d9")
        self.Message7.configure(font=font24)
        self.Message7.configure(foreground="#000000")
        self.Message7.configure(highlightbackground="#d9d9d9")
        self.Message7.configure(highlightcolor="black")
        self.Message7.configure(text='''Tempo Enduro''')
        self.Message7.configure(width=250)

        self.Button1 = Button(top)
        self.Button1.place(relx=0.03, rely=0.83, height=71, width=137)
        self.Button1.configure(activebackground="#d9d9d9")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#d9d9d9")
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(font=font21)
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#d9d9d9")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(text='''ON''')
        self.Button1.configure(command=self.callback_button_on)

        self.Button2 = Button(top)
        self.Button2.place(relx=0.2, rely=0.83, height=71, width=137)
        self.Button2.configure(activebackground="#d9d9d9")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#d9d9d9")
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(font=font21)
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''Pause''')
        self.Button2.configure(command=self.callback_button_pause)

        self.Button3 = Button(top)
        self.Button3.place(relx=0.37, rely=0.83, height=71, width=137)
        self.Button3.configure(activebackground="#d9d9d9")
        self.Button3.configure(activeforeground="#000000")
        self.Button3.configure(background="#d9d9d9")
        self.Button3.configure(disabledforeground="#a3a3a3")
        self.Button3.configure(font=font21)
        self.Button3.configure(foreground="#000000")
        self.Button3.configure(highlightbackground="#d9d9d9")
        self.Button3.configure(highlightcolor="black")
        self.Button3.configure(pady="0")
        self.Button3.configure(text='''BOX''')
        self.Button3.configure(command=self.callback_button_box)

        self.Button4 = Button(top)
        self.Button4.place(relx=0.53, rely=0.83, height=71, width=137)
        self.Button4.configure(activebackground="#d9d9d9")
        self.Button4.configure(activeforeground="#000000")
        self.Button4.configure(background="#d9d9d9")
        self.Button4.configure(disabledforeground="#a3a3a3")
        self.Button4.configure(font=font21)
        self.Button4.configure(foreground="#000000")
        self.Button4.configure(highlightbackground="#d9d9d9")
        self.Button4.configure(highlightcolor="black")
        self.Button4.configure(pady="0")
        self.Button4.configure(text='''Salvar''')
        self.Button4.configure(command=self.callback_button_salvar)

        self.Button5 = Button(top)
        self.Button5.place(relx=0.7, rely=0.83, height=71, width=137)
        self.Button5.configure(activebackground="#d9d9d9")
        self.Button5.configure(activeforeground="#000000")
        self.Button5.configure(background="#d9d9d9")
        self.Button5.configure(disabledforeground="#a3a3a3")
        self.Button5.configure(font=font21)
        self.Button5.configure(foreground="#000000")
        self.Button5.configure(highlightbackground="#d9d9d9")
        self.Button5.configure(highlightcolor="black")
        self.Button5.configure(pady="0")
        self.Button5.configure(text='''Zerar''')
        self.Button5.configure(command=self.callback_button_zerar)

        self.Button6 = Button(top)
        self.Button6.place(relx=0.87, rely=0.83, height=71, width=137)
        self.Button6.configure(activebackground="#d9d9d9")
        self.Button6.configure(activeforeground="#000000")
        self.Button6.configure(background="#d9d9d9")
        self.Button6.configure(disabledforeground="#a3a3a3")
        self.Button6.configure(font=font21)
        self.Button6.configure(foreground="#000000")
        self.Button6.configure(highlightbackground="#d9d9d9")
        self.Button6.configure(highlightcolor="black")
        self.Button6.configure(pady="0")
        self.Button6.configure(text='''Tempo''')
        self.Button6.configure(command=self.callback_button_tempo)

        self.Message8 = Message(top)
        self.Message8.place(relx=0.30, rely=0.04, relheight=0.05, relwidth=0.40)
        self.Message8.configure(background="#d9d9d9")
        self.Message8.configure(font=font20)
        self.Message8.configure(foreground="#000000")
        self.Message8.configure(highlightbackground="#d9d9d9")
        self.Message8.configure(highlightcolor="black")
        self.Message8.configure(text='''Telemetria EESC USP BAJA''')
        self.Message8.configure(width=500)

        X = [0, 2, 4, 8]
        Y = [0, 5, 7, 6]
        X1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        Y1 = [3, 5, 6, 8, 9, 7, 8, 6, 9, 10]
        X2 = [0, 1, 2, 3, 5, 6]
        Y2 = [0, 2, 3, 7, 5, 8]
        ticks = [0,2,4,8]

        #X = 10*np.array(range(len(data1)))
        #Y = np.sin(X)

        #X1 = np.linspace(0, 2* np.pi, 50)
        #Y1 = np.cos(X1)

        #X2 = np.linspace(0, 2* np.pi, 50)
        #Y2 = np.arcsinh(X2)

        fig = plt.Figure()
        ax = fig.add_subplot(111, ylabel = 'Distribuição(%)', title = 'Distribuição', xlabel = 'Tempo', aspect = 'equal')
        fig.set_tight_layout(True)
        ax.plot(X, Y, 'r')
        draw_figure(self.Canvas1, fig)


        fig1 = plt.Figure()
        ax1 = fig1.add_subplot(111, ylabel = 'Km/h e RPM', title = 'Velocidade e Rotação', xlabel = 'Tempo')
        fig1.set_tight_layout(True)
        ax1.plot(X1, Y1, 'r')
        draw_figure(self.Canvas2, fig1)


        fig2 = plt.Figure()
        ax2 = fig2.add_subplot(111, ylabel = '(%)', title = 'Combustível', xlabel = 'Tempo')
        fig2.set_tight_layout(True)
        ax2.plot(X2, Y2, 'r')
        draw_figure(self.Canvas3, fig2)

    # em callback nao pode ter loop demorado (e jamais "while True")
    def callback_button_box(self):
        print("Funfou")

    def callback_button_on(self):
        print("ON")
        thread_backend.Resume()

    def callback_button_pause(self):
        print("PAUSE")
        thread_backend.Pause()

    def callback_button_tempo(self):
        pass

    def callback_button_zerar(self):
        pass

    def callback_button_salvar(self):
        # Seria legal dar a opcao de escolher o nome do arquivo antes de salvar
        print("SALVAR")
        thread_backend.leitor.SalvarExcel('output.xlsx')



def draw_figure(canvas, figure):
    canvas = FigureCanvasTkAgg(figure, master=canvas)
    canvas.show()
    canvas.get_tk_widget().pack(anchor = tk.NW, side=tk.TOP, fill=tk.BOTH, expand=1)

def on_close():
    print("[Closing]")
    thread_backend.Stop()
    root.destroy()
    sys.exit()

class Backend(threading.Thread):
    def __init__(self):
      threading.Thread.__init__(self)
      self.leitor = LeitorSerial()
      self.pause = True
      self.stop = False

    def Stop(self):
        self.stop = True

    def Pause(self):
        self.pause = True

    def Resume(self):
        self.pause = False

    def run(self):
        self.leitor.df['KmRodadosAtual'] = np.nan
        self.leitor.df['KmRodadosTotal'] = np.nan
        KmRodadosTotal = 0
        firstIter = True
        while self.stop == False:
            if self.pause == False:
                print("foo")
                if PORT is None:
                    self.leitor.LeituraAleatoria()
                    try:
                        sleep(1)
                    except NameError:
                        pass
                else:
                    self.leitor.Leitura()

                #Atribui a CHOKE o ultimo Choke registrado
                CHOKE = self.leitor.df.Choke.iloc[-1]
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
                if firstIter == True:
                    self.leitor.df.KmRodadosTotal.iloc[-1] = 0
                    firstIter = False
                else:
                    #Retorna a velocidade média em m/s
                    VelMediaMPS = ((self.leitor.df.Velocidade.iloc[-1] + self.leitor.df.Velocidade.iloc[-2])/2)/3.6
                    #Retorna os Km Rodados nesta iteração
                    KmRodadosAtual = VelMediaMPS * (self.leitor.df.Tempo.iloc[-1] - self.leitor.df.Tempo.iloc[-2])/1000
                    self.leitor.df.KmRodadosAtual.iloc[-1] = KmRodadosAtual
                    #Soma os Km Rodados nesta iteração ao total
                    KmRodadosTotal += KmRodadosAtual
                    self.leitor.df.KmRodadosTotal.iloc[-1] = KmRodadosTotal

def main():
    # Cria thread do backend
    global thread_backend
    try:
        thread_backend = Backend()
        thread_backend.start()
    except:
        print ("Error: unable to start backend's thread")
        sys.exit()

    # Cria interface (frontend)
    global root
    root = Tk()
    #root.protocol("WM_DELETE_WINDOW", on_close)
    top = Frontend(root)
    root.mainloop()

if __name__ == '__main__':
    main()

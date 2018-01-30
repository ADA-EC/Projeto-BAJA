import numpy as np
import sys
import serial
import pandas as pd

from datetime import datetime
from time import sleep

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.animation as animation
from matplotlib import style
style.use("ggplot")

from tkinter import *
import tkinter.ttk as ttk
import tkinter as tk

try:
    import threading
except ImportError:
    import dummy_threading as threading

### Implements Singleton Design Pattern
class SingletonDecorator:
    """http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Singleton.html"""
    def __init__(self,klass):
        self.klass = klass
        self.instance = None
    def __call__(self,*args,**kwds):
        if self.instance == None:
            self.instance = self.klass(*args,**kwds)
        return self.instance

class Interpretador():
    """This class is a Singleton"""
    # Nome de cada campo que é recebido pelo receptor serial + tempo
    labels = ('Tempo',
        'Box',
        'Velocidade',
        'Rotacao',
        'Distribuicao',
        'Combustivel',
        'Posicao')

    def __init__(self):
        # cria o DataFrame com as colunas que serão preenchidas
        self.df = pd.DataFrame(columns=self.labels)
        self.df['KmRodadosAtual'] = np.nan
        self.df['KmRodadosTotal'] = np.nan
        self._KmRodadosTotal = 0

    def last(self, label, length=1, conv=True):
        l = self.df[label].iloc[-length:].as_matrix().reshape(-1)
        if conv == False:
            return l

        # conversion from list to number
        if l.shape[0] == 0:
            return None
        elif l.shape[0] == 1:
            return l[0]
        else:
            return l

    def append(self, readings):
        # Append readings to Dataframe
        self.df = self.df.append(dict(zip(self.labels, readings)), ignore_index=True)

        # Calculo de distancia percorrida
        # Uma vez que é necessário o acesso aos dois últimos registros,
        # O 'if' impede que esse cálculo seja feito na primeira iteração
        if self.df.index.shape[0] > 1:
            #Determina a velocidade média em m/s
            VelMediaMPS = ((self.df.Velocidade.iloc[-1] + self.df.Velocidade.iloc[-2])/2)/3.6
            #Determina os Km Rodados nesta iteração
            KmRodadosAtual = VelMediaMPS * (self.df.Tempo.iloc[-1] - self.df.Tempo.iloc[-2])/1000
            self.df.KmRodadosAtual.iloc[-1] = KmRodadosAtual
            #Soma os Km Rodados nesta iteração ao total
            self._KmRodadosTotal += KmRodadosAtual
            self.df.KmRodadosTotal.iloc[-1] = self._KmRodadosTotal
        else:
            self.df.KmRodadosTotal.iloc[-1] = 0

    def saveExcel(self, filename='output.xlsx'):
        writer = pd.ExcelWriter(filename)
        df_exc = self.df[['Tempo','Velocidade', 'Rotacao', 'Distribuicao', 'Combustivel', 'KmRodadosTotal', 'Posicao']]
        df_exc.to_excel(writer,'Sheet1')
        writer.close()
        print(self.df)


# This indeed makes the classa a Singleton
Interpretador = SingletonDecorator(Interpretador)

class LeitorSerial():
    def __init__(self, port=None, BaudRate = 9600):
        # atribui a tstart o tempo do sistema na criação do objeto
        self.tstart = datetime.now()
        self.port = port
        if self.port is not None:
            # configura a conexão serial
            # detalhes em "https://pythonhosted.org/pyserial/pyserial_api.html"
            self.ser = serial.Serial(
                port=port,
                baudrate=BaudRate,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS
            )
            # cria um lock para evitar acesso mutuo a porta serial
            self._lock = threading.Lock()
            print('[Conexao serial aberta]')
        print('[Leitor Serial iniciado]')

    def Leitura(self):
        with self._lock:
            line = str(self.ser.readline(),'utf-8')
            readings = [np.float(x) for x in line.split(';')[:-1]]
            time = (datetime.now()-self.tstart).total_seconds()
            readings.insert(0, time)
            return readings

    def LeituraAleatoria(self):
        l = np.random.randint(0, 100, size=6)
        box_values = [0,0,0,0,48,48,49]
        l[0] = box_values[np.random.choice(len(box_values))]# BOX
        readings = list(l)
        time = (datetime.now()-self.tstart).total_seconds()
        readings.insert(0, time)
        return readings

    def MandaZero(self):
        if self.port is not None:
            with self._lock:
                self.ser.write(b'0')

    def MandaUm(self):
        if self.port is not None:
            with self._lock:
                self.ser.write(b'1')


class Backend(threading.Thread):
    def __init__(self, port=None):
        """port: Endereco do PORT de entrada. i.e. /dev/ttyCOM6
        Se PORT for None, faz leituras aleatorias."""
        threading.Thread.__init__(self)
        self.pause = True
        self.stop = False
        self.port = port
        self.leitor = LeitorSerial(port=port)

    def Stop(self):
        self.stop = True

    def Pause(self):
        self.pause = True

    def Resume(self):
        self.pause = False

    def run(self):
        interp = Interpretador() # Singleton
        while self.stop == False:
            if self.pause == False:
                print("[Running Backend]")
                readings = None
                if self.port is not None:
                    readings = self.leitor.Leitura()
                else:
                    readings = self.leitor.LeituraAleatoria()
                    sleep(1)

                interp.append(readings)
                print(interp.df.tail())


class Frontend(tk.Tk):

    def create_elem(self, top):
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

        top.geometry("1366x705+0+0")

        top.title("Telemetria EESC USP BAJA")
        top.configure(background="#d9d9d9")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")

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
        self.Button1.configure(command=self.callback_button_on) # <<<  Foi assim que setei qual a funcao que o botao executa <<<

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

    def __init__(self, *args, **kwargs):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        tk.Tk.__init__(self, *args, **kwargs)

        # make sure widget instances are deleted
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # cria elementos da janela: botoes, paineis, titulo, etc
        self.create_elem(self)

        self.backend = None
        self.pause = True

        self.box_button_pressed = False

        self.Canvas = {1: self.Canvas1, 2: self.Canvas2, 3: self.Canvas3}
        self.fig = {}
        self.ax = {}
        self.ani = {}

        self.fig[1] = Figure()
        self.ax[1] = self.fig[1].add_subplot(111, ylabel = 'Distribuição(%)', title = 'Distribuição', xlabel = 'Tempo(s)')
        self.fig[1].set_tight_layout(True)
        self.Canvas[1] = FigureCanvasTkAgg(self.fig[1], self.Canvas1)
        self.Canvas[1].show()
        self.Canvas[1].get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.ani[1] = animation.FuncAnimation(self.fig[1], self.update_fig, \
            lambda: self.gen_values_anim(label='Distribuicao'), fargs=(self.ax[1],'c', 'Distribuição', 'Tempo(s)', 'Distribuição(%)'))

        self.fig[2] = Figure()
        self.ax[2] = self.fig[2].add_subplot(111, ylabel = 'Km/h e RPM', title = 'Velocidade e Rotação', xlabel = 'Tempo(s)')
        self.fig[2].set_tight_layout(True)
        self.Canvas[2] = FigureCanvasTkAgg(self.fig[2], self.Canvas[2])
        self.Canvas[2].show()
        self.Canvas[2].get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.ani[2] = animation.FuncAnimation(self.fig[2], self.update_fig_2, \
            self.gen_values_anim_2, fargs=(self.ax[2],'y', 'c', 'Velocidade e Rotação', 'Tempo(s)', 'Km/h e RPM'))

        self.fig[3] = Figure()
        self.ax[3] = self.fig[3].add_subplot(111, ylabel = 'Combustível(%)', title = 'Combustível', xlabel = 'Tempo')
        self.fig[3].set_tight_layout(True)
        self.Canvas[3] = FigureCanvasTkAgg(self.fig[3], self.Canvas[3])
        self.Canvas[3].show()
        self.Canvas[3].get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.ani[3] = animation.FuncAnimation(self.fig[3], self.update_fig, \
            lambda: self.gen_values_anim(label='Combustivel'), fargs=(self.ax[3],'c', 'Combustível', 'Tempo(s)', 'Combustível(%)'))

        self.stop_ani()

    def stop_ani(self):
        for ani in self.ani.values():
            ani.event_source.stop()

    def start_ani(self):
        for ani in self.ani.values():
            ani.event_source.start()

    def update_fig(self, data, ax, color, TITLE = None, XLABEL = None, YLABEL = None):
        t, y = data
        ax.cla()
        if YLABEL != None:
            ax.set(ylabel = YLABEL)
        if TITLE != None:
            ax.set(title = TITLE)
        if XLABEL != None:
            ax.set(xlabel = XLABEL)
        ax.plot(t,y, c=color)

    def update_fig_2(self, data, ax, c1, c2, TITLE = None, XLABEL = None, YLABEL = None):
        t1, y1, t2, y2 = data
        ax.cla()
        if YLABEL != None:
            ax.set(ylabel = YLABEL)
        if TITLE != None:
            ax.set(title = TITLE)
        if XLABEL != None:
            ax.set(xlabel = XLABEL)
        ax.plot(t1,y1, c=c1)
        ax.plot(t2,y2, c=c2)

    def update_fig3(self, data, ax, color):
        t, y = data
        ax.cla()
        ax.set(ylabel = '%', title = 'Combustível', xlabel = 'Tempo(s)')
        ax.plot(t,y, c=color)

    def gen_values_anim(self, label):
        interp = Interpretador()
        while True:
            t = interp.last('Tempo', 20, conv=False)
            y = interp.last(label, 20, conv=False)
            yield t, y

    def gen_values_anim_2(self):
        iter_vel = self.gen_values_anim('Velocidade')
        iter_rot = self.gen_values_anim('Rotacao')
        while True:
            t1, y1 = next(iter_vel)
            t2, y2 = next(iter_rot)
            yield t1,y1,t2,y2



    # em callback nao pode ter loop demorado (e jamais "while True")
    def callback_button_on(self):
        print("ON")
        self.pause = False
        self.after(500, self.update_labels)
        self.after(100, self.update_box)
        self.backend.Resume()
        self.start_ani()

    def callback_button_pause(self):
        print("PAUSE")
        self.pause = True
        self.backend.Pause()
        self.stop_ani()

    def callback_button_tempo(self):
        #self.draw_graph1()
        pass

    def callback_button_zerar(self):
        print("ZERAR")
        ## Deve limpar a figura

    def callback_button_salvar(self):
        # Seria legal dar a opcao de escolher o nome do arquivo antes de salvar
        print("SALVAR")
        interp = Interpretador() # Singleton
        # Precisa de pausar pq o backend fica escrevendo no objeto
        # que o interpretador quer salvar em disco. Nao tem problema de
        # concorrencia, mas o SO fica maluco e nao salva direito, ou demora
        # pra salvar. Pausando, ele salva rapido.
        self.backend.Pause()
        interp.saveExcel('baja.xlsx') #'+str(datetime.now())+
        self.backend.Resume()

    def callback_button_box(self):
        if self.box_button_pressed == False:
            self.box_button_pressed = True
            self.Button3.configure(foreground="#ff1900")
            self.Button3.configure(activeforeground="#ff1900")

        else:
            self.box_button_pressed = False
            self.Button3.configure(foreground="#000000")
            self.Button3.configure(activeforeground="#000000")
            # self.Button3.configure(background="#2e0400")
            # self.Button3.configure(activebackground="#2e0400")

    def update_box(self):
        # #Atribui a BOX o ultimo Box registrado
        interp = Interpretador()
        BOX = interp.last('Box')
        if self.box_button_pressed:
            if BOX == 0 or BOX == ord('0'): # '0' em ascii tem valor 48
                print('manda um')
                self.backend.leitor.MandaUm()
            elif BOX == ord('1'): # '1' em ascii tem valor 49
                print('box:vermelho')
                self.Button3.configure(background="#7f0c00")
                self.Button3.configure(activebackground="#7f0c00")
        else:
            if BOX == ord('1'):
                print('manda zero')
                self.backend.leitor.MandaZero()
            elif BOX ==  ord('0'):
                print('box:preto')
                self.Button3.configure(background="#d9d9d9")
                self.Button3.configure(activebackground="#d9d9d9")
        if self.pause == False:
            self.after(100, self.update_box)

    def update_labels(self):
        interp = Interpretador() # Singleton
        
        try:
            self.Label2.configure(text=round((interp.last('Distribuicao')),4))
            self.Label3.configure(text=round((interp.last('Velocidade')),4))
            self.Label4.configure(text=round((interp.last('KmRodadosTotal')),4))
            self.Label5.configure(text=round((interp.last('Rotacao')),4))
            self.Label6.configure(text=round((interp.last('Tempo')),4))
        except:
            pass

        # Isso faz com que a funcao seja chamada a cada 500ms pelo root.mainloop()
        if self.pause == False:
            self.after(500, self.update_labels)

    def on_close(self):
        print("[Closing]")
        self.backend.Stop()
        self.quit()
        self.destroy()
        sys.exit()

def main():
    PORT = None
    # Primeiro argumento é a porta serial
    if len(sys.argv) > 1:
        PORT = sys.argv[1]

    # Cria thread do backend
    try:
        thread_backend = Backend(port=PORT)
        thread_backend.start()
    except:
        print ("Error: unable to start backend's thread")
        sys.exit()

    # Cria interface (frontend)
    root = Frontend()
    root.backend = thread_backend
    root.mainloop()

if __name__ == '__main__':
    main()

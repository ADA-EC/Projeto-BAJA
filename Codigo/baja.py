#!/usr/bin/python3
################################################################################
# Sistmea de Telemetria EESC USP Baja
#
# Tem como proposito realizar a telemetria do carro do grupo EESC USP Baja SAE
################################################################################
# Copyright (C) 2018 ADA-Projetos em Engenharia de Computacao
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
# Authors:
# Pedro V. B. Jeronymo (pedrovbj@gmail.com)
# Amador M. de Souza Neto (amador.neto@usp.br)
################################################################################


# Constantes do projeto
import const

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

class Cronometro():
    def __init__(self):
        self._lock = threading.Lock()
        self.Zerar()

    def Formatar(self, t):
        mn = int(t//60)
        sec = int(t-60*mn)
        return mn, sec

    def Aferir(self, formatted=True):
        with self._lock:
            if self.pause:
                if formatted:
                    return self.Formatar(self._t_acc)
                else:
                    return self._t_acc
            self._t_running = (datetime.now()-self._t_ref).total_seconds()+self._t_acc
            if formatted:
                return self.Formatar(self._t_running)
            else:
                return self._t_running

    def Pausar(self):
        with self._lock:
            if self.pause == False:
                self.pause = True
                self._t_acc = self._t_running

    def Resumir(self):
        with self._lock:
            if self.pause == True:
                self.pause = False
                self._t_ref = datetime.now()

    def Toggle(self):
        with self._lock:
            if self.pause == True:
                self.pause = False
                self._t_ref = datetime.now()
            else:
                self.pause = True
                self._t_acc = self._t_running

    def Zerar(self):
        with self._lock:
            self.pause = True
            self._t_acc = 0
            self._t_running = 0
            self._t_ref = None

class Interpretador():
    def __init__(self):
        # cria o DataFrame com as colunas que serão preenchidas
        self.df = pd.DataFrame(columns=const.SER_LABELS)
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
        self.df = self.df.append(dict(zip(const.SER_LABELS, readings)), ignore_index=True)

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

    def clear(self):
        self.__init__()

class LeitorSerial():
    def __init__(self, port=None, BaudRate = const.SER_BAUD_RATE):
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
            print('[ Conexao serial aberta na porta', self.port, ']')
        print('[Leitor Serial iniciado]')

    def Leitura(self):
        if self.port is not None:
            with self._lock:
                line = str(self.ser.readline(),'utf-8')
                readings = [np.float(x) for x in line.split(';')[:-1]]
                time = cronExec.Aferir(formatted=False)
                readings.insert(0, time)
                return readings
        else: # realiza leitura aleatoria
            l = np.random.randint(0, 100, size=6)
            box_values = [0,0,0,0,48,48,49]
            l[0] = box_values[np.random.choice(len(box_values))]# BOX
            readings = list(l)
            time = cronExec.Aferir(formatted=False)
            readings.insert(0, time)
            sleep(1)
            return readings

    def MandaZero(self):
        if self.port is not None:
            with self._lock:
                self.ser.write(b'0')

    def MandaUm(self):
        if self.port is not None:
            with self._lock:
                self.ser.write(b'1')

    def Fechar(self):
        if self.port is not None:
            with self._lock:
                self.ser.close()

class Backend(threading.Thread):
    def run(self):
        while True:
            try:
                if cronExec.pause == False:
                    print("[Running Backend]")
                    readings = leitorSer.Leitura()
                    interp.append(readings)
                    print(interp.df.tail())
                else:
                    with pausing_cv:
                        pausing_cv.notify()
            except:
                # Ignores NameError's on exit
                pass

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
        self.Label6.configure(text='''0:00''')

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
        self.Label7.configure(text='''0:00''')

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

        # Funcionalidade do botao de box
        self.box_button_pressed = False

        # Funcionalidade de enduro
        self.cronEnduro = Cronometro()

        # capta se este cron estava pausado antes de pausar o cronometro global
        self.pauseCronEnduro = self.cronEnduro.pause

        # Graficos
        self.Canvas = {1: self.Canvas1, 2: self.Canvas2, 3: self.Canvas3}
        self.fig = {}
        self.ax = {}
        self.ani = {}


        self.add_fig(1, 'Distribuição', 'Tempo(s)', 'Distribuição(%)')
        self.ani[1] = animation.FuncAnimation(self.fig[1], self.update_fig, \
            lambda: self.gen_values_anim(label='Distribuicao'), \
            fargs=(self.ax[1],'c', 'Distribuição', 'Tempo(s)', 'Distribuição(%)'), \
            interval=const.PLOT_DELAY)

        self.add_fig(2, 'Velocidade e Rotação', 'Tempo(s)', 'Km/h e RPM')
        self.ani[2] = animation.FuncAnimation(self.fig[2], self.update_fig_2, \
            self.gen_values_anim_2, \
            fargs=(self.ax[2],'y', 'c', 'Velocidade e Rotação', 'Tempo(s)', 'Km/h e RPM'), \
            interval=const.PLOT_DELAY)

        self.add_fig(3, 'Combustível', 'Tempo(s)', 'Combustível(%)')
        self.ani[3] = animation.FuncAnimation(self.fig[3], self.update_fig, \
            lambda: self.gen_values_anim(label='Combustivel'), \
            fargs=(self.ax[3],'c', 'Combustível', 'Tempo(s)', 'Combustível(%)'), \
            interval=const.PLOT_DELAY)

        self.stop_ani()

    def add_fig(self, i, title, xlabel, ylabel):
        self.fig[i] = Figure()
        self.ax[i] = self.fig[i].add_subplot(111, title=title, xlabel=xlabel, ylabel=ylabel)
        self.fig[i].set_tight_layout(True)
        self.Canvas[i] = FigureCanvasTkAgg(self.fig[i], self.Canvas[i])
        self.Canvas[i].show()
        self.Canvas[i].get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def stop_ani(self):
        for ani in self.ani.values():
            ani.event_source.stop()

    def start_ani(self):
        for ani in self.ani.values():
            ani.event_source.start()

    def update_fig(self, data, ax, color, TITLE = None, XLABEL = None, YLABEL = None):
        t, y = data
        ax.cla()
        if YLABEL is not None:
            ax.set(ylabel = YLABEL)
        if TITLE is not None:
            ax.set(title = TITLE)
        if XLABEL is not None:
            ax.set(xlabel = XLABEL)
        ax.plot(t,y, c=color)

    def update_fig_2(self, data, ax, c1, c2, TITLE = None, XLABEL = None, YLABEL = None):
        t1, y1, t2, y2 = data
        ax.cla()
        if YLABEL is not None:
            ax.set(ylabel = YLABEL)
        if TITLE is not None:
            ax.set(title = TITLE)
        if XLABEL is not None:
            ax.set(xlabel = XLABEL)
        ax.plot(t1,y1, c=c1)
        ax.plot(t2,y2, c=c2)

    def gen_values_anim(self, label):
        while True:
            t = interp.last('Tempo', const.PLOT_WIN, conv=False)
            y = interp.last(label, const.PLOT_WIN, conv=False)
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
        print("[ON]")
        cronExec.Resumir()
        if self.pauseCronEnduro == False:
            self.cronEnduro.Resumir()
        self.after(const.UPDATE_DELAY, self.update_labels)
        self.after(const.UPDATE_DELAY, self.update_box)
        self.start_ani()

    def callback_button_pause(self):
        print("[PAUSE]")
        cronExec.Pausar()
        with pausing_cv:
            pausing_cv.wait()
        self.pauseCronEnduro = self.cronEnduro.pause
        self.cronEnduro.Pausar()
        self.stop_ani()

    def callback_button_tempo(self):
        print('[TEMPO (Enduro)]')
        self.cronEnduro.Toggle()

    def callback_button_zerar(self):
        self.callback_button_pause()
        self.Label2.configure(text='0')
        self.Label3.configure(text='0')
        self.Label4.configure(text='0')
        self.Label5.configure(text='0')
        self.Label6.configure(text='0:00')
        self.Label7.configure(text='0:00')
        interp.clear()
        self.start_ani()
        print("[ZERAR]")

    def callback_button_salvar(self):
        print('[SALVAR]')
        filename = 'baja'+datetime.now().strftime("%Y-%m-%d_%Hh%Mm%Ss")+'.xlsx'
        paused = cronExec.pause
        cronExec.Pausar()
        with pausing_cv:
            pausing_cv.wait()
        interp.saveExcel(filename)
        if paused == False:
            cronExec.Resumir()
        print('[Dados salvos em: '+filename+']')

    def callback_button_box(self):
        print('[BOX]')
        if self.box_button_pressed == False:
            self.box_button_pressed = True
            self.Button3.configure(foreground="#ff1900")
            self.Button3.configure(activeforeground="#ff1900")
        else:
            self.box_button_pressed = False
            self.Button3.configure(foreground="#000000")
            self.Button3.configure(activeforeground="#000000")

    def update_box(self):
        # #Atribui a BOX o ultimo Box registrado
        BOX = interp.last('Box')
        if self.box_button_pressed:
            if BOX == 0 or BOX == ord('0'): # '0' em ascii tem valor 48
                print('[Enviando 1]')
                leitorSer.MandaUm()
            elif BOX == ord('1'): # '1' em ascii tem valor 49
                #print('[box:vermelho]')
                self.Button3.configure(background="#7f0c00")
                self.Button3.configure(activebackground="#7f0c00")
        else:
            if BOX == ord('1'):
                print('[Enviando 0]')
                leitorSer.MandaZero()
            elif BOX ==  ord('0'):
                #print('[box:preto]')
                self.Button3.configure(background="#d9d9d9")
                self.Button3.configure(activebackground="#d9d9d9")
        if cronExec.pause == False:
            self.after(const.UPDATE_DELAY, self.update_box)

    def update_labels(self):
        try:
            self.Label2.configure(text=round((interp.last('Distribuicao')),4))
            self.Label3.configure(text=round((interp.last('Velocidade')),4))
            self.Label4.configure(text=round((interp.last('KmRodadosTotal')),4))
            self.Label5.configure(text=round((interp.last('Rotacao')),4))
            # tempo de exec
            mn, sec = cronExec.Aferir()
            self.Label6.configure(text="{:d}:{:02d}".format(mn, sec))
            # tempo de enduro
            mn, sec = self.cronEnduro.Aferir()
            self.Label7.configure(text="{:d}:{:02d}".format(mn, sec))
        except:
            pass
        # Isso faz com que a funcao seja chamada a cada (...)ms pelo root.mainloop()
        if cronExec.pause == False:
            self.after(const.UPDATE_DELAY, self.update_labels)

    def on_close(self):
        print("[Fechando]")
        cronExec.Pausar()
        self.quit()
        self.destroy()
        sys.exit()

## Cronometro (GLOBAL) do tempo de execucao
# Referencia para o Frontend e o Backend
global cronExec
cronExec = Cronometro()

## Interpretador
# Acessado por ambas as classes
global interp
interp = Interpretador()

## Leitor Serial
# Acessado por ambas as classes
global leitorSer
leitorSer = None

## Variavel condicional para sincronizacao de threads
# Sempre que o Frontend requesita a pausa e é necessario esperar
# o Backend parar, se utiliza esta variavel
global pausing_cv
pausing_cv = threading.Condition()

if __name__ == '__main__':
    ## Definicao da porta serial
    # Prioridade: 1. Argumento; 2. const.py; 3. Leituras aleatorias
    PORT = None
    if const.SER_PORT is not None:
        PORT = const.SER_PORT
    # Primeiro argumento é a porta serial
    # Se fornecido nos argumentos sobrescreve const.py
    # Se nao fornecido aqui nem em const.py, faz leituras aleatorias
    if len(sys.argv) > 1:
        PORT = sys.argv[1]

    # Instancia Leitor Serial
    leitorSer = LeitorSerial(port=PORT)

    # Cria thread do backend
    try:
        thread_backend = Backend(daemon=True)
        thread_backend.start()
    except:
        print ("Erro: nao foi possivel iniciar o Backend")
        sys.exit()

    # Cria interface (frontend)
    root = Frontend()
    root.mainloop()

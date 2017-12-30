function varargout = Interface_1(varargin)
% INTERFACE_1 MATLAB code for Interface_1.fig
%      INTERFACE_1, by itself, creates a new INTERFACE_1 or raises the existing
%      singleton*.
%
%      H = INTERFACE_1 returns the handle to a new INTERFACE_1 or the handle to
%      the existing singleton*.
%
%      INTERFACE_1('CALLBACK',hObject,eventData,handles,...) calls the local
%      function named CALLBACK in INTERFACE_1.M with the given input arguments.
%
%      INTERFACE_1('Property','Value',...) creates a new INTERFACE_1 or raises the
%      existing singleton*.  Starting from the left, property value pairs are
%      applied to the GUI before Interface_1_OpeningFcn gets called.  An
%      unrecognized property name or invalid value makes property application
%      stop.  All inputs are passed to Interface_1_OpeningFcn via varargin.
%
%      *See GUI Options on GUIDE's Tools menu.  Choose "GUI allows only one
%      instance to run (singleton)".
%
% See also: GUIDE, GUIDATA, GUIHANDLES

% Edit the above text to modify the response to help Interface_1

% Last Modified by GUIDE v2.5 08-Aug-2017 20:10:57

% Begin initialization code - DO NOT EDIT
gui_Singleton = 1;
gui_State = struct('gui_Name',       mfilename, ...
                   'gui_Singleton',  gui_Singleton, ...
                   'gui_OpeningFcn', @Interface_1_OpeningFcn, ...
                   'gui_OutputFcn',  @Interface_1_OutputFcn, ...
                   'gui_LayoutFcn',  [] , ...
                   'gui_Callback',   []);
if nargin && ischar(varargin{1})
    gui_State.gui_Callback = str2func(varargin{1});
end

if nargout
    [varargout{1:nargout}] = gui_mainfcn(gui_State, varargin{:});
else
    gui_mainfcn(gui_State, varargin{:});
end
% End initialization code - DO NOT EDIT


% --- Executes just before Interface_1 is made visible.
function Interface_1_OpeningFcn(hObject, eventdata, handles, varargin)
% This function has no output args, see OutputFcn.
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
% varargin   command line arguments to Interface_1 (see VARARGIN)

% Choose default command line output for Interface_1
handles.output = hObject;

% Update handles structure
guidata(hObject, handles);

% UIWAIT makes Interface_1 wait for user response (see UIRESUME)
% uiwait(handles.figure1);


% --- Outputs from this function are returned to the command line.
function varargout = Interface_1_OutputFcn(hObject, eventdata, handles) 
% varargout  cell array for returning output args (see VARARGOUT);
% hObject    handle to figure
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Get default command line output from handles structure
varargout{1} = handles.output;


% --- Executes on button press in pushbutton1.
function pushbutton1_Callback(hObject, eventdata, handles)
% hObject    handle to pushbutton1 (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)



function Cel_Choke_Callback(hObject, eventdata, handles)
% hObject    handle to Cel_Choke (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Cel_Choke as text
%        str2double(get(hObject,'String')) returns contents of Cel_Choke as a double


% --- Executes during object creation, after setting all properties.
function Cel_Choke_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Cel_Choke (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function Cel_Distribuicao_Callback(hObject, eventdata, handles)
% hObject    handle to Cel_Distribuicao (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Cel_Distribuicao as text
%        str2double(get(hObject,'String')) returns contents of Cel_Distribuicao as a double


% --- Executes during object creation, after setting all properties.
function Cel_Distribuicao_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Cel_Distribuicao (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function Cel_Velocidade_Callback(hObject, eventdata, handles)
% hObject    handle to Cel_Velocidade (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Cel_Velocidade as text
%        str2double(get(hObject,'String')) returns contents of Cel_Velocidade as a double


% --- Executes during object creation, after setting all properties.
function Cel_Velocidade_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Cel_Velocidade (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function Cel_Rotacao_Callback(hObject, eventdata, handles)
% hObject    handle to Cel_Rotacao (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Cel_Rotacao as text
%        str2double(get(hObject,'String')) returns contents of Cel_Rotacao as a double


% --- Executes during object creation, after setting all properties.
function Cel_Rotacao_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Cel_Rotacao (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function Cel_KmRodados_Callback(hObject, eventdata, handles)
% hObject    handle to Cel_KmRodados (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Cel_KmRodados as text
%        str2double(get(hObject,'String')) returns contents of Cel_KmRodados as a double


% --- Executes during object creation, after setting all properties.
function Cel_KmRodados_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Cel_KmRodados (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function Cel_Tempo_Ligado_Callback(hObject, eventdata, handles)
% hObject    handle to Cel_Tempo_Ligado (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Cel_Tempo_Ligado as text
%        str2double(get(hObject,'String')) returns contents of Cel_Tempo_Ligado as a double


% --- Executes during object creation, after setting all properties.
function Cel_Tempo_Ligado_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Cel_Tempo_Ligado (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end



function Cel_Tempo_Enduro_Callback(hObject, eventdata, handles)
% hObject    handle to Cel_Tempo_Enduro (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% Hints: get(hObject,'String') returns contents of Cel_Tempo_Enduro as text
%        str2double(get(hObject,'String')) returns contents of Cel_Tempo_Enduro as a double


% --- Executes during object creation, after setting all properties.
function Cel_Tempo_Enduro_CreateFcn(hObject, eventdata, handles)
% hObject    handle to Cel_Tempo_Enduro (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    empty - handles not created until after all CreateFcns called

% Hint: edit controls usually have a white background on Windows.
%       See ISPC and COMPUTER.
if ispc && isequal(get(hObject,'BackgroundColor'), get(0,'defaultUicontrolBackgroundColor'))
    set(hObject,'BackgroundColor','white');
end


% --- Executes on button press in Bot_ON.
function Bot_ON_Callback(hObject, eventdata, handles)
% hObject    handle to Bot_ON (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

% VARIAVEIS GLOBAIS

global serialCom;
global controle;
global valores;
global i;
global tempo;
global ValorBotao;
global TempoEnduro;

global TempoM;


  global           CHOKE
  CHOKE =0;
  global           VELOCIDADE
  VELOCIDADE=0;
  global           ROTACAO
  ROTACAO=0;
  global           DISTRIBUICAO
  DISTRIBUICAO=0;
   global          COMBUSTIVEL
   COMBUSTIVEL=0;
   global          POSICAO
   POSICAO=0;
    global         BOX
    BOX=0;
  global  Kmrodados;
 
  global TempoL;
  
  global TempoLS;
  global TempoM2;
  TempoM2=0;

  TempoLS=0;
  TempoL=0;
  Kmrodados=0;
TempoM=0;

TempoEnduro=0;
% Valores iniciais das variaveis

tempo=0;
tempo1=0;
controle=2;
i=1;
kmrodadosatual=0;
kmrodadostotal=0;
kmrodadostotalStr = 0;
 
% Abrir porta serial
  try
        delete(instrfind({'port'},{'COM6'}));
        serialCom = serial('com6');
   % Define Parametros do canal de comunicação
        set(serialCom,'BaudRate',9600);       
        set(serialCom,'DataBits',8);            
        set(serialCom,'Parity','none');          
        set(serialCom,'StopBits',1);         
        set(serialCom,'FlowControl','none');     
        %set(serialCom,'InputBufferSize',38.5); %5.5 por cada variavel
        
        %Abre a porta serial
        fopen(serialCom);
        handles.serialCom=serialCom;
        guidata(hObject, handles);
       
 
     
      while controle==2
          if (get(serialCom,'BytesAvailable') > 1)
            try  
             valores =  fscanf(serialCom, '%s;%s;%s;%s;%s;%s;%s;\n'); %%% pega valores 
             Split_Buffer = strsplit(valores,';'); % divide cada valor pelo ;
             FlagEstab = Split_Buffer(7); % divide em 7 
          
             %%%%%%%%%pega os valores e joga em uma variavel
             SBOX(i)          = Split_Buffer(1); 
             SVELOCIDADE(i)   = Split_Buffer(2);
             SROTACAO(i)      = Split_Buffer(3); 
             SDISTRIBUICAO(i) = Split_Buffer(4);
             SCOMBUSTIVEL(i)  = Split_Buffer(5);
             SPOSICAO(i)      = Split_Buffer(6);
             SCHOKE(i)        = Split_Buffer(7);
           pause(0.001)
           
           try
     %       pause(0.001);

             CHOKE(i)        = str2double(SCHOKE(i)); 
             VELOCIDADE(i)   = str2double(SVELOCIDADE(i));
             ROTACAO(i)      = str2double(SROTACAO(i)); 
             DISTRIBUICAO(i) = str2double(SDISTRIBUICAO(i));
             COMBUSTIVEL(i)  = str2double(SCOMBUSTIVEL(i));
             POSICAO(i)      = str2double(SPOSICAO(i));
             BOX(i)          = str2double(SBOX(i));
           end
         
          
             pause(0.001)    
             % joga os valores nos dados atuais
         try
             if CHOKE(i)==1
                  set(handles.Cel_Choke,'String','choke','ForegroundColor','black');
             end
             if CHOKE(i)==0
                  set(handles.Cel_Choke,'String','Run','ForegroundColor','red');
             end
             pause(0.001)
             set(handles.Cel_Velocidade,'String',VELOCIDADE(i),'ForegroundColor','black');
             set(handles.Cel_Rotacao,'String',ROTACAO(i),'ForegroundColor','black');
             set(handles.Cel_Distribuicao,'String',DISTRIBUICAO(i),'ForegroundColor','black');
             set(handles.Cel_KmRodados,'String',tempo(i),'ForegroundColor','black');
             
         end
        %  pause(0.001);
             %%%%% define o tempo
try
pegav1=datevec(now) ;
tempo1(i)=pegav1(1,6);
if i>=2
    if (tempo1(i)-tempo1(i-1))>=0
    tempo(i)=tempo1(i)-tempo1((i-1))+tempo((i-1));
    end
    if (tempo1(i)-tempo1((i-1)))<=0
    tempo(i)=tempo1(i)+tempo((i-1));
    end
end
end

        try     
            ValorBotaoTempo = get(handles.Tempo_Enduro, 'Value');

        %    pause(0.001)
            if i>1
                     if ValorBotaoTempo==1 
                       TempoEnduro=tempo(i)-tempo(i-1)+TempoEnduro
                            if TempoEnduro>60
                                TempoM=round((TempoEnduro/60));
                                set(handles.Cel_Tempo_Enduro,'String',TempoM,'ForegroundColor','black');
                            end
                            
                      if TempoEnduro<60
                      set(handles.Cel_Tempo_Enduro,'String',TempoEnduro,'ForegroundColor','black');                         
                      end
                      end
                end
          end
        try
                  if tempo(i)>60
                         TempoM2(i)=round((tempo(i)/60));
                         set(handles.Cel_Tempo_Ligado,'String', TempoM2(i),'ForegroundColor','black');
                  end

        	    if tempo(i)<60
                    TempoM2(i)=0;
                  set(handles.Cel_Tempo_Ligado,'String',tempo(i),'ForegroundColor','black');             
                end
       TempoM2
        end  
          pause(0.001)
         
             %salva valores
          
             %%%%%%% CONTROLE voltar para o box
         try 
             ValorBotao = get(handles.Bot_BOX, 'Value');
          
         
             pause(0.001)
             if ValorBotao==1
          %      pause(0.001)
                    if BOX(i)==0;
                        
                        fprintf(serialCom,'%c','1'); 
            %            pause(0.07);
                        
                    end
                      if BOX(i)==48;                      
                        fprintf(serialCom,'%c','1'); 
                 %       pause(0.07);  
                      end
                      if BOX(i)==49
                          try
                    %         pause(0.01);
                             set(handles.Bot_BOX,'ForegroundColor','red');
                          end

                      end
                      end
         end
             if ValorBotao==0
              %  pause(0.001)
                     if BOX(i)==49;                     
                         fprintf(serialCom,'%c','0'); 
                      %   pause(0.07);                        
                     end
                     if BOX(i)==48;
                        
                      %   pause(0.001);
                         set(handles.Bot_BOX,'ForegroundColor','black');
                  end
             end
           
             
             
            %%%%%%%%% plota os graficos   

      %  pause(0.001)
            
            try
            axes(handles.Graf_Velocidade_e_Rotacao); % escolhe em qual grafico plotar
            
            try
            plot(tempo,VELOCIDADE,'LineWidth',[1.5],'color','red')
            hold on %%% Faz plotar no mesmo grafico    
            plot(tempo,ROTACAO,'LineWidth',[1.5],'color','blue')
            grid on %%% aciona a gradev
              ylim([0 60]);
            legend('Velocidade','Rotação','Location','northwest')
          %  ylim([0 70]); %% limite do eixo y
            title('\fontsize{19}Velocidade & Rotação') %% titulo do grafico
            xlabel('Tempo(s)') %% nome do eixo x
            ylabel('Velocidade(km/h) & Rotação(RPM)') %% nome do eixo y
          
            
            end
            
 
 
            axes(handles.Graf_Volante);
 
            plot(tempo,POSICAO,'LineWidth',[1.5],'color','blue')
            hold on
           %plot(tempo,TEMPO1,'LineWidth',[1.5],'color','red')
            xlabel('Tempo(s)')
            ylabel('Angulo(Graus)')
            ylim([0 1000]);
            title('\fontsize{19}Posição Volante')
            %ylim([-110 110])
           % legend('Diantera(azul)','Traseira(Vermelho)', 'Location','southwest') %% adiciona legenda
            grid on 
             

            axes(handles.Graf_Combustivel);

            plot(tempo,COMBUSTIVEL,'--','LineWidth',[1.5],'color','black')
            xlabel('Tempo(s)')
            title('\fontsize{19}Combustível')
            grid on 
            ylabel('Nível de Combustível') 
            ylim([0 3])
             pause(0.001);
             
 end        
            
            %%%% definir a distancia percorrida
    pause(0.001)
            if i>=2
                 kmrodadosatual=(((((VELOCIDADE(i)+VELOCIDADE(i-1))/3.6)*(tempo(i)-tempo(i-1)))/2)/1000);

                 kmrodadostotal=kmrodadostotal + kmrodadosatual;
                 Kmrodados(i)=kmrodadostotal;

                 kmrodadostotalStr = num2str(kmrodadostotal);
                 pause(0.001);
               
                 set(handles.Cel_KmRodados,'String',kmrodadostotal,'ForegroundColor','black');
                % set(handles.Cel_Tempo_Enduro,'String',TempoM,'ForegroundColor','black');

               
            end

         
             
            end
           i=i+1;
          end
        
      end
  end
          
% --- Executes on button press in Bot_Pause.
function Bot_Pause_Callback(hObject, eventdata, handles)
% hObject    handle to Bot_Pause (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
global serialCom;
global controle;
 pause(0.001);
try 
  fclose(serialCom);
  controle=1;
  delete(instrfind({'port'},{'COM8'}));

end

% --- Executes on button press in Bot_Salvar.
function Bot_Salvar_Callback(hObject, eventdata, handles)
% hObject    handle to Bot_Salvar (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
x=1;
global VELOCIDADE
global ROTACAO
global tempo
global DISTRIBUICAO
global COMBUSTIVEL
global Kmrodados
global POSICAO
global TempoM2
pause(0.001);
Velocidade=[VELOCIDADE'];
Rotacao=[ROTACAO'];
Distribuicao=[DISTRIBUICAO'];
Combustivel=[COMBUSTIVEL'];
KMrodados=[Kmrodados'];
Posicao=[POSICAO'];
Tempo=[TempoM2'];
try


pause(0.1)

pause(0.1)%%
%T = table(Velocidade,Rotacao,Distribuicao,Combustivel,KMrodados,Posicao,Tempo)%% faz uma tabela
T = table(Velocidade,Rotacao,Distribuicao,Combustivel,KMrodados,Posicao,Tempo)%% faz uma tabela

pause(0.1)
pause(0.1)

%T = table(Tempo,Vel,Rotacao,Combust,Distrib,NivelBat,Kmrod);%% faz uma tabela
T
%filename = 'C:\Users\Andre\Desktop\baja\interface grafica TELEMETRIA(matlab)\DADOS.xlsx';
pause(0.01)
filename = 'C:\Users\Spider\Desktop\Baja\18\Telemetria\Dados Competição\19-08.xlsx';
%%% cria a tabela no excel

while x==1
%xlswrite(filename,Matriz)

    try
    writetable(T,filename);
    pause(5);
    catch
     x=1
    end
pause(0.01)
x=2
end


end
% --- Executes on button press in Bot_Zerar.
function Bot_Zerar_Callback(hObject, eventdata, handles)
% hObject    handle to Bot_Zerar (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)
%%%%%%%%%% zera os graficos

    try
    axes(handles.Graf_Velocidade_e_Rotacao);
    cla 
    axes(handles.Graf_Volante);
    cla
    axes(handles.Graf_Combustivel);
    cla
    end
     pause(0.001);
     try
 %%%%%%%%%% zera os valores
 set(handles.Cel_Tempo_Enduro,'String','0');                         

    set(handles.Cel_Tempo_Ligado,'String','0');
    set(handles.Cel_Velocidade,'String','0');
    set(handles.Cel_Rotacao,'String','0');
    set(handles.Cel_Distribuicao,'String','0');
   % set(handles.Cel_Combustivel,'String','0');
    set(handles.Cel_Choke,'String','0');
  %  set(handles.Bateria,'String','0');
    set(handles.Cel_KmRodados,'String','0');
    set(handles.Km,'String','0');
   
   
     pause(0.001);
     
     end


% --- Executes on button press in Bot_BOX.
function Bot_BOX_Callback(hObject, eventdata, handles)
% hObject    handle to Bot_BOX (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)


% --- Executes on button press in Tempo_Enduro.
function Tempo_Enduro_Callback(hObject, eventdata, handles)
% hObject    handle to Tempo_Enduro (see GCBO)
% eventdata  reserved - to be defined in a future version of MATLAB
% handles    structure with handles and user data (see GUIDATA)

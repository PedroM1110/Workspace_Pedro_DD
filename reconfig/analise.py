#!/usr/bin/env python3

#BIBLIOTECAS
import subprocess
import time
import signal
import os
import statistics
from math import sqrt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def analysis(tipo, n, DATA_HORA):
    processos = ["amcl","map_server","move_base","rosmaster"]
    rotas = ["Rota_AB", "Rota_BC", "Rota_CH", "Rota_HD", "Rota_DE", "Rota_EC", "Rota_CA"]
    #DATA_HORA = "2022-04-19-20:29:43"
    #tipo = 'full'
    z = 1.96 #95% de confiança
    
    for rota in rotas:
        for processo in processos:
            path_rota = os.path.expanduser('~')+"/Análise_Simulações/"+ DATA_HORA +"/" +rota
            path_processo = os.path.expanduser('~')+"/Análise_Simulações/"+ DATA_HORA +"/"+rota+"/"+processo
            grep = subprocess.Popen(['cd '+ path_rota + ' ; grep ' + processo + ' ' + "full" 
                                    + ' > ' + path_processo+'/'+processo+'.txt'], shell=True,preexec_fn=os.setpgrp)
            grep.wait()
            sed = subprocess.Popen(['cd '+ path_processo + ' ; sed "{s/^ *//;s/ *$//;s/  */,/g; }" ' + path_processo+'/'+processo+'.txt' 
                                     + ' >> ' + path_processo+'/'+processo+'_'+"full"+'.csv'], shell=True,preexec_fn=os.setpgrp)
            sed.wait()
            
            grep = subprocess.Popen(['cd '+ path_rota + ' ; grep ' + processo + ' ' + "default" 
                                    + ' > ' + path_processo+'/'+processo+'.txt'], shell=True,preexec_fn=os.setpgrp)
            grep.wait()
            sed = subprocess.Popen(['cd '+ path_processo + ' ; sed "{s/^ *//;s/ *$//;s/  */,/g; }" ' + path_processo+'/'+processo+'.txt' 
                                     + ' >> ' + path_processo+'/'+processo+'_'+"default"+'.csv'], shell=True,preexec_fn=os.setpgrp)
            sed.wait()
            
            os.remove(path_processo+'/'+processo+'.txt')
            
            
    #Listas %CPU
    media_cpu_full = []
    std_cpu_full = []
    ic_cpu_full = []
    media_cpu_default = []
    std_cpu_default = []
    ic_cpu_default = []

    #Listas %MEM
    media_mem_full = []
    std_mem_full = []
    ic_mem_full = []
    media_mem_default = []
    std_mem_default = []
    ic_mem_default = []
    
    n = 1
    for rota in rotas:
        for processo in processos:
            n = 1
        
            path_processo = os.path.expanduser('~')+'/Análise_Simulações/'+ DATA_HORA +"/"+rota+"/"+processo    
            file_full = pd.read_csv(path_processo+'/'+processo+'_'+'full''.csv', 
                            names = ['Pid', 'Usuário', 'X', 'XX', 'XXX', 'XXXX', 'XXXXX', 'xxx', '%CPU', '%MEM', 'xxXX', 'Processo'])
            file_default = pd.read_csv(path_processo+'/'+processo+'_'+'default''.csv', 
                            names = ['Pid', 'Usuário', 'X', 'XX', 'XXX', 'XXXX', 'XXXXX', 'xxx', '%CPU', '%MEM', 'xxXX', 'Processo'])
   
            media_cpu_full.append(file_full['%CPU'].mean()) 
            std_cpu_full.append(file_full['%CPU'].std())
            ic = z * (file_full['%CPU'].std() / sqrt(len(file_full['%CPU'])))
            ic_cpu_full.append(ic)
            
            media_mem_full.append(file_full['%MEM'].mean())
            std_mem_full.append(file_full['%MEM'].std())
            ic = z * (file_full['%MEM'].std() / sqrt(len(file_full['%MEM'])))
            ic_mem_full.append(ic)
            
            media_cpu_default.append(file_default['%CPU'].mean())
            std_cpu_default.append(file_default['%CPU'].std())
            ic = z * (file_default['%CPU'].std() / sqrt(len(file_full['%CPU'])))
            ic_cpu_default.append(ic)
            
            media_mem_default.append(file_default['%MEM'].mean())
            std_mem_default.append(file_default['%MEM'].std())
            ic = z * (file_default['%MEM'].std() / sqrt(len(file_full['%MEM'])))
            ic_mem_default.append(ic)
            
        n += 1
 
    aux_processo = 0
    n = 0
    for rota in rotas:
        
        graph_cpu = pd.DataFrame({'%CPU_' + rota:['amcl', 'map_server', 'move_base', 'rosmaster'], 
                                'Full':[media_cpu_full[aux_processo], 
                                        media_cpu_full[aux_processo+1], 
                                        media_cpu_full[aux_processo+2],
                                        media_cpu_full[aux_processo+3]], 
                                'Default': [media_cpu_default[aux_processo], 
                                            media_cpu_default[aux_processo+1], 
                                            media_cpu_default[aux_processo+2],
                                            media_cpu_default[aux_processo+3]],
                                'Intervalo_Confiança_full':[ic_cpu_full[aux_processo], 
                                                            ic_cpu_full[aux_processo+1], 
                                                            ic_cpu_full[aux_processo+2], 
                                                            ic_cpu_full[aux_processo+3]],
                                'Intervalo_Confiança_default': [ic_cpu_default[aux_processo], 
                                                                ic_cpu_default[aux_processo+1], 
                                                                ic_cpu_default[aux_processo+2], 
                                                                ic_cpu_default[aux_processo+3]]})
        
        graph_cpu.plot.bar(x='%CPU_' + rota, y=['Full','Default'], rot=0, 
                      yerr = [[ic_cpu_full[aux_processo], 
                              ic_cpu_full[aux_processo+1], 
                              ic_cpu_full[aux_processo+2], 
                              ic_cpu_full[aux_processo+3]],  
                              
                              [ic_cpu_default[aux_processo], 
                              ic_cpu_default[aux_processo+1], 
                              ic_cpu_default[aux_processo+2], 
                              ic_cpu_default[aux_processo+3]]],
                      )
        plt.savefig(os.path.expanduser('~')+'/Análise_Simulações/'+ DATA_HORA+"/"+ rota + "/Grafico_"+rota+"_CPU.png")
        plt.close()
        graph_mem = pd.DataFrame({'%MEM_' + rota:['amcl', 'map_server', 'move_base', 'rosmaster'], 
                                'Full':[media_mem_full[aux_processo], 
                                        media_mem_full[aux_processo+1], 
                                        media_mem_full[aux_processo+2],
                                        media_mem_full[aux_processo+3]], 
                                'Default': [media_mem_default[aux_processo], 
                                            media_mem_default[aux_processo+1], 
                                            media_mem_default[aux_processo+2],
                                            media_mem_default[aux_processo+3]],
                                'Intervalo_Confiança_full':[ic_mem_full[aux_processo], 
                                                            ic_mem_full[aux_processo+1], 
                                                            ic_mem_full[aux_processo+2], 
                                                            ic_mem_full[aux_processo+3]],
                                'Intervalo_Confiança_default': [ic_mem_default[aux_processo], 
                                                                ic_mem_default[aux_processo+1], 
                                                                ic_mem_default[aux_processo+2], 
                                                                ic_mem_default[aux_processo+3]]})
        
        graph_mem.plot.bar(x='%MEM_' + rota, y=['Full','Default'], rot=0, 
                      yerr = [[ic_mem_full[aux_processo], 
                              ic_mem_full[aux_processo+1], 
                              ic_mem_full[aux_processo+2], 
                              ic_mem_full[aux_processo+3]],  
                              
                              [ic_mem_full[aux_processo], 
                              ic_mem_full[aux_processo+1], 
                              ic_mem_full[aux_processo+2], 
                              ic_mem_full[aux_processo+3]]],
                      )
        aux_processo += 4
        plt.savefig(os.path.expanduser('~')+'/Análise_Simulações/'+ DATA_HORA +"/"+ rota + "/Grafico_"+rota+"_MEM.png") 
        plt.close()
        graph_cpu.to_csv(os.path.expanduser('~')+'/Análise_Simulações/'+ DATA_HORA +"/"+ rota + '/Resumo_CPU.csv')
        graph_mem.to_csv(os.path.expanduser('~')+'/Análise_Simulações/'+ DATA_HORA +"/"+ rota + '/Resumo_MEM.csv')
        n += 1
    
    
########TIME ANALYSIS########################################################
    rota1 = []
    rota2 = []
    rota3 = []
    rota4 = []
    rota5 = []
    rota6 = []
    rota7 = []
    rotas = [rota1, rota2, rota3, rota4, rota5, rota6, rota7]
    
    time_file = open(os.path.expanduser('~')+"/Análise_Simulações/"+DATA_HORA+"/time_file_"+"full"+".txt",'r')
    for line in time_file:
        for rota in rotas:
            if line[0] == str((rotas.index(rota)+1)): 
                if len(line) == 8:
                    string =  line[3]+line[4]+'.'+line[6]
                    rota.append(float(string))
                elif len(line) == 9: 
                    string =  line[3]+line[4]+line[5]+'.'+line[7]
                    rota.append(float(string))
                
    time_file.close()
            
    medias_full = [0]*7
    desvios_full = [0]*7
    n_amostras_full = [0]*7
    ic_full = [0]*7
    z = 1.96 #95% de confiança

    for rota in rotas:
        medias_full[rotas.index(rota)] = statistics.mean(rota) 
        desvios_full[rotas.index(rota)] = statistics.pstdev(rota)
        n_amostras_full[rotas.index(rota)] = len(rota)

    items = range(0,7,1)
    for item in items:
        ic_full[items.index(item)] = z*(desvios_full[items.index(item)]/sqrt(n_amostras_full[items.index(item)]))
   
    tempos = open(os.path.expanduser('~')+"/Análise_Simulações/" +DATA_HORA +"/Summary_time_file.txt",'a')
    tempos.write("----------------FULL-------------------------------\n")
    for media in medias_full:
        tempos.write("Média de tempo gasto na rota "+str((medias_full.index(media)+1))+": "
                        +str(round(media,2))+" IC: "+str(round(ic_full[medias_full.index(media)],2))+"\n")
    tempos.write("¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨\n")
    tempos.close()
    
    rota1 = []
    rota2 = []
    rota3 = []
    rota4 = []
    rota5 = []
    rota6 = []
    rota7 = []
    rotas = [rota1, rota2, rota3, rota4, rota5, rota6, rota7]
    
    time_file = open(os.path.expanduser('~')+"/Análise_Simulações/"+DATA_HORA+"/time_file_"+"default"+".txt",'r')
    for line in time_file:
        for rota in rotas:
            if line[0] == str((rotas.index(rota)+1)): 
                if len(line) == 8:
                    string =  line[3]+line[4]+'.'+line[6]
                    rota.append(float(string))
                elif len(line) == 9: 
                    string =  line[3]+line[4]+line[5]+'.'+line[7]
                    rota.append(float(string))
                
    time_file.close()
            
    medias_default = [0]*7
    desvios_default = [0]*7
    n_amostras_default = [0]*7
    ic_default = [0]*7
    z = 1.96 #95% de confiança

    for rota in rotas:
        medias_default[rotas.index(rota)] = statistics.mean(rota) 
        desvios_default[rotas.index(rota)] = statistics.pstdev(rota)
        n_amostras_default[rotas.index(rota)] = len(rota)

    items = range(0,7,1)
    for item in items:
        ic_default[items.index(item)] = z*(desvios_default[items.index(item)]/sqrt(n_amostras_default[items.index(item)]))
   
    tempos = open(os.path.expanduser('~')+"/Análise_Simulações/" +DATA_HORA +"/Summary_time_file.txt",'a')
    tempos.write("----------------DEFAULT-------------------------------\n")
    for media in medias_default:
        tempos.write("Média de tempo gasto na rota "+str((medias_default.index(media)+1))+": "
                        +str(round(media,2))+" IC: "+str(round(ic_default[medias_default.index(media)],2))+"\n")
    tempos.write("¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨¨\n")
    tempos.close()

    plt.close()
    graph_times = pd.DataFrame({'Medias_de_Tempo': ['Rota AB', 'Rota BC', 'Rota CH', 'Rota HD', 'Rota DE', 'Rota EC', 'Rota CA'], 
                                'Medias_full': medias_full, 
                                'IC_full': ic_full, 
                                'Medias_default': medias_default, 
                                'IC_default': ic_default})
    print(graph_times)
    graph_times.plot.bar(x='Medias_de_Tempo', 
                         y=['Medias_full','Medias_default'], 
                         rot=0, 
                         yerr = [ic_full, ic_default],)
    
    graph_times.to_csv(os.path.expanduser('~')+'/Análise_Simulações/'+ DATA_HORA + '/Tempos.csv')
    plt.savefig(os.path.expanduser('~')+'/Análise_Simulações/'+ DATA_HORA +"/Times.png", bbox_inches = "tight", dpi = 800 )
    
    
    
'''def plot_both(DATA_HORA):

    comandos = ["move_base","amcl","map_server","rosmaster"]
    

    for comando in comandos:
        #########################################################################################################
        top_file = open("/home/pedro/Análise_Simulações/"+comando+"_top_"+"full"+".txt",'r')
        lista_full = []

        for line in top_file: 
            if line[49] == " ":
                if line[50] == " ": string = line[51]+'.'+line[53]
                else: string = line[50]+line[51]+'.'+line[53]
            else:
                string = line[49]+line[50]+line[51]+'.'+line[53]
            lista_full.append(float(string))

        top_file.close()

        media_full = statistics.mean(lista_full)

        lista2_full = [float(media_full)]*len(lista_full)
        ######################################################################################################

        ######################################################################################################
        top_file = open("/home/pedro/Análise_Simulações/"+comando+"_top_"+"default"+".txt",'r')
        lista = []

        for line in top_file: 
            if line[49] == " ":
                if line[50] == " ": string = line[51]+'.'+line[53]
                else: string = line[50]+line[51]+'.'+line[53]
            else:
                string = line[49]+line[50]+line[51]+'.'+line[53]
            lista.append(float(string))

        top_file.close()

        media = statistics.mean(lista)

        lista2 = [float(media)]*len(lista)
        ######################################################################################################

        w=5
        fig1, grafico = plt.subplots()
        grafico.hist(lista,color='blue',label='Default',bins=np.arange(min(lista_full), max(lista_full) + w, w))
        grafico.hist(lista_full,color='red',label='Full',alpha=0.5,bins=np.arange(min(lista_full), max(lista_full) + w, w))
        #grafico.axvline(x=(media_full + 0.17),color='r',ls='--' )
        #grafico.axvline(x=(media_full - 0.17),color='g',ls='--' )
        grafico.set_title(comando)
        grafico.set_ylabel('Amostras')
        grafico.set_xlabel('%CPU')
        grafico.legend()

        

        fig1.savefig('/home/pedro/Análise_Simulações/Gráficos/'+comando+"_both"+'.png', transparent=False, dpi=800, bbox_inches="tight")
        '''


#if __name__ == '__main__':
    #analysis(0,0,0)
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 21:50:14 2022

@author: Nico
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Jul  4 11:45:23 2022

@author: Nico
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 09:24:12 2022

@author: Nico
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Jun 30 16:33:12 2022

@author: Nico
"""
import random as random 
from random import choices
# Importamos Numpy para hacer cuentas con vectores, matrices
import numpy as np
# Importamos Matplotlib para visualizar
import matplotlib.pyplot as plt
# importamos seaborn
import seaborn as sns
# importar picos

import picos



#################################### Parte 1: cadenas de Markov - condiciones para que se arme un ciclón #########################################
##################################################################################################################


exp = 100
#

puertos = ["PuertoMontevideo" 
           ,"PuertoLapaloma" 
           ,"PuertoPuntadeldiablo"] 
# nuestro vector p0 va a tener la probabilidad de que arranque en un lugar que puede ser 1 si sabemos donde arranca o ser 0,2 en cada valor si es aleatorio

i = random.randint(0, 2)
p0 = [0,0,0]
p0[i] = 1

p1 = [0,0,0]
p1[i] = 1

i = random.randint(0, 3)
p2 = [0,0,0,0]
p2[i] = 1

# defino desde los datos la matriz de transicion de 1 paso

P1 = np.array([[0.49, 0.33,0.18],
               [0.35, 0.30, 0.35],
               [0.26, 0.52, 0.22]]) 


P2 = np.array([[0.52, 0.29,0.19],
               [0.41, 0.47, 0.12],
               [0.22, 0.14, 0.64]])


P3 = np.array([[0.5, 0.5,0, 0],
               [0.16, 0.58, 0.26, 0],
               [0,0.31, 0.38, 0.31], 
               [0, 0, 0.26,0.74]])


# determinar la cantidad total de estados
estados1 = np.shape(P1)[0]

estados2 = np.shape(P2)[0]

estados3 = np.shape(P3)[0]


# cantidad de pasos a simular
m = 12

# en esta matriz vamos a guardar el vector de estados para cada paso t
vectorestado1 = np.zeros((m,estados1,exp))
vectorestado2 = np.zeros((m,estados2,exp))
vectorestado3 = np.zeros((m,estados3,exp))

estadofinal1 = 2
estadofinal2 = 1
estadofinal3 = 0

# Vectores donde luego imprimo resultados 

cantpasos = np.zeros(exp)

puertosfinales = []

cantvalorobjetivo = np.zeros(exp)

cantargumentos = []


#loop para cada experimento
for e in range(0,exp):

    
    # for loop para cantidad de pasos

    for i in range(0,m):
      
        if i == 0:
            
         # el vector de estado en el tiempo inicial es p0
         vectorestado1[i, :, e] = p0 
         vectorestado2[i, :, e] = p1
         vectorestado3[i, :, e] = p2
               

        else:   # para el resto de los pasos

        # guardarse cuantas veces corrio que no dio ciclon para dar una estadística final 
        # si se cumplen las 3 condiciones tirame a un puerto con un if
 
        # conociendo el estado previo del sistema "estado_actual[i-1]" 
        # calculo la distribucion de proba de transicion hacia cada estad
         proba_transicion_1 = np.dot(vectorestado1[i-1,:,e],P1)
         proba_transicion_2 = np.dot(vectorestado2[i-1,:,e],P2)
         proba_transicion_3 = np.dot(vectorestado3[i-1,:,e],P3)
     
         # muestreamos la distribucion de proba de transicion 
         # basandonos en el estado del sistema en t=t-1
         estado_actual_1 = choices([0,1,2], proba_transicion_1)
         estado_actual_2 = choices([0,1,2], proba_transicion_2)
         estado_actual_3 = choices([0,1,2,3], proba_transicion_3)

        # el estado actual lo guardo en la fila "i", "columna estado actual" y capa "e"
         vectorestado1[i, estado_actual_1 ,e] = 1
         vectorestado2[i, estado_actual_2 ,e] = 1
         vectorestado3[i, estado_actual_3 ,e] = 1
         
       

        # Si se cumplen los tres estados que yo quiero tirame un puerto 
        
        if vectorestado1[i, estadofinal1 ,e] == 1 and vectorestado2[i, estadofinal2 ,e] == 1 and vectorestado3[i, estadofinal3 ,e] == 1:
                    
            #Cantidad de pasos en cada experimento hasta que se cumplan las condiciones 
            
            cantpasos[e] = i 
            print(cantpasos,"Cantidad pasos")
            
              
        
            # Graficos 
            
            sns.heatmap(vectorestado1[:,:,e])
            plt.title('Vector de probabilidad del clima en 12 meses ')
            plt.xlabel('Estados')
            plt.ylabel('12 Pasos simulados')
            plt.show()
        
            sns.heatmap(vectorestado2[:,:,e])
            plt.title('Vector de probabilidad de la direccion del viento en 12 meses ')
            plt.xlabel('Estados')
            plt.ylabel('12 Pasos simulados')
            plt.show()
        
        
            sns.heatmap(vectorestado3[:,:,e])
            plt.title('Vector de probabilidad de temperatura del agua en 12 meses ')
            plt.xlabel('Estados')
            plt.ylabel('12 Pasos simulados')
            plt.show()
            
               
            
       
            # Selección de puerto aleatoriamente si se cumple el if 
            
            puertofinal = random.choice(puertos)
            print(puertofinal, "Puertodestino")
         
#################################### Parte 2: Optimización - rutas #########################################
####################################################################################################################
        

            
            P = picos.Problem()
            
            #Variables aleatorias asignadas a cada tramo 
            
            c0 = np.random.normal(loc = 1.5, scale = 1, size= 1) # de tacuerambo a paso de los toros 
        
            c1 = np.random.normal(loc = 2.6, scale = 1, size= 1) # de tacuerambo a melo
        
            # de paso de los toros a los otros 3 nodos (fui de izq a der)
            c2 = np.random.normal(loc = 2.16, scale = 1, size= 1)
            c3 = np.random.normal(loc = 3, scale = 1, size= 1) 
            c4 = np.random.normal(loc = 5.16, scale = 1, size= 1) 
        
            # de melo a los otros 3 nodos (fui de izq a der)
            c5 = np.random.normal(loc = 4.5, scale = 1, size= 1)
            c6 = np.random.normal(loc = 3, scale = 1, size= 1)
            c7 = np.random.normal(loc = 2.3, scale = 1, size= 1)
         
            # de los nodos del medio a los puertos (primero de esa fila)
            c8 = np.random.normal(loc = 1.5, scale = 1, size= 1)
            c9 = np.random.normal(loc = 3.6, scale = 1, size= 1)
            c10 = np.random.normal(loc = 4.5, scale = 1, size= 1)
        
            #segundo de la fila
            c11 = np.random.normal(loc = 4, scale = 1, size= 1)
            c12 = np.random.normal(loc = 4, scale = 1, size= 1)
            c13 = np.random.normal(loc = 4.8, scale = 1, size= 1)
        
            # tercero de la fila
            c14 = np.random.normal(loc = 3.6, scale = 1, size= 1) # estime
            c15 = np.random.normal(loc = 2, scale = 1, size= 1) # estime
            c16 = np.random.normal(loc = 1.5, scale = 1, size= 1)
        
        
        
            c = np.concatenate((c0,c1,c2,c3,c4,c5,
                                c6,c7,c8,c9,c10,c11,
                                c12,c13,c14,c15,c16)) 
        
            x = picos.BinaryVariable('x', 17)
            
            
            
            # Primeras reestricciones
        
            P.set_objective('min', c | x)
         
            P.add_constraint(x[0]+x[1]==1)
            P.add_constraint(x[2]+x[3]+x[4]+x[5]+x[6]+x[7]==1)
            P.add_constraint(x[8]+x[9]+x[10]+x[11]+x[12]+x[13]+x[14]+x[15]+x[16]==1)
            P.add_constraint(x[1] == x[5] + x[6]+ x[7])
            P.add_constraint(x[0] == x[2] + x[3]+ x[4])
            P.add_constraint(x[2]+x[5] == x[8]+x[9]+ x[10])
            P.add_constraint(x[3]+x[6] == x[11]+x[12]+ x[13])
            P.add_constraint(x[4]+x[7] == x[14]+x[15]+ x[16])
         
            #Reestricciones puertos 
         
            #puerto 1 es montevideo 
            if puertofinal == "PuertoMontevideo" :
         
             P.add_constraint(x[8]+x[11]+x[14]==1)
             P.add_constraint(x[9]+x[10]+x[12]+x[13]+x[15]+x[16]==0)
         
         
            #puerto dos es la paloma     
            elif puertofinal == "PuertoLapaloma":
         
             P.add_constraint(x[9]+x[12]+x[15]==1)
             P.add_constraint(x[8]+x[10]+x[11]+x[13]+x[14]+x[16]==0)
          
           
            #puerto tres es la punta del diablo   
            elif puertofinal == "PuertoPuntadeldiablo" :
         
             P.add_constraint(x[10]+x[13]+x[16]==1)
             P.add_constraint(x[8]+x[9]+x[11]+x[12]+ x[14]+x[15]==0)
           
           
            print("")
            
            P.options.verbosity=1
            print(P)
            #P SOLVE
            P.solve()
            print(x,"Argumentos")
            #VALOR FUNCION OBJETIVO
            print(round(P.value), "Valorobjetivo")
            
            print(" ")
         
            #Anotar a cada experimento valor funcion objetivo y argumentos de variable de decision 
         
            cantvalorobjetivo[e] = (P.value)
            cantargumentos.append(np.array(x))
            
            # Los argumentos en una simulacion 
           
            print(cantargumentos, "Argumentos")
            
            # Los valores objetivos en una simulacion 
           
            print(cantvalorobjetivo, "Valor objetivo")
            
            # Los puertos en una simulacion 
            
            puertosfinales.append(np.array(puertofinal))
            print(puertosfinales, "Puertosfinales")
             
            break

 
   

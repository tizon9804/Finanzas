from numpy import genfromtxt
import random
from collections import Counter
import numpy as np
import itertools
import csv
import pesos
for iterDesv in range(0,5):
    print("numMejores",iterDesv)
    rp = 0.016
    pesosP = pesos.p(rp)
    bd = genfromtxt('bd2.csv', delimiter=',')
    print (bd.shape)
    li = bd[0]
    acciones = bd[1:]
    combGroup = 3
    numIteraciones = 5
    numMejores = 50*numIteraciones
    porcentajeInicialMejores = 600
    minMejoresInit=500
    print("acciones", acciones.shape)
    for iter in range(0,numIteraciones):
        print("iteracion:",iter,"---------------------------------------")
        print("grupo de combinaciones",combGroup)
        print("num acciones",li.shape)
        #halla las combinaciones posibles del listado de acciones
        combinaciones = list(itertools.combinations(li,combGroup))
        comb = np.asarray(combinaciones)
        print("num combinaciones",comb.shape)
        comb = comb.astype(np.int32)
        #revuelve aletoriamente las combinaciones
        positionRand = random.sample(range(0,comb.shape[0]),comb.shape[0])
        mejores = []
        #recorre las combinaciones desordenadas
        for r in positionRand:
            #obtiene la combinacion
            c = comb[r]
            # obtiene las acciones de esa combinacion
            grupAcc = acciones[:,c]
            #halla la desviacion de esa combinacion
            desv = pesosP.hallarDesv(grupAcc)
            #la guarda en un arreglo combinacion,desvicacion
            res=[c,desv]
            termino = False;
            #del grupo de mejores si ya se agregaron el min de mejores empieza a agregar las mejores y a quitar las peores
            grupoInicialMejores = comb.shape[0] / porcentajeInicialMejores
            if len(mejores) > minMejoresInit or (iter == 0 and len(mejores)> grupoInicialMejores):
                for i in range(0,len(mejores)):
                    if desv < mejores[i][1]:
                        mejores.insert(i,res)
                        mejores.pop()
                        termino = True
                        break
            #si la desviacion no estuvo dentro de las mejores la agrega al final
            if not termino:
                mejores.append(res)
                #organiza las mejores de menor a mayor
                mejores = sorted(mejores, key=lambda x: x[1])
            if len(mejores)>=(grupoInicialMejores) and iter == 0:
                print("grupo inicial",comb.shape[0]/porcentajeInicialMejores)
                break
            if len(mejores)>=(1000) and iter > 0:
                break
        newacciones=[]
        accionesL = []
        for m in mejores:
            for me in m[0]:
                accionesL.append(me)

        counts = Counter(accionesL)
        new_list = sorted(accionesL, key=lambda x: -counts[x])
        duplicates=[]
        for i in new_list:
          if i not in duplicates:
            duplicates.append(i)
        print("lista de acciones mejores",len(duplicates))
        li = np.asarray(duplicates)[1:numMejores]
        numMejores-=50
        combGroup+=1
        if numMejores==0:
            break

    mejnump = np.asarray(mejores)
    with open('resultado3.csv', 'a') as csvfile:
        writerres = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        print("menor",mejnump[0][1])
        print("mayor",mejnump[mejnump.shape[0]-1][1])
        writerres.writerow(["menor",str(mejnump[0][1])])
        writerres.writerow(["mayor",str(mejnump[mejnump.shape[0]-1][1])])
        desv = pesosP.hallarDesv(acciones[:,li])
        print ("rp:",rp,"-",[li,desv])
        writerres.writerow(["rp:",rp,"-",[li,desv]])
        rp = 16
        for x in range(0,100):
            pesosP.rp = rp/1000
            desv = pesosP.hallarDesv(acciones[:, li])
            print("rp:", rp/1000, "-",desv)
            writerres.writerow(["rp:", rp/1000, "-",desv])
            rp+=1













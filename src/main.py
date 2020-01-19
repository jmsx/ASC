import numpy
from utiles import *
from funciones import *
import random
from tqdm import tqdm

N = 50
T = 25
espacio = (0, 1)
generaciones = 100
dimension = 30
CR = 0.5
Fm = 0.5
# Generar vectores pesos
pesos = numpy.empty((N, 2))
for i in range(0, N):
    pesos[i][0] = 0 + (1/(N-1))*i
    pesos[i][1] = 1 - (1/(N-1))*i


#Calcular vecinos
vecinos = numpy.empty((N, T))
for i in range(0, N):
    vecinos[i] = masCercanosA(pesos, pesos[i], T)


#Genera individuos
X = numpy.empty((N, dimension))
for i in range(0, N):
    for j in range(0, dimension):
        X[i][j] = numpy.random.random_sample()

#Evalua funciones
F = numpy.empty((N, 2))
for i in range(0, len(X)):
    F[i][0] = ZDT3_f1(X[i][:])
    F[i][1] = ZDT3_f2(X[i][:])

#Inicializa Z
Z = F[0][:]
for i in range(0, len(F)):
    Z = numpy.minimum(F[i][:], Z)


#Cargar el frente de pareto
pareto = cargaPareto()
creaFoto(0, F, Z, pareto)

#Calculo las agregaciones iniciales
agregaciones = numpy.empty((N, ))
for i in range(0, N):
    agregaciones[i] = g_te(F[i][:], pesos[i][:], Z)

#Array para el fichero de salida
lineas = list()

#Iteraccion
print("Evoluciones:")
for j in tqdm(range(0, generaciones)):
    #Generando lineas para el archivo de salida
    
    for i in range(0, N):
         lineas.append(str(F[i][0]) + "	" + str(F[i][1]) + "	" + str(float(0)))

    #Evolucionando
    for i in range(0, N):
        while True:
            v1 = X[int(random.choice(vecinos[i]))]
            v2 = X[int(random.choice(vecinos[i]))]
            v3 = X[int(random.choice(vecinos[i]))]
            if (v1 is not v2) and (v2 is not v3):
                break
        
        y = muta_y_cruza(X[i] ,v1, v2, v3, espacio, CR , Fm)
        Fy = numpy.empty((2,))
        Fy[0] = ZDT3_f1(y)
        Fy[1] = ZDT3_f2(y)
        Z = numpy.minimum(Fy, Z)
        F_agregacion = g_te(F[i][:], pesos[i][:], Z)
        Fy_agregacion = g_te(Fy, pesos[i][:], Z) 
        if Fy_agregacion < F_agregacion:
            X[i] = y
            F[i][:] = Fy
            agregaciones[i] = Fy_agregacion
        for t in vecinos[i]:
            t = int(t)
            if g_te(Fy, pesos[t][:], Z)  < agregaciones[t]:
                X[t] = y
                F[t][:] = Fy


    creaFoto(j + 1, F, Z, pareto)


escribirSalida(lineas, N, generaciones)
creaGif()

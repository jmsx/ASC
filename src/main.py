import numpy
from utiles import *
from funciones import *
import random
from tqdm import tqdm

N = 100
T = 30
espacio = (0, 1, -2, 2)
generaciones = 100
dimension = 16
CR = 0.5
Fm = 0.5
peso_restricciones = 0.2
problema = "CF6_16D"
SIG = 20

#restricciones incumplidas
restricciones = numpy.zeros((N, 1))

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
        if ("CF6" in problema) and (j != 0):
            X[i][j] = (espacio[3] - espacio[2]) * numpy.random.random_sample() + espacio[2]

#Evalua funciones
F = numpy.empty((N, 2))
for i in range(0, len(X)):
    if problema == "ZDT3":
        F[i][0] = ZDT3_f1(X[i][:])
        F[i][1] = ZDT3_f2(X[i][:])
    elif "CF6" in problema:
        F[i][0] = CF6_f1(X[i][:])
        F[i][1] = CF6_f2(X[i][:])

#Inicializa Z
Z = F[0][:]
for i in range(0, len(F)):
    Z = numpy.minimum(F[i][:], Z)

#CargaFrente competencia
frente_NS = cargaCompetencia(problema, N, generaciones)
#Cargar el frente de pareto
pareto = cargaPareto(problema)
creaFoto(0, F, Z, pareto, frente_NS)




#Calculo las agregaciones iniciales
agregaciones = numpy.empty((N, ))
for i in range(0, N):
    agregaciones[i] = g_te(F[i][:], pesos[i][:], Z, cuentaRestricciones(X[i][:], problema), peso_restricciones)

#Array para el fichero de salida
lineas = list()

#Iteraccion
print("Evoluciones:")
for j in tqdm(range(0, generaciones)):

    #Generando lineas para el archivo de salida
    for i in range(0, N):
         lineas.append(str(F[i][0]) + "	" + str(F[i][1]) + "	" + str(float(cuentaRestricciones(X[i][:], problema))))



    #Cambio de SIG
    aux1  = numpy.array(X)


    #Evolucionando
    for i in range(0, N):
        while True:
            v1 = X[int(random.choice(vecinos[i]))]
            v2 = X[int(random.choice(vecinos[i]))]
            v3 = X[int(random.choice(vecinos[i]))]
            if (v1 is not v2) and (v2 is not v3):
                break
        
        y = muta_y_cruza(X[i] ,v1, v2, v3, espacio, CR , Fm, problema, SIG)

        Fy = numpy.empty((2,))
        if problema == "ZDT3":
            Fy[0] = ZDT3_f1(y)
            Fy[1] = ZDT3_f2(y)
        else:
            Fy[0] = CF6_f1(y)
            Fy[1] = CF6_f2(y)

        Z = numpy.minimum(Fy, Z)

        F_agregacion = g_te(F[i][:], pesos[i][:], Z, cuentaRestricciones(X[i], problema), peso_restricciones)
        Fy_agregacion = g_te(Fy, pesos[i][:], Z, cuentaRestricciones(y,problema), peso_restricciones) 



        #Comparacion del individuo
        if Fy_agregacion < F_agregacion:
            X[i] = y
            F[i][:] = Fy


        #Altualizando vecinos
        for t in vecinos[i]:
            t = int(t)
            if g_te(Fy, pesos[t][:], Z, cuentaRestricciones(y, problema), peso_restricciones)  < g_te(F[t][:], pesos[t][:], Z, cuentaRestricciones(X[t], problema), peso_restricciones):
                X[t] = y
                F[t][:] = Fy



    #Variacion de SIG
    """
    diff = aux1 - X
    contador = 0
    for e in numpy.nditer(diff):
        if e == 0:
            contador += 1
    try:
        contador = float(contador / math.pow(N, 2))
        SIG = (5)*contador + 5
    except:
        SIG = 5
    """
    

    #Generando grafica de la generacion

    creaFoto(j + 1, F, Z, pareto, frente_NS)


#Escribiendo fichero de salida
escribirSalida(lineas, N, generaciones, problema)
crearFicheroMetricas(N,  generaciones, problema)
ejecutaMetricas(N,  generaciones, problema)
#Generando animacion con las distintas generaciones
creaGif()
#Añadiendo minimos al archivo de estadisticas
guardaEstadistica(Z, N, generaciones, problema)

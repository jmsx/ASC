import math
import numpy


def distanciaEuclidea(v1, v2):
    suma = 0
    for i in range(0, len(v1)):
        suma  += pow(v1[i] - v2[i], 2)
    return math.sqrt(suma)

def masCercanosA(matriz, v, n):
    l = []
    res = []
    for i in range(0, len(matriz)):
        l.append((i, distanciaEuclidea(matriz[i], v)))
    l = sorted(l, key= lambda elemento: elemento[1])

    for t in l:
        res.append(t[0])
    
    return res[:n]

def g_te(F, pesos, Z):
    aux = numpy.empty((len(F),))
    for i in range(0, len(F)):
        aux[i] = pesos[i] * abs(F[i] - Z[i])
    return numpy.amax(aux)

def muta_y_cruza(v1, v2, v3):
    v1 = numpy.array(v1)
    v2 = numpy.array(v2)
    v3 = numpy.array(v3)
    F = 0.5
    v = v1 + F * (v2 - v3)
    #TODO: mutacion gaussiana.
    return v 


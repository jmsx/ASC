import math


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
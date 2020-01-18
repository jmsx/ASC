import math
import numpy
import glob
import os
from PIL import Image
import matplotlib.pyplot as plt
from shutil import rmtree

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

def muta_y_cruza(y, v1, v2, v3, espacio, CR, fm):
    v1 = numpy.array(v1)
    v2 = numpy.array(v2)
    v3 = numpy.array(v3)
    F = fm
    v = v1 + F * (v2 - v3)

    for i in range(0, len(v)):
        rnd = numpy.random.random_sample()
        if rnd <= CR:
            y[i] = v[i]

    y = mutacion_gausiana(y, espacio)

    for i in range(0, len(y)):
        if y[i] < espacio[0]:
            y[i] = espacio[0]
        elif y[i] > espacio[1]:
             y[i] = espacio[1]
    return y 

def mutacion_gausiana(y, espacio):
    o = (espacio[1] - espacio[0]) / 20.0
    for i in range(0, len(y)):
        rnd = numpy.random.random_sample()
        if rnd <= (1/len(y)):
            aux = y[i]
            y[i] +=  numpy.random.normal(0.0, o)
    return y

def creaGif():

    fp_in = "img/grafica-*.png"
    fp_out = "img/grafica.gif"
    img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
    img.save(fp=fp_out, format='GIF', append_images=imgs,
            save_all=True, duration=400, loop=0)


def creaFoto(i, F, Z, pareto):
    if i == 0:
        folder = 'img' 
        for the_file in os.listdir(folder):
            file_path = os.path.join(folder, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except:
                pass
    axisF1 = numpy.amax(F[: , 0])
    axisF2 = numpy.amax(F[: , 1])
    plt.figure(i)
    plt.plot(F[: , 0], F[: , 1], 'bo')
    plt.plot(pareto[: , 0],pareto[: , 1], 'go')
    plt.plot(Z[0], Z[1], 'ro')
    plt.axis([0, axisF1, -1, axisF2])
    plt.savefig('img/grafica-' + str(i) + '.png')
    plt.close()


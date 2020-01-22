import math
import numpy
import glob
import os
from PIL import Image
import matplotlib.pyplot as plt
from shutil import rmtree
from tqdm import tqdm

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

def muta_y_cruza(y, v1, v2, v3, espacio, CR, fm, problema):
    v1 = numpy.array(v1)
    v2 = numpy.array(v2)
    v3 = numpy.array(v3)
    F = fm
    v = v1 + F * (v2 - v3)
    
    y = numpy.array(y)
    for i in range(0, len(v)):
        rnd = numpy.random.random_sample()
        if rnd <= CR:
            y[i] = v[i]

    y = mutacion_gausiana(y, espacio)

    #Ajustando al espacio de busqueda
    if problema == "ZDT3":
        for i in range(0, len(y)):
            if y[i] < espacio[0]:
                y[i] = espacio[0]
            elif y[i] > espacio[1]:
                y[i] = espacio[1]
    else:
        if y[i] < espacio[0]:
            y[i] = espacio[0]
        elif y[i] > espacio[1]:
            y[i] = espacio[1]
        for i in range(1, len(y)):
            if y[i] < espacio[2]:
                y[i] = espacio[2]
            elif y[i] > espacio[3]:
                y[i] = espacio[3]

    return y 

def mutacion_gausiana(y, espacio):
    o = (espacio[1] - espacio[0]) / 20.0
    for i in range(0, len(y)):
        rnd = numpy.random.random_sample()
        if rnd <= (1/len(y)):
            y[i] +=  numpy.random.normal(0.0, o)
    return y

def creaGif():
    print("Generando Gif:")
    fp_in = "img/grafica-*.png"
    fp_out = "img/grafica.gif"
    img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
    img.save(fp=fp_out, format='GIF', append_images=imgs,
            save_all=True, duration=100, loop=0)


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
    plt.plot(pareto[: , 0],pareto[: , 1], 'g.')
    plt.plot(F[: , 0], F[: , 1], 'b.')
    plt.plot(Z[0], Z[1], 'r.')
    plt.axis([0, 1, -1, 2.5])
    plt.ylabel('f2')
    plt.xlabel('f1')
    plt.suptitle('Generecion ' + str(i))
    num = '{:05d}'.format(i)
    plt.savefig('img/grafica-' + num + '.png')
    plt.close()

def escribirSalida(lineas, N, generaciones):
    salida = "out/" + str(N) + "P" + str(generaciones) + "G.out"
    outF = open(salida, "w")
    for line in lineas:
        outF.write(line + "\n")
    outF.close()

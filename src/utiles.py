import math
import numpy
import glob
import os
from PIL import Image
import matplotlib.pyplot as plt
from shutil import rmtree
from tqdm import tqdm
from os import listdir
from os.path import isfile, join
from funciones import *
import decimal



def float_to_str(f):
    ctx = decimal.Context()
    ctx.prec = 20
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')


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

def g_te(F, pesos, Z, restricciones, peso_restricciones):
    aux = numpy.empty((len(F),))
    for i in range(0, len(F)):
        aux[i] = pesos[i] * abs(F[i] - Z[i])
    res = numpy.amax(aux)
    res += peso_restricciones*restricciones
    return res

def muta_y_cruza(y, v1, v2, v3, espacio, CR, fm, problema, SIG):
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

    y = mutacion_gausiana(y, espacio, problema, SIG)

    #Ajustando al espacio de busqueda
    if problema == "ZDT3":
        for i in range(0, len(y)):
            if y[i] < espacio[0]:
                y[i] = espacio[0]
            elif y[i] > espacio[1]:
                y[i] = espacio[1]
    else:
        if y[0] < espacio[0]:
            y[0] = espacio[0]
        elif y[0] > espacio[1]:
            y[0] = espacio[1]
        for i in range(1, len(y)):
            if y[i] < espacio[2]:
                y[i] = espacio[2]
            elif y[i] > espacio[3]:
                y[i] = espacio[3]

    return y 

def mutacion_gausiana(y, espacio, problema, SIG):
    
    o = (espacio[1] - espacio[0]) / SIG
    o_aux = (espacio[3] - espacio[2]) / SIG
    for i in range(0, len(y)):
        rnd = numpy.random.random_sample()
        if rnd <= (1/len(y)):
            if ("CF6" in problema) and (i != 0):
                y[i] +=  numpy.random.normal(0.0, o_aux)
            else:
                y[i] +=  numpy.random.normal(0.0, o)
    return y

def creaGif():
    print("Generando Gif:")
    fp_in = "img/generaciones/grafica-*.png"
    fp_out = "img/generaciones/grafica.gif"
    img, *imgs = [Image.open(f) for f in sorted(glob.glob(fp_in))]
    img.save(fp=fp_out, format='GIF', append_images=imgs,
            save_all=True, duration=100, loop=0)


def creaFoto(i, F, Z, pareto, frente_NS):
    if i == 0:
        folder = 'img/generaciones' 
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
    if len(frente_NS )!= 0:
        plt.plot(frente_NS[:, 0], frente_NS[:, 1], 'y.')
    plt.plot(F[: , 0], F[: , 1], 'b.')
    plt.plot(Z[0], Z[1], 'r.')
    plt.axis([0, 1, -1, 2])
    plt.ylabel('f2')
    plt.xlabel('f1')
    plt.suptitle('Generacion ' + str(i))
    num = '{:05d}'.format(i)
    plt.savefig('img/generaciones/grafica-' + num + '.png')
    plt.close()

def escribirSalida(lineas, N, generaciones, problema):
    salida = "out/" + problema + "/" + str(N) + "P" + str(generaciones) + "G.out"
    salida_final = "out/" + problema + "/" + str(N) + "P" + str(generaciones) + "G_final.out"

    try:
        os.mkdir("out/" + problema)
    except:
        pass

    outF = open(salida, "w")
    for line in lineas:
        outF.write(line + "\n")
    outF.close()

    outF = open(salida_final, "w")
    for line in lineas[N*(generaciones-1):]:
        outF.write(line + "\n")
    outF.close()

def crearFicheroMetricas(N,  generaciones, problema):
    salida = "out/" + str(N) + "P" + str(generaciones) + "G_" + problema + ".in"
    file1 = "out/" + problema + "/" + str(N) + "P" + str(generaciones) + "G.out"
    try:
        mypath = "out/NSGAII_" + problema + "/P" + str(N) + "G" + str(generaciones)
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        while True:
            file2 =  mypath + "/" + numpy.random.choice(onlyfiles)
            if "all" in file2:
                break

        lineas = [2, 1, 2, file1, N, generaciones, file2, N, generaciones, 1]
    except:
        lineas = [1, 1, 2, file1, N, generaciones]
    outF = open(salida, "w")
    for line in lineas:
        outF.write(str(line) + "\n")
    outF.close()

def ejecutaMetricas(N,  generaciones, problema):
    folder = "img/metricas/" + str(N) + "P" + str(generaciones) + "G" 
    try:
        os.mkdir(folder)
    except:
        pass

    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except:
            pass

    try:
        os.mkdir(folder)
    except:
        pass
    cmd = "sudo ./METRICS/metrics < out/" + str(N) + "P" + str(generaciones) + "G_" + problema + ".in > /dev/null"
    os.system(cmd)
    folder = '../src' 
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path) and (".out" in file_path):
                os.unlink(file_path)
        except:
            pass





def cargaCompetencia(problema, N, generaciones):
    try:
        mypath = "out/NSGAII_" + problema + "/P" + str(N) + "G" + str(generaciones)
        onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

        while True:
            file1 =  mypath + "/" + numpy.random.choice(onlyfiles)
            if "final" in file1:
                break
        fileobj = open(file1, "r")
        frente = list()
        for line in fileobj.readlines():
            if "#" not in line:
                rip = line.split("	")
                x = float(rip[0].strip())
                y = float(rip[1].strip())
                frente.append([x, y])
        frente = numpy.array(frente)
    except:
        frente = []
    return frente

def guardaEstadistica(Z, N, generaciones, problema):
    fichero = "estadisticas/" + str(problema) + "/" + str(N) + "P" + str(generaciones) + "G.csv" 
    existe = os.path.isfile(fichero) 
    with open(fichero, "a+") as myfile:
        if not existe:
            myfile.write("F1;F2\n")
        myfile.write(float_to_str(Z[0]) + ";" + float_to_str(Z[1]) + "\n")


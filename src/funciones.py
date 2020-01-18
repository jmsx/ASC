import math
import numpy


def ZDT3_f1(X):
    return X[0]
def ZDT3_f2(X):
    g = ZDT3_g(X)
    f1 = ZDT3_f1(X)
    
    f2 = g*ZDT3_h(f1, g)

    return f2

def ZDT3_g(X):
    g = 0
    for i in range(1, len(X)):
        g += X[i]
    g = g*(9/(len(X) - 1)) + 1
    return g
def ZDT3_h(f1, g):

    sqrt = math.sqrt(f1/g)
    return 1 - sqrt - (f1/g)*math.sin(10*math.pi*f1)

def cargaPareto():
    fileobj = open("resources\PF.dat", "r")
    pareto = list()
    for line in fileobj.readlines():
        rip = line.split("	")
        x = float(rip[0].strip())
        y = float(rip[1].strip())
        pareto.append([x, y])
    pareto = numpy.array(pareto)
    return pareto
        
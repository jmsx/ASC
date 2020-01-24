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

def cargaPareto(problema):
    fileobj = open("resources/PF_" + problema + ".dat", "r")
    pareto = list()
    for line in fileobj.readlines():
        rip = line.split("	")
        x = float(rip[0].strip())
        y = float(rip[1].strip())
        pareto.append([x, y])
    pareto = numpy.array(pareto)
    return pareto


def CF6_f1(x):
    res = x[0]
    y = CF6_y(x)
    for _y in y[2::2]:
        res += pow(_y, 2)
    return res

def CF6_f2(x):
    res = pow((1 - x[0]), 2)
    y = CF6_y(x)
    for _y in y[1::2]:
        res += pow(_y, 2)
    return res

def CF6_y(x):
    n = len(x)
    res = numpy.empty((n,))
    
    for i in range(0, n):
        if (i % 2) == 0:
            res[i] = x[i] - 0.8*math.sin(6*math.pi*x[0] + (((i + 1)*math.pi)/n))
        else:
            res[i] = x[i] - 0.8*math.cos(6*math.pi*x[0] + (((i + 1)*math.pi)/n))
    return res

def CF6_R1(x):
    n = len(x)
    return x[1] - 0.8*x[0]*math.sin(6*math.pi*x[0] + ((2*math.pi)/n)) - numpy.sign(0.5*(1-x[0]) - math.pow((1 - x[0]),2))*math.sqrt(abs(0.5*(1-x[0]) - math.pow((1 - x[0]),2))) >= 0

def CF6_R2(x):
    n = len(x)
    return x[3] - 0.8*x[0]*math.sin(6*math.pi*x[0] + ((4*math.pi)/n)) - numpy.sign(0.25*math.sqrt(1-x[0]) - (1 - x[0]))*math.sqrt(abs(0.25*math.sqrt(1-x[0]) - (1 - x[0]))) >= 0

def cuentaRestricciones(X):
    res = 0
    if CF6_R1(X):
        res += 1
    if CF6_R2(X):
        res += 1
    return res


import math
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
    return 1 - math.sqrt(f1/g) - (f1/g)*math.sin(10*math.pi*f1)
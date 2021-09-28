#!/usr/bin/env python
from random import random
import matplotlib.pyplot as plt
import numpy as np

def absolute(*args) -> float:
    """Benchmark function"""
    res = 0
    for x in args:
        res += abs(x)
    return res

def get_intervals(dom: list, dimensions: int, poblationSize: int, tao: float):
    newDom = []
    newDomTao = []
    tmp = []
    tmpTao = []
    for i in range(1, len(dom) + 1):
        tmp.append(dom[i - 1])
        tmpTao.append(tao)
        if i % (poblationSize / dimensions) == 0:
            newDom.append(tmp)
            newDomTao.append(tmpTao)
            tmp = []
            tmpTao = []
    return newDom, newDomTao

def generate_ants(dom: list, tao: list):
    ants = []
    taoAnts = []
    for i in range(len(dom)):
        rand = int((random() * 100) % len(dom[i]))
        ants.append(dom[i][rand])
        taoAnts.append(tao[i][rand])
    return ants, taoAnts

def inner_sum(x: list):
    sum = 0
    for i in x:
        for j in i:
            sum += j
    return sum

def greatest(x: list):
    gr = 0
    for i in range(len(x)):
        if x[i] > gr:
            gr = i
    return gr

# Datos iniciales
generations = 500
domStart = -10
domEnd = 10
poblationSize = 200
dimensions = 10
# Tasa de evaportación
ro = 0.01
increment = (abs(domStart) + abs(domEnd)) / (poblationSize - 1)
# Cantidad de feromonas en cada camino (inicialmente)
tao = 0.1
Q = 1

domain = [ domStart + (increment * i) for i in range(poblationSize) ]
domain, taoDom = get_intervals(domain, dimensions, poblationSize, tao)

ants, taoAnts = generate_ants(domain, taoDom)

for g in range(generations):

    for i in range(len(taoDom)):
        taoSum = sum(taoDom[i])
        for j in range(len(taoDom[i])):
            taoDom[i][j] /= taoSum
        probStart = 0
        probRate = random()
        for j in range(len(taoDom[i])):
            probStart += taoDom[i][j]
            if probStart >= probRate:
                ants[i] = domain[i][j]
                taoAnts[i] = taoDom[i][j]
                break

    for i in range(len(domain)):
        for j in range(len(domain[i])):
            if domain[i][j] in ants:
                try:
                    taoDom[i][j] = Q / absolute(domain[i][j])
                except ZeroDivisionError:
                    taoDom[i][j] = Q / 0.0000000000000001
            else:
                taoDom[i][j] = 0
        taoSum = sum(taoDom[i])
        for j in range(len(domain[i])):
            taoDom[i][j] = ( (1 - ro) * taoDom[i][j] ) + taoSum

# res = [ [ ants[i], abs(prob[i]) ] for i in range(len(prob)) ]
# res.sort(key=lambda x: x[1], reverse=True)
# print("\n", res)

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
    tmp = []
    for i in range(1, len(dom) + 1):
        tmp.append([dom[i - 1], tao])
        if i % (poblationSize / dimensions) == 0:
            newDom.append(tmp)
            tmp = []
    return newDom

def generate_ants(dom: list):
    ants = []
    for i in range(len(dom)):
        rand = int((random() * 100) % len(dom[i]))
        ants.append([dom[i][rand][0], dom[i][rand][1]])
    return ants

def inner_sum(x: list):
    sum = 0
    for _, v in x:
        sum += v
    return sum

def greatest(x: list):
    gr = 0
    for i in range(len(x)):
        if x[i] > gr:
            gr = i
    return gr

# Datos iniciales
generations = 100
domStart = -10
domEnd = 10
poblationSize = 4000
dimensions = 100
# Tasa de evaportación
ro = 0.01
increment = (abs(domStart) + abs(domEnd)) / (poblationSize - 1)
# Cantidad de feromonas en cada camino (inicialmente)
tao = 0.1
Q = 1

domain = [ domStart + (increment * i) for i in range(poblationSize) ]
domain = get_intervals(domain, dimensions, poblationSize, tao)

ants = generate_ants(domain)
best = 0

for g in range(generations):
    for i in range(len(domain)):
        taoSum = inner_sum(domain[i])
        for j in range(len(domain[i])):
            domain[i][j][1] /= taoSum
        probStart = 0
        probRate = random()
        domain[i].sort(key=lambda x: x[1], reverse=True)
        for j in range(len(domain[i])):
            probStart += domain[i][j][1]
            if probStart >= probRate:
                ants[i] = domain[i][j]
                break

    for i in range(len(domain)):
        for j in range(len(domain[i])):
            prevTao = domain[i][j][0]
            if domain[i][j] in ants:
                try:
                    domain[i][j][1] = Q / (absolute(domain[i][j][0]))
                except ZeroDivisionError:
                    domain[i][j][1] = Q / (1 / 0.00001)
            else:
                domain[i][j][1] = 0
            domain[i][j][1] = ( (1 - ro) * domain[i][j][1] ) + prevTao

for i in range(len(ants)):
    ants[i][1] = tao

for g in range(generations):
    taoSum = inner_sum(ants)
    for i in range(len(ants)):
        ants[i][1] /= taoSum
    probStart = 0
    probRate = random()
    ants.sort(key=lambda x: x[1], reverse=True)
    found = False
    for i in range(len(ants)):
        prevTao = ants[i][1]
        probStart += ants[i][1]
        if probStart >= probRate and not found:
            best = ants[i]
            found = True
            ants[i][1] = Q / (absolute(ants[i][0]))
        else:
            ants[i][1] = 0
        ants[i][1] = ( (1 - ro) * ants[i][1] ) + prevTao
    ants.sort(key=lambda x: x[1], reverse=True)
    print(f"best ({g}): {best}")

# print(ants)

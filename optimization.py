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
generations = 200
domStart = -10
domEnd = 10
poblationSize = 400
dimensions = 10
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
bestGlobal = []
bestDim = [ [] for _ in range(dimensions) ]

minimums = []
for i in range(len(domain)):
    tmp = domain[i][0][0]
    for k, _ in domain[i]:
        if k < 0:
            if k > tmp:
                tmp = k
        else:
            if k < tmp:
                tmp = k
    minimums.append(tmp)

print("Datos iniciales:")
print("Generaciones: ", generations)
print("Cantidad de caminos (dominio): ", poblationSize)
print(f"Valores del dominio: [{domStart}, {domEnd}]")
print("Dimensiones (cantidad en la que se divide el dominio): ", dimensions)
print("Número de feromonas inicial en todos los caminos (tao): ", tao)
print("Tasa de evaporación (ro): ", ro)
print("Constante de aprendizaje (Q): ", Q)

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
                bestDim[i].append(ants[i][0])
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
            best = ants[i][0]
            found = True
            bestGlobal.append(best)
            ants[i][1] = Q / (absolute(ants[i][0]))
        else:
            ants[i][1] = 0
        ants[i][1] = ( (1 - ro) * ants[i][1] ) + prevTao
    ants.sort(key=lambda x: x[1], reverse=True)

print(f"Mejor valor (global): {best}")

plt.figure()
for i in range(dimensions):
    fig = plt.figure()
    ax = fig.add_subplot()
    fig.suptitle('Optimización por colonia de hormigas continua', fontweight='bold')
    ax.set_title('Evolución de las hormigas (por dimensión)')
    ax.set_xlabel('Cantidad de generaciones')
    ax.set_ylabel(f'Evolución de la solución de la dimensión {i + 1}/{dimensions} (local)')
    plt.plot(range(generations), bestDim[i], 'b-', label='Evolución de la solución de la dimensión (local)')
    tmpX = 0
    for j in range(len(bestDim)):
        if bestDim[i][j] == bestGlobal[i]:
            tmpX = j
    ants.sort(key=lambda x: x[0])
    plt.plot(generations - 1, ants[i][0], 'r*', label="Mejor solución encontrada")
    plt.plot([ minimums[i] for _ in range(generations)], 'g--', \
            label='Valor óptimo (mínimo local de la dimensión)')
    ax.legend()
    plt.show()

fig = plt.figure()
ax = fig.add_subplot()
fig.suptitle('Optimización por colonia de hormigas continua')
ax.set_title('Evolución de la hormiga (de manera global)')
ax.set_xlabel('Cantidad de generaciones')
ax.set_ylabel('Evolución de la solución global')
plt.plot([0 for _ in range(generations)], 'g--', label='Valor óptimo (mínimo global)')
plt.plot([ bestGlobal[i] for i in range(len(bestGlobal))], 'b-', label='Evolución de la ruta de la hormiga')
tmpMin = max(bestGlobal)
tmpX = 0
for i in range(len(bestGlobal)):
    if bestGlobal[i] < abs(tmpMin):
        tmpMin = bestGlobal[i]
        tmpX = i
    elif bestGlobal[i] == abs(tmpMin):
        break

plt.plot(tmpX, tmpMin, 'r*', label="Mejor solución encontrada")
plt.plot(len(bestGlobal) - 1, bestGlobal[len(bestGlobal) - 1], 'r+', label="Última solución encontrada")
ax.legend()
plt.show()

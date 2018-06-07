import random
import collections
import math
import copy
from operator import attrgetter

# Global

populacao = 100
geracoes = 2000
dimensions = 30
intervalo = [[-100.0, 100.0]] * dimensions
numeroCromossomos = 10 * dimensions
delta = 0.09


def functionX(vetorSolucaoDeUmCromossomo):
    result = 0
    for x in range(dimensions):
        result += (vetorSolucaoDeUmCromossomo[x]**2)

    return result


def definir_cromossomo_qbit():
    cromossomo = []
    alpha = beta = (math.sqrt(2) / 2)
    for _ in range(numeroCromossomos):
        qbit = [alpha, beta]
        cromossomo.append(qbit)

    return cromossomo


def converterQBIT(cromossomo):
    cromossomoClassico = []
    for qbit in cromossomo:
        rand = random.random()
        if rand < qbit[0] ** 2:
            cromossomoClassico.append(1)
        else:
            cromossomoClassico.append(0)

    return cromossomoClassico


def functionFindIntervals(valorIntervalo, posicaoDoCromossomo, x):
    xintervalo = intervalo[x][0] + posicaoDoCromossomo * ((valorIntervalo[1] - (valorIntervalo[0])) / 1024)
    return xintervalo


def converterCromossomo(cromossomo):
    binaryChromeRepresentation = []  # Representa as variaveis que vao adquirir o valor binario da parcial
    realChromeRepresentation = []  # Representa as variaves que vao adquirir o valor real das variaveis binarias

    parcial = int(numeroCromossomos/dimensions)

    while len(binaryChromeRepresentation) != dimensions:
        binaryChromeRepresentation.append(cromossomo[:parcial])
        cromossomo = cromossomo[parcial:]

    for x in range(len(binaryChromeRepresentation)):  # len de binaryChrome = len de variaveis da function
        binaryChromeRepresentation[x] = ''.join(str(x) for x in binaryChromeRepresentation[x])

    for x in range(dimensions):
        realChromeRepresentation.append(
            functionFindIntervals(intervalo[x], int(binaryChromeRepresentation[x], 2), x))

    return realChromeRepresentation


class Agent(object):
    def __init__(self):
        self.cromossomoQBIT = definir_cromossomo_qbit()
        self.cromossomoClassico = converterQBIT(self.cromossomoQBIT)
        self.cromossomoINT = converterCromossomo(self.cromossomoClassico)
        self.fitness = 9999999

    def __str__(self):
        return "Fitness: {}".format(self.fitness)
        # return "CromossomoQBIT: {} | CromossomoClassico: {} | CromossomoINT: {} | Fitness: {}".format(
        #     self.cromossomoQBIT, self.cromossomoClassico, self.cromossomoINT, self.fitness)

def iniciarPopulacao(populacao):
    return [Agent() for _ in range(populacao)]


def definirFitness(agents):

    for agent in agents:
        agent.fitness = functionX(agent.cromossomoINT)
    # agents = sorted(agents, key=lambda x: x.fitness, reverse=True)
    #print('\n'.join(map(str, agents)))
    print(min(agents, key=attrgetter('fitness')))

    return agents

def findBestGlobal(agents, bestAgent):
    melhorGeracao = min(agents, key=attrgetter('fitness'))
    if bestAgent.fitness > melhorGeracao.fitness:
        bestAgent = copy.deepcopy(melhorGeracao)

    return bestAgent


def tableRotation(agents, bestAgent):
    arrayEpsilons = []
    deltaTeta = 0.0
    sinal = 0
    epsilonDeltaTeta = 0.0

    for agent in agents:
        for x in range(numeroCromossomos):

            if agent.cromossomoClassico[x] == 0 and bestAgent.cromossomoClassico[x] == 0:
                deltaTeta = 0.0
                sinal = 0

            if agent.cromossomoClassico[x] == 0 and bestAgent.cromossomoClassico[x] == 1:
                if agent.fitness > bestAgent.fitness:
                    deltaTeta = delta * math.pi
                    if agent.cromossomoQBIT[x][0] * agent.cromossomoQBIT[x][1] > 0:
                        sinal = -1

                    if agent.cromossomoQBIT[x][0] * agent.cromossomoQBIT[x][1] < 0:
                        sinal = 1

                    if agent.cromossomoQBIT[x][0] == 0:
                        rand = random.random()
                        if rand > 0.5:
                            sinal = 1

                        else:
                            sinal = -1

                    if agent.cromossomoQBIT[x][1] == 0:
                        sinal = 0

                else:
                    deltaTeta = delta * math.pi
                    if agent.cromossomoQBIT[x][0] * agent.cromossomoQBIT[x][1] > 0:
                        sinal = 1

                    if agent.cromossomoQBIT[x][0] * agent.cromossomoQBIT[x][1] < 0:
                        sinal = -1

                    if agent.cromossomoQBIT[x][0] == 0:
                        sinal = 0

                    if agent.cromossomoQBIT[x][1] == 0:
                        rand = random.random()
                        if rand > 0.5:
                            sinal = 1
                        else:
                            sinal = -1

            if agent.cromossomoClassico[x] == 1 and bestAgent.cromossomoClassico[x] == 0:
                if agent.fitness > bestAgent.fitness:
                    deltaTeta = delta * math.pi
                    if agent.cromossomoQBIT[x][0] * agent.cromossomoQBIT[x][1] > 0:
                        sinal = 1

                    if agent.cromossomoQBIT[x][0] * agent.cromossomoQBIT[x][1] < 0:
                        sinal = -1

                    if agent.cromossomoQBIT[x][0] == 0:
                        sinal = 0

                    if agent.cromossomoQBIT[x][1] == 0:
                        rand = random.random()
                        if rand > 0.5:
                            sinal = 1
                        else:
                            sinal = -1
                else:
                    deltaTeta = delta * math.pi
                    if agent.cromossomoQBIT[x][0] * agent.cromossomoQBIT[x][1] > 0:
                        sinal = 1

                    if agent.cromossomoQBIT[x][0] * agent.cromossomoQBIT[x][1] < 0:
                        sinal = -1

                    if agent.cromossomoQBIT[x][0] == 0:
                        sinal = 0

                    if agent.cromossomoQBIT[x][1] == 0:
                        rand = random.random()
                        if rand > 0.5:
                            sinal = 1
                        else:
                            sinal = -1

            if agent.cromossomoClassico[x] == 1 and bestAgent.cromossomoClassico[x] == 1:
                deltaTeta = 0.0
                sinal = 0


            epsilonDeltaTeta = sinal * deltaTeta
            arrayEpsilons.append(epsilonDeltaTeta)
    return arrayEpsilons


def updateUsingGate(agents, bestAgent):
    epsilons = tableRotation(agents, bestAgent)
    x_ep = 0

    for agent in agents:
        for qbit in agent.cromossomoQBIT:
            alpha = ((math.cos(epsilons[x_ep]) * qbit[0]) + (-math.sin(epsilons[x_ep]) * qbit[1]))
            beta = ((math.sin(epsilons[x_ep]) * qbit[0]) + (math.cos(epsilons[x_ep]) * qbit[1]))

            qbit[0] = alpha
            qbit[1] = beta
            x_ep += 1
        agent.cromossomoClassico = converterQBIT(agent.cromossomoQBIT)
        agent.cromossomoINT = converterCromossomo(agent.cromossomoClassico)

    return agents


def execGA():
    agents = iniciarPopulacao(populacao)  # Inicio uma populacao aleatoria
    bestAgent = copy.deepcopy(agents[0])

    for geracao in range(geracoes):
        print("Geracao " + str(geracao))

        agents = definirFitness(agents)  # Defino a fitness
        bestAgent = findBestGlobal(agents, bestAgent)
        print("BEST AGENT", bestAgent)
        agents = updateUsingGate(agents, bestAgent)

        # if any(round(agent.fitness, 2) == 0.00 for agent in agents):
        #     print('Achei um bom na geracao ', geracao)
        #     exit(0)


execGA()
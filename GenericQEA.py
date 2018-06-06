import random
import collections
import math

# Global
numeroCromossomos = 30
populacao = 100
geracoes = 1000
intervalo = [0.0, 10.0]


def functionX(x, y, z):
    return (x**2) + (y ** 2) + (z ** 2)


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


def functionFindIntervals(valorIntervalo, posicaoDoCromossomo):
    xintervalo = intervalo[0] + posicaoDoCromossomo * ((valorIntervalo[1] - (valorIntervalo[0])) / 1024)
    return xintervalo


def converterCromossomo(cromossomo):
    realX = 0.0
    realY = 0.0
    realZ = 0.0
    variaveis = collections.namedtuple('variaveis', ['x', 'y', 'z'])
    cromossomoX = cromossomo[:10]
    cromossomoY = cromossomo[10:20]
    cromossomoZ = cromossomo[20:]
    cromossomoX = ''.join(str(x) for x in cromossomoX)
    cromossomoY = ''.join(str(y) for y in cromossomoY)
    cromossomoZ = ''.join(str(z) for z in cromossomoZ)

    realX = functionFindIntervals(intervalo, int(cromossomoX, 2))
    realY = functionFindIntervals(intervalo, int(cromossomoY, 2))
    realZ = functionFindIntervals(intervalo, int(cromossomoZ, 2))

    variaveis = variaveis(realX, realY, realZ)
    return variaveis


class Agent(object):
    def __init__(self):
        self.cromossomoQBIT = definir_cromossomo_qbit()
        self.cromossomoClassico = converterQBIT(self.cromossomoQBIT)
        self.cromossomoINT = converterCromossomo(self.cromossomoClassico)
        self.fitnessPercent = 0.0
        self.rangeRoleta = [0.0, 0.0]
        self.fitness = -1

    def __str__(self):
        return "CromossomoQBIT: {} | CromossomoClassico: {} | CromossomoINT: {} | Fitness: {}".format(
            self.cromossomoQBIT, self.cromossomoClassico, self.cromossomoINT, self.fitness)

def iniciarPopulacao(populacao):
    return [Agent() for _ in range(populacao)]


def definirFitness(agents):
    for agent in agents:
        agent.fitness = functionX(agent.cromossomoINT[0], agent.cromossomoINT[1], agent.cromossomoINT[2])
    agents = sorted(agents, key=lambda x: x.fitness, reverse=True)
    print('\n'.join(map(str, agents)))
    return agents


def tableRotation(agents):
    b = agents[-1]
    arrayEpsilons = []
    deltaTeta = 0.0
    sinal = 0
    epsilonDeltaTeta = 0.0

    for agent in agents:
        for x in range(numeroCromossomos):

            if agent.cromossomoClassico[x] == 0 and b.cromossomoClassico[x] == 0:
                deltaTeta = 0.0
                sinal = 0

            if agent.cromossomoClassico[x] == 0 and b.cromossomoClassico[x] == 1:
                if agent.fitness > b.fitness:
                    deltaTeta = 0.01 * math.pi
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
                    deltaTeta = 0.01 * math.pi
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

            if agent.cromossomoClassico[x] == 1 and b.cromossomoClassico[x] == 0:
                if agent.fitness > b.fitness:
                    deltaTeta = 0.01 * math.pi
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
                    deltaTeta = 0.01 * math.pi
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

            if agent.cromossomoClassico[x] == 1 and b.cromossomoClassico[x] == 1:
                deltaTeta = 0.0
                sinal = 0


            epsilonDeltaTeta = sinal * deltaTeta
            arrayEpsilons.append(epsilonDeltaTeta)
    return arrayEpsilons


def updateUsingGate(agents):
    epsilons = tableRotation(agents)
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

    for geracao in range(geracoes):
        print("Geracao " + str(geracao))

        agents = definirFitness(agents)  # Defino a fitness
        agents = updateUsingGate(agents)

        if any(round(agent.fitness, 2) == 0.00 for agent in agents):
            print('Achei um bom na geracao ', geracao)
            exit(0)


execGA()
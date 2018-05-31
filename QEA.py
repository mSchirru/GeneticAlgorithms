import random
import math

# Global
numeroCromossomos = 5
populacao = 20
geracoes = 100


def function_x(x):
    return x ** 2


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
        if rand > qbit[0] ** 2:
            cromossomoClassico.append(1)
        else:
            cromossomoClassico.append(0)

    return cromossomoClassico


def converterCromossomo(cromossomoClassico):
    decimal = ''.join(str(x) for x in cromossomoClassico)
    return int(decimal, 2)


class Agent(object):
    def __init__(self):
        self.cromossomoQBIT = definir_cromossomo_qbit()  # Array de qbits(array) [[qbit]]
        self.cromossomoClassico = converterQBIT(self.cromossomoQBIT)
        self.cromossomoINT = converterCromossomo(self.cromossomoClassico)
        self.fitness = -1

    def __str__(self):
        return "CromossomoQBIT: {} | CromossomoClassico: {} | CromossomoINT: {} | Fitness: {}".format(
            self.cromossomoQBIT, self.cromossomoClassico, self.cromossomoINT, self.fitness)


def iniciarPopulacao(populacao):
    return [Agent() for _ in range(populacao)]


def definirFitness(agents):
    for agent in agents:
        agent.fitness = function_x(agent.cromossomoINT)

    agents = sorted(agents, key=lambda x: x.fitness)
    print('\n'.join(map(str, agents)))
    return agents


# def calcularFitnessPercent(agents):
#     somatorio = 0
#     for agent in agents:
#         agent.fitnessPercent = 0.0
#     for x in agents:
#         somatorio += x.fitness
#
#     for agent in agents:
#         agent.fitnessPercent = ((agent.fitness * 100) / somatorio)
#     return agents
#
#
# def definirRangeRoleta(agents):
#     for agent in agents:
#         agent.rangeRoleta = [0.0, 0.0]
#     agents = sorted(agents, key=lambda x: x.fitnessPercent)
#     # print("ANTES DO FOR")
#     # print('\n'.join(map(str, agents)))
#     somatorio = 0
#     for x in range(populacao):
#         if x == 0:
#             somatorio += agents[x].fitnessPercent
#             agents[x].rangeRoleta[1] = somatorio
#             agents[x].rangeRoleta[0] = 0.0
#         else:
#             agents[x].rangeRoleta[0] = somatorio
#             agents[x].rangeRoleta[1] = (somatorio + agents[x].fitnessPercent)
#             somatorio += agents[x].fitnessPercent
#     # print("DEPOIS DO FOR")
#     # print('\n'.join(map(str, agents)))
#     print('\n'.join(map(str, agents)))
#     return agents


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
                    deltaTeta = 0.05 * math.pi
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
                    deltaTeta = 0.05 * math.pi
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
                    deltaTeta = 0.05 * math.pi
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
                    deltaTeta = 0.05 * math.pi
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
        # agents = calcularFitnessPercent(agents)  # Calculo o percentual na rolate
        # agents = definirRangeRoleta(agents)  # Defino o range na roleta
        agents = updateUsingGate(agents)

        if any(agent.fitness >= 960 for agent in agents):
            print('Achei um bom')
            exit(0)


execGA()

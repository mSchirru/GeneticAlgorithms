import random
import math
import testSettings

#User input
funcao = input("Funcao que deseja minimizar: ")
setfun = input("max / min")
variaveis_da_funcao = []

for x in funcao:
    if x.isalpha():
        if x not in variaveis_da_funcao:
            variaveis_da_funcao.append(x)



# Global
numeroCromossomos = 10 * int(len(variaveis_da_funcao))
populacao = 100
geracoes = 1000
intervalo = [-6.0, 6.0]


def definir_cromossomo_qbit():
    cromossomo = []
    alpha = beta = (math.sqrt(2) / 2)
    for _ in range(numeroCromossomos):
        qbit = [alpha, beta]
        cromossomo.append(qbit)

    return cromossomo


# def converterQBIT(cromossomo):
#     cromossomoClassico = []
#     for qbit in cromossomo:
#         rand = random.random()
#         if rand > qbit[0] ** 2: # Minimiza funcao. > Maximiza funcao
#             cromossomoClassico.append(1)
#         else:
#             cromossomoClassico.append(0)
#
#     return cromossomoClassico


def functionX(variaveis_da_funcao, agent, funcao):
    funcao2 = funcao
    for aux in range(len(agent.cromossomoINT)):
        if variaveis_da_funcao[aux] in funcao2:
            funcao2 = funcao2.replace(str(variaveis_da_funcao[aux]), str(agent.cromossomoINT[aux]))


    return eval(str(funcao2))


def functionFindIntervals(valorIntervalo, posicaoDoCromossomo):
    xintervalo = intervalo[0] + posicaoDoCromossomo * ((valorIntervalo[1] - (valorIntervalo[0])) / 1024)
    return xintervalo


def converterCromossomo(cromossomo):
    binaryChromeRepresentation = [] # Representa as variaveis que vao adquirir o valor binario da parcial
    realChromeRepresentation = [] # Representa as variaves que vao adquirir o valor real das variaveis binarias
    variaveis =[]


    parcial = int(numeroCromossomos / len(variaveis_da_funcao))

    while len(binaryChromeRepresentation) != len(variaveis_da_funcao):
        binaryChromeRepresentation.append(cromossomo[:parcial])
        cromossomo = cromossomo[parcial:]

    for x in range(len(binaryChromeRepresentation)): # len de binaryChrome = len de variaveis da funcao
        binaryChromeRepresentation[x] = ''.join(str(x) for x in binaryChromeRepresentation[x])

    for x in range(len(variaveis_da_funcao)):
        realChromeRepresentation.append(functionFindIntervals(intervalo, int(binaryChromeRepresentation[x], 2)))


    return realChromeRepresentation


class Agent(object):
    def __init__(self):
        self.cromossomoQBIT = definir_cromossomo_qbit()
        self.cromossomoClassico = testSettings.setFunction[setfun](self.cromossomoQBIT)
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
        agent.fitness = functionX(variaveis_da_funcao, agent, funcao)
    agents = sorted(agents, key=lambda x: x.fitness, reverse=True)
    print('\n'.join(map(str, agents)))
    return agents


def tableRotation(agents):
    if setfun == 'min':
        b = agents[-1]
    else:
        b = agents[0]
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
        agent.cromossomoClassico = testSettings.setFunction[setfun](agent.cromossomoQBIT)
        agent.cromossomoINT = converterCromossomo(agent.cromossomoClassico)

    return agents


def execGA():


    agents = iniciarPopulacao(populacao)  # Inicio uma populacao aleatoria

    for geracao in range(geracoes):
        print("Geracao " + str(geracao))

        agents = definirFitness(agents)  # Defino a fitness
        agents = updateUsingGate(agents)

        if any(round(agent.fitness, 2) == 0.00 for agent in agents):
        # if any(agent.fitness >= 7198 for agent in agents):
            print('Achei um bom na geracao ', geracao)
            exit(0)


execGA()
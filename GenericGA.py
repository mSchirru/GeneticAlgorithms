import random
import copy
from operator import attrgetter

# Global

populacao = 100
geracoes = 10000
dimensoes = 5
taxaCrossOver = int(0.8*populacao)
taxaMutacao = 0.001
intervalo = [[-100.0, 100.0]] * dimensoes
numeroCromossomos = 10 * dimensoes


def functionX(vetorSolucaoDeUmCromossomo):
    result = 0
    for x in range(dimensoes):
        result += (vetorSolucaoDeUmCromossomo[x] ** 2)

    return result


def definirCromossomo():
    cromossomo = []
    for _ in range(numeroCromossomos):
        if random.random() >= 0.5:
            cromossomo.append(1)
        else:
            cromossomo.append(0)

    return cromossomo


def functionFindIntervals(valorIntervalo, posicaoDoCromossomo, x):
    xintervalo = intervalo[x][0] + posicaoDoCromossomo * ((valorIntervalo[1] - (valorIntervalo[0])) / 1024)
    return xintervalo


def converterCromossomo(cromossomo):
    binaryChromeRepresentation = []  # Representa as variaveis que vao adquirir o valor binario da parcial
    realChromeRepresentation = []  # Representa as variaves que vao adquirir o valor real das variaveis binarias

    parcial = int(numeroCromossomos / dimensoes)

    while len(binaryChromeRepresentation) != dimensoes:
        binaryChromeRepresentation.append(cromossomo[:parcial])
        cromossomo = cromossomo[parcial:]

    for x in range(len(binaryChromeRepresentation)):  # len de binaryChrome = len de variaveis da function
        binaryChromeRepresentation[x] = ''.join(str(x) for x in binaryChromeRepresentation[x])

    for x in range(dimensoes):
        realChromeRepresentation.append(
            functionFindIntervals(intervalo[x], int(binaryChromeRepresentation[x], 2), x))

    return realChromeRepresentation


class Agent(object):
    def __init__(self):
        self.cromossomoBIT = definirCromossomo()
        self.cromossomoINT = converterCromossomo(self.cromossomoBIT)
        self.fitnessPercent = 0.0
        self.rangeRoleta = [0.0, 0.0]
        self.fitness = 99999999
        self.ficFitness = 999



    def __str__(self):
        # return "Fitness: {}".format(self.fitness)
       return "Fitness: {} | RangeRoleta: {} | FitnessPercent: {}".format(self.fitness, self.rangeRoleta, self.fitnessPercent)

        # return "CromossomoClassico: {} | CromossomoINT: {} | Fitness: {} | RangeRoleta: {}".format(
           # self.cromossomoBIT, self.cromossomoINT, self.fitness, self.rangeRoleta)
#

def iniciarPopulacao(populacao):
    return [Agent() for _ in range(populacao)]


def definirFitness(agents):
    for agent in agents:
        agent.fitness = functionX(agent.cromossomoINT)
    return agents

def findBestGlobal(agents, bestAgent):
    melhorGeracao = min(agents, key=attrgetter('fitness'))
    if bestAgent.fitness > melhorGeracao.fitness:
        bestAgent = copy.deepcopy(melhorGeracao)

    return bestAgent

def calcularFitnessPercent(agents):

    somatorio = 0
    for agent in agents:
        agent.fitnessPercent = 0.0
    for x in agents:
        somatorio += x.fitness

    for agent in agents:
        agent.fitnessPercent =  agent.fitness / somatorio
    return agents


def definirRangeRoleta(agents):
    somageral = (100+1)*(100/2)
    for agent in agents:
        agent.rangeRoleta = [0.0, 0.0]
    agents = sorted(agents, key=lambda x: x.fitnessPercent, reverse=True)
    # print("ANTES DO FOR")
    # print('\n'.join(map(str, agents)))
    somatorio = 0

    for x in range(populacao):
        if x == 0:
            somatorio += agents[x].fitnessPercent
            agents[x].rangeRoleta[1] = somatorio
            agents[x].rangeRoleta[0] = 0.0

        else:

            agents[x].rangeRoleta[0] = somatorio
            agents[x].rangeRoleta[1] = (somatorio + agents[x].fitnessPercent)

            somatorio += agents[x].fitnessPercent

    # print("DEPOIS DA DEFINICAO DA FITNESS")
    # print('\n'.join(map(str, agents)))

    return agents



def selecaoProCross(agents):
    listaSelecionados = []
    agents = sorted(agents, key=lambda x: x.fitnessPercent, reverse=True)
    # print('\n'.join(map(str, agents)))

    # print(min(agents, key=attrgetter('fitness')))
    somatorio = 0
    for x in agents:
        somatorio += x.fitnessPercent

    for _ in range(taxaCrossOver):
        numeroAleatorio = random.uniform(0.0, somatorio)
        for agent in agents:
            if numeroAleatorio >= agent.rangeRoleta[0] and numeroAleatorio < agent.rangeRoleta[1]:

                # Todos os objetos que eu quero adicionar na lista, tem que
                # ser novos objetos e não cópias dos q já existem
                agenteSelecionado = copy.deepcopy(agent)
                listaSelecionados.append(agenteSelecionado)
                break

    # print('\n'.join(map(str, listaSelecionados)))


    return listaSelecionados




def crossover(listaSelecionados, taxaCrossOver, agents):
    novaGeracao = []
    for _ in range(int(taxaCrossOver/2)):  # Crossando sempre 80% da populacao

        randPai = random.choice(listaSelecionados)
        pai = copy.deepcopy(randPai)


        randMae = random.choice(listaSelecionados)
        # while randMae == randPai:
        #
        #     randMae = random.choice(listaSelecionados)

        mae = copy.deepcopy(randMae)

        child1 = Agent()
        child2 = Agent()
        #ONE POINT CROSSOVER
        split = random.randint(1, numeroCromossomos-1)
        child1.cromossomoBIT = pai.cromossomoBIT[:split] + mae.cromossomoBIT[split:]
        child2.cromossomoBIT = mae.cromossomoBIT[:split] + pai.cromossomoBIT[split:]

        # listaSelecionados.remove(randMae)
        # listaSelecionados.remove(randPai)

        novaGeracao.append(child1)
        novaGeracao.append(child2)

    novaGeracao.append(min(agents, key=attrgetter('fitness')))

    while len(novaGeracao) != len(agents):
        novaGeracao.append(copy.deepcopy(random.choice(agents)))

    print('\n'.join(map(str, novaGeracao)))

    return novaGeracao


def mutar(agents, taxaMutacao):

    teste = int((populacao * numeroCromossomos) * taxaMutacao)
    for _ in range(teste):
        individuoRand = random.choice(agents)
        individuoAmutar = copy.deepcopy(individuoRand)
        agents.remove(individuoRand)

        pontoCorte = random.randint(1, numeroCromossomos-1)
        if individuoAmutar.cromossomoBIT[pontoCorte] == 0:
            individuoAmutar.cromossomoBIT[pontoCorte] = 1
            agents.append(individuoAmutar)

        else:
            individuoAmutar.cromossomoBIT[pontoCorte] = 0
            agents.append(individuoAmutar)
    return agents


def execGA(taxaCrossOver, taxaMutacao):
    agents = iniciarPopulacao(populacao)  # Inicio uma populacao aleatoria
    bestAgent = copy.deepcopy(agents[0])

    for geracao in range(geracoes):
        print("Geracao " + str(geracao))

        agents = definirFitness(agents)  # Defino a fitness
        agents = calcularFitnessPercent(agents)  # Calculo o percentual na rolate
        agents = definirRangeRoleta(agents)  # Defino o range na roleta
        bestAgent = findBestGlobal(agents, bestAgent)
        print("BEST AGENT", bestAgent)
        listaSelecionados = selecaoProCross(agents) # Seleciono novos individuos a partir da geracao anterior
        agents = crossover(listaSelecionados, taxaCrossOver, agents)  # Crosso esses individuos
        agents = mutar(agents, taxaMutacao)  # Muto eles


        # if any(round(agent.fitness, 2) == 0.00 for agent in agents):
        #     print('Achei um bom')
        #     exit(0)

execGA(taxaCrossOver, taxaMutacao)
import random
import copy
from operator import attrgetter

# Global

populacao = 2000
geracoes = 4000
dimensoes = 10
taxaCrossOver = int(0.8*populacao)
taxaMutacao = 0.05
intervalo = [[-5.12, 5.12]] * dimensoes
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

    def __str__(self):
       return "Fitness: {}".format(self.fitness)

        #return "CromossomoClassico: {} | CromossomoINT: {} | Fitness: {}".format(
         #   self.cromossomoBIT, self.cromossomoINT, self.fitness)


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
        agent.fitnessPercent = (somatorio / agent.fitness)
    return agents


def definirRangeRoleta(agents):
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
    # print("DEPOIS DO FOR")
    # print('\n'.join(map(str, agents)))

    return agents


def selecao(agents, bestAgent):
    listaSelecionados = []
    #print('\n'.join(map(str, agents)))
    print(min(agents, key=attrgetter('fitness')))
    somatorio = 0
    for x in agents:
        somatorio += x.fitnessPercent

    listaSelecionados.append(bestAgent)  # Elitismo

    for _ in range(populacao-1):
        numeroAleatorio = random.uniform(0.0, somatorio)
        for agent in agents:
            if numeroAleatorio >= agent.rangeRoleta[0] and numeroAleatorio < agent.rangeRoleta[1]:

                # Todos os objetos que eu quero adicionar na lista, tem que
                # ser novos objetos e não cópias dos q já existem
                agenteSelecionado = copy.deepcopy(agent)
                listaSelecionados.append(agenteSelecionado)
                break
#  Destruo todas as referencias dos objetos antigos
    for _ in range(len(agents)):
        del agents[0]

    agents = listaSelecionados

    return agents


def crossover(agents, taxaCrossOver):
    list = [*range(populacao)]

    for _ in range(int(taxaCrossOver/2)):  # Crossando sempre 80% da populacao
        indexPai = random.choice(list)
        pai = agents[indexPai]
        list.remove(indexPai)

        indexMae = random.choice(list)
        list.remove(indexMae)
        mae = agents[indexMae]

        child1 = Agent()
        child2 = Agent()
        split = random.randint(0, numeroCromossomos)
        child1.string = pai.cromossomoBIT[0:split] + mae.cromossomoBIT[split:numeroCromossomos]
        child2.string = mae.cromossomoBIT[0:split] + pai.cromossomoBIT[split:numeroCromossomos]

        agents.remove(mae)
        agents.remove(pai)

        agents.append(child1)
        agents.append(child2)

    return agents


def mutar(agents, taxaMutacao):
    for agent in agents:
        pontoCorte = random.randint(0, numeroCromossomos-1)  # Gero um ponto de corte aleatorio
        chanceMutacao = random.random()
        if chanceMutacao <=taxaMutacao:  # Chance de mutacao em 0.01
            if agent.cromossomoBIT[pontoCorte] == 0:
                agent.cromossomoBIT[pontoCorte] = 1
            else:
                agent.cromossomoBIT[pontoCorte] = 0

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
        agents = selecao(agents, bestAgent)  # Seleciono novos individuos a partir da geracao anterior
        agents = crossover(agents, taxaCrossOver)  # Crosso esses individuos
        agents = mutar(agents, taxaMutacao)  # Muto eles

        if any(round(agent.fitness, 2) == 0.00 for agent in agents):
            print('Achei um bom')
            exit(0)

execGA(taxaCrossOver, taxaMutacao)
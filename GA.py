import random
import copy
import collections

# Global
numeroCromossomos = 20
populacao = 100
geracoes = 3000
intervalo = [-6.0, 6.0]


def functionX(x, y):
    return ((x**2 + y - 11)**2) + ((x + y**2 - 7)**2)


def definirCromossomo():
    cromossomo = []
    for _ in range(numeroCromossomos):
        if random.random() >= 0.5:
            cromossomo.append(1)
        else:
            cromossomo.append(0)

    return cromossomo


def functionFindIntervals(valorIntervalo, posicaoDoCromossomo):
    xintervalo = intervalo[0] + posicaoDoCromossomo * ((valorIntervalo[1] - (valorIntervalo[0])) / 1024)
    return xintervalo


def converterCromossomo(cromossomo):
    realX = 0.0
    realY = 0.0
    variaveis = collections.namedtuple('variaveis', ['x', 'y'])
    cromossomoX = cromossomo[:10]
    cromossomoY = cromossomo[10:]
    cromossomoX = ''.join(str(x) for x in cromossomoX)
    cromossomoY = ''.join(str(y) for y in cromossomoY)

    realX = functionFindIntervals(intervalo, int(cromossomoX, 2))
    realY = functionFindIntervals(intervalo, int(cromossomoY, 2))

    variaveis = variaveis(realX, realY)
    return variaveis


class Agent(object):
    def __init__(self):
        self.cromossomoBIT = definirCromossomo()
        self.cromossomoINT = converterCromossomo(self.cromossomoBIT)
        self.fitnessPercent = 0.0
        self.rangeRoleta = [0.0, 0.0]
        self.fitness = -1

    def __str__(self):
        return "CromossomoBIT: {} CromossomoINT: {} Fitness: {} FitnessPercent: {} RangeRoleta: {}".format(self.cromossomoBIT, self.cromossomoINT, self.fitness, self.fitnessPercent, self.rangeRoleta)


def iniciarPopulacao(populacao):
    return [Agent() for _ in range(populacao)]


def definirFitness(agents):
    for agent in agents:
        agent.fitness = functionX(agent.cromossomoINT[0], agent.cromossomoINT[1])
    return agents


def calcularFitnessPercent(agents):
    somatorio = 0
    for agent in agents:
        agent.fitnessPercent = 0.0
    for x in agents:
        somatorio += x.fitness

    for agent in agents:
        agent.fitnessPercent = ((somatorio / agent.fitness))
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


def selecao(agents):
    listaSelecionados = []
    agents = sorted(agents, key=lambda x: x.fitnessPercent, reverse=True)
    print('\n'.join(map(str, agents)))
    somatorio = 0
    for x in agents:
        somatorio += x.fitnessPercent

    # listaSelecionados.append(agents[-1])  # Elitismo

    for _ in range(populacao):
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


def crossover(agents):
    list = [*range(populacao)]

    TAXACROSS = int(0.8*populacao)

    for _ in range(int(TAXACROSS/2)):  # Crossando sempre 80% da populacao
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


def mutar(agents):
    for agent in agents:
        pontoCorte = random.randint(0, numeroCromossomos-1)  # Gero um ponto de corte aleatorio
        chanceMutacao = random.random()
        if chanceMutacao <= 0.01:  # Chance de mutacao em 0.01
            if agent.cromossomoBIT[pontoCorte] == 0:
                agent.cromossomoBIT[pontoCorte] = 1
            else:
                agent.cromossomoBIT[pontoCorte] = 0

    return agents


def execGA():
    agents = iniciarPopulacao(populacao)  # Inicio uma populacao aleatoria

    for geracao in range(geracoes):
        print("Geracao " + str(geracao))

        agents = definirFitness(agents)  # Defino a fitness
        agents = calcularFitnessPercent(agents)  # Calculo o percentual na rolate
        agents = definirRangeRoleta(agents)  # Defino o range na roleta
        agents = selecao(agents)  # Seleciono novos individuos a partir da geracao anterior
        agents = crossover(agents)  # Crosso esses individuos
        agents = mutar(agents)  # Muto eles

        if any(round(agent.fitness, 2) == 0.00 for agent in agents):
            print('Achei um bom')
            exit(0)

execGA()
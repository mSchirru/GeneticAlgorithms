import random
import math
import testSettings

################ PARAMETERS OF THE FUNCTION############################

function = '((x**2 + y - 11)**2) + ((x + y**2 - 7)**2)' # Insert the function
setfun = 'min' # max or min to maximize ou minimize the function
function_variables = ['x','y'] # set the variables of the function
integrations_curves = [[-6.0, 6.0], [-6.0, 6.0]]

#######################################################################


###################### PARAMETERS OF QEA ##############################

number_of_alleles = 10 * int(len(function_variables))   # precision of chromossome
population = 100  # Number of population for each generation
generations = 1000 # number_of_alleles of maximum generations
delta = 0.01 # Delta of the gate

#######################################################################

####################################################################################################################
# This function define the pair of alpha and beta for each chromossome and intiliaze it with 50% chances (sqrt(2)/2)
def define_qbit_chromossome():
    chromossome = []
    alpha = beta = (math.sqrt(2) / 2)
    for _ in range(number_of_alleles):
        qbit = [alpha, beta]
        chromossome.append(qbit)

    return chromossome
####################################################################################################################


def functionX(function_variables, agent, function):
    function2 = function
    for aux in range(len(agent.chromossomeINT)): # insert each variable in the function and return evaluate the fuction
        if function_variables[aux] in function2:
            function2 = function2.replace(str(function_variables[aux]), str(agent.chromossomeINT[aux]))


    return eval(str(function2))

####################################################################################################################


def functionFindIntervals(valorIntervalo, posicaoDoCromossomo, x):
    xintervalo = integrations_curves[x][0] + posicaoDoCromossomo * ((valorIntervalo[1] - (valorIntervalo[0])) / 1024)
    return xintervalo


def converterCromossomo(chromossome):
    binaryChromeRepresentation = [] # Representa as variaveis que vao adquirir o valor binario da parcial
    realChromeRepresentation = [] # Representa as variaves que vao adquirir o valor real das variaveis binarias

    parcial = int(number_of_alleles / len(function_variables))

    while len(binaryChromeRepresentation) != len(function_variables):
        binaryChromeRepresentation.append(chromossome[:parcial])
        chromossome = chromossome[parcial:]

    for x in range(len(binaryChromeRepresentation)): # len de binaryChrome = len de variaveis da function
        binaryChromeRepresentation[x] = ''.join(str(x) for x in binaryChromeRepresentation[x])

    for x in range(len(function_variables)):
        realChromeRepresentation.append(functionFindIntervals(integrations_curves[x], int(binaryChromeRepresentation[x], 2), x))


    return realChromeRepresentation


class Agent(object):
    def __init__(self):
        self.chromossomeQBIT = define_qbit_chromossome()
        self.chromossomeClassico = testSettings.setFunction[setfun](self.chromossomeQBIT)
        self.chromossomeINT = converterCromossomo(self.chromossomeClassico)
        self.fitness = -1

    def __str__(self):
        return "CromossomoQBIT: {} | CromossomoClassico: {} | CromossomoINT: {} | Fitness: {}".format(
            self.chromossomeQBIT, self.chromossomeClassico, self.chromossomeINT, self.fitness)

def iniciarPopulacao(population):
    return [Agent() for _ in range(population)]


def definirFitness(agents):

    for agent in agents:
        agent.fitness = functionX(function_variables, agent, function)
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
        for x in range(number_of_alleles):

            if agent.chromossomeClassico[x] == 0 and b.chromossomeClassico[x] == 0:
                deltaTeta = 0.0
                sinal = 0

            if agent.chromossomeClassico[x] == 0 and b.chromossomeClassico[x] == 1:
                if agent.fitness > b.fitness:
                    deltaTeta = delta * math.pi
                    if agent.chromossomeQBIT[x][0] * agent.chromossomeQBIT[x][1] > 0:
                        sinal = -1

                    if agent.chromossomeQBIT[x][0] * agent.chromossomeQBIT[x][1] < 0:
                        sinal = 1

                    if agent.chromossomeQBIT[x][0] == 0:
                        rand = random.random()
                        if rand > 0.5:
                            sinal = 1

                        else:
                            sinal = -1

                    if agent.chromossomeQBIT[x][1] == 0:
                        sinal = 0

                else:
                    deltaTeta = delta * math.pi
                    if agent.chromossomeQBIT[x][0] * agent.chromossomeQBIT[x][1] > 0:
                        sinal = 1

                    if agent.chromossomeQBIT[x][0] * agent.chromossomeQBIT[x][1] < 0:
                        sinal = -1

                    if agent.chromossomeQBIT[x][0] == 0:
                        sinal = 0

                    if agent.chromossomeQBIT[x][1] == 0:
                        rand = random.random()
                        if rand > 0.5:
                            sinal = 1
                        else:
                            sinal = -1

            if agent.chromossomeClassico[x] == 1 and b.chromossomeClassico[x] == 0:
                if agent.fitness > b.fitness:
                    deltaTeta = delta * math.pi
                    if agent.chromossomeQBIT[x][0] * agent.chromossomeQBIT[x][1] > 0:
                        sinal = 1

                    if agent.chromossomeQBIT[x][0] * agent.chromossomeQBIT[x][1] < 0:
                        sinal = -1

                    if agent.chromossomeQBIT[x][0] == 0:
                        sinal = 0

                    if agent.chromossomeQBIT[x][1] == 0:
                        rand = random.random()
                        if rand > 0.5:
                            sinal = 1
                        else:
                            sinal = -1
                else:
                    deltaTeta = delta * math.pi
                    if agent.chromossomeQBIT[x][0] * agent.chromossomeQBIT[x][1] > 0:
                        sinal = 1

                    if agent.chromossomeQBIT[x][0] * agent.chromossomeQBIT[x][1] < 0:
                        sinal = -1

                    if agent.chromossomeQBIT[x][0] == 0:
                        sinal = 0

                    if agent.chromossomeQBIT[x][1] == 0:
                        rand = random.random()
                        if rand > 0.5:
                            sinal = 1
                        else:
                            sinal = -1

            if agent.chromossomeClassico[x] == 1 and b.chromossomeClassico[x] == 1:
                deltaTeta = 0.0
                sinal = 0


            epsilonDeltaTeta = sinal * deltaTeta
            arrayEpsilons.append(epsilonDeltaTeta)
    return arrayEpsilons


def updateUsingGate(agents):
    epsilons = tableRotation(agents)
    x_ep = 0

    for agent in agents:
        for qbit in agent.chromossomeQBIT:
            alpha = ((math.cos(epsilons[x_ep]) * qbit[0]) + (-math.sin(epsilons[x_ep]) * qbit[1]))
            beta = ((math.sin(epsilons[x_ep]) * qbit[0]) + (math.cos(epsilons[x_ep]) * qbit[1]))

            qbit[0] = alpha
            qbit[1] = beta
            x_ep += 1
        agent.chromossomeClassico = testSettings.setFunction[setfun](agent.chromossomeQBIT)
        agent.chromossomeINT = converterCromossomo(agent.chromossomeClassico)

    return agents


def execGA():


    agents = iniciarPopulacao(population)  # Inicio uma population aleatoria

    for geracao in range(generations):
        print("Geracao " + str(geracao))

        agents = definirFitness(agents)  # Defino a fitness
        agents = updateUsingGate(agents)

        if any(round(agent.fitness, 5) == 0.0000 for agent in agents):
        # if any(agent.fitness   for agent in agents):
            print('Achei um bom na geracao ', geracao)
            exit(0)


execGA()
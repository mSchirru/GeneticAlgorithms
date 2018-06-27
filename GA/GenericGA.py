import random
import copy
from operator import attrgetter
import matplotlib.pyplot as plt

# Global

population = 1000
generations = 2000
dimensions = 30
crossover_percentage = int(0.8*population)
mutation_percentage = 0.01
intervals = [[-5.12, 5.12]] * dimensions
chromosome_alleles_number = 12 * dimensions


def function_x(chromosome_vector_solution):
    result = 0

    for x in range(dimensions):
        result += (chromosome_vector_solution[x] ** 2)

    return result


def generate_binary_chromosome():
    chromosome = []
    for _ in range(chromosome_alleles_number):
        if random.random() >= 0.5:
            chromosome.append(1)
        else:
            chromosome.append(0)

    return chromosome


def interval_precision(interval_value, chromosome_position, x):

    xintervals = intervals[x][0] + chromosome_position * ((interval_value[1] - (interval_value[0])) / 4096)

    return xintervals


def convert_binary_to_decimal(chromosome):
    binary_chromosome_representation = []
    real_chromosome_representation = []

    parcial = int(chromosome_alleles_number / dimensions)

    while len(binary_chromosome_representation) != dimensions:
        binary_chromosome_representation.append(chromosome[:parcial])
        chromosome = chromosome[parcial:]

    for x in range(len(binary_chromosome_representation)):
        binary_chromosome_representation[x] = ''.join(str(x) for x in binary_chromosome_representation[x])

    for x in range(dimensions):
        real_chromosome_representation.append(
            interval_precision(intervals[x], int(binary_chromosome_representation[x], 2), x))

    return real_chromosome_representation


class Agent(object):
    def __init__(self):
        self.chromosomeBIT = generate_binary_chromosome()
        self.chromosomeINT = convert_binary_to_decimal(self.chromosomeBIT)
        self.fitness_percentage = 0.0
        self.roulette_range = [0.0, 0.0]
        self.fitness = -99999999
        self.mutated = False

    def __str__(self):
        return "Fitness: {}".format(1/self.fitness)


def initialize_population(population):
    return [Agent() for _ in range(population)]


def define_fitness(agents):

    for agent in agents:
        agent.fitness = 1/function_x(agent.chromosomeINT)

    return agents


def find_global_best(agents, bestAgent):

    new_possible_best = max(agents, key=attrgetter('fitness'))

    if bestAgent.fitness < new_possible_best.fitness:
        bestAgent = copy.deepcopy(new_possible_best)

    return bestAgent


def calculate_fitness_percentage(agents):

    _sum = 0
    for agent in agents:
        agent.mutated = False
        agent.fitness_percentage = 0.0
    for x in agents:
        _sum += x.fitness

    for agent in agents:
        agent.fitness_percentage = agent.fitness / _sum
    return agents


def define_roulette_range(agents):

    for agent in agents:
        agent.roulette_range = [0.0, 0.0]
    agents = sorted(agents, key=lambda x: x.fitness_percentage, reverse=True)

    _sum = 0

    for x in range(population):
        if x == 0:
            _sum += agents[x].fitness_percentage
            agents[x].roulette_range[1] = _sum
            agents[x].roulette_range[0] = 0.0

        else:

            agents[x].roulette_range[0] = _sum
            agents[x].roulette_range[1] = (_sum + agents[x].fitness_percentage)

            _sum += agents[x].fitness_percentage

    return agents

def select_by_roulette(agents):

    selected_list = []

    agents = sorted(agents, key=lambda x: x.fitness_percentage, reverse=True)

    _sum = 0

    for agent in agents:
        _sum += agent.fitness_percentage

    for _ in range(population):
        random_number = random.uniform(0.0, _sum)
        for agent in agents:
            if random_number >= agent.roulette_range[0] and random_number < agent.roulette_range[1]:

                agent_selected = copy.deepcopy(agent)
                selected_list.append(agent_selected)
                break

    for _ in range(len(agents)):
        del agents[0]

    agents = selected_list

    return agents


def select_for_crossover(agents):
    selected_list = []
    agents = sorted(agents, key=lambda x: x.fitness_percentage, reverse=True)

    _sum = 0
    for x in agents:
        _sum += x.fitness_percentage

    while len(selected_list) != crossover_percentage:
        random_number = random.uniform(0.0, _sum)
        for agent in agents:
            if random_number >= agent.roulette_range[0] and random_number < agent.roulette_range[1]:

                agent_selected = copy.deepcopy(agent)
                selected_list.append(agent_selected)
                agents.remove(agent)
                break

    return selected_list, agents




def crossover(selected_list, crossover_percentage, agents):

    new_generation = []

    for _ in range(int(crossover_percentage/2)):

        random_dad = random.choice(selected_list)
        dad = copy.deepcopy(random_dad)


        random_mom = random.choice(selected_list)
        while random_mom == random_dad:

            random_mom = random.choice(selected_list)

        mom = copy.deepcopy(random_mom)

        child1 = Agent()
        child2 = Agent()
        #ONE POINT CROSSOVER
        split = random.randint(1, chromosome_alleles_number - 1)
        child1.chromosomeBIT = dad.chromosomeBIT[:split] + mom.chromosomeBIT[split:]
        child2.chromosomeBIT = mom.chromosomeBIT[:split] + dad.chromosomeBIT[split:]
        child1.chromosomeINT = convert_binary_to_decimal(child1.chromosomeBIT)
        child2.chromosomeINT = convert_binary_to_decimal(child2.chromosomeBIT)


        selected_list.remove(random_mom)
        selected_list.remove(random_dad)
        del dad
        del mom

        new_generation.append(child1)
        new_generation.append(child2)

    new_generation += agents


    return new_generation


def mutar(agents, mutation_percentage):

    mutations_number = int(population * mutation_percentage)

    for _ in range(mutations_number):
        randomic_agent = random.choice(agents)

        while randomic_agent.mutated == True:
            randomic_agent = random.choice(agents)

        agent_tobe_muted = copy.deepcopy(randomic_agent)
        agents.remove(randomic_agent)

        pontoCorte = random.randint(1, chromosome_alleles_number-1)
        if agent_tobe_muted.chromosomeBIT[pontoCorte] == 0:
            agent_tobe_muted.chromosomeBIT[pontoCorte] = 1
            agent_tobe_muted.mutated = True
            agents.append(agent_tobe_muted)

        else:
            agent_tobe_muted.chromosomeBIT[pontoCorte] = 0
            agent_tobe_muted.mutated = True
            agents.append(agent_tobe_muted)

    return agents


def execGA(crossover_percentage, mutation_percentage):
    teste1 = []
    teste2 = []
    agents = initialize_population(population)
    bestAgent = copy.deepcopy(agents[0])

    for generation in range(generations):
        print("Geracao " + str(generation))

        agents = define_fitness(agents)
        agents = calculate_fitness_percentage(agents)
        agents = define_roulette_range(agents)
        bestAgent = find_global_best(agents, bestAgent)
        agents = select_by_roulette(agents)
        print("BEST AGENT", bestAgent)
        selected_list, agents = select_for_crossover(agents)
        agents = crossover(selected_list, crossover_percentage, agents)
        agents = mutar(agents, mutation_percentage)
        agents.remove(min(agents, key=attrgetter('fitness')))
        agents.append(bestAgent)
        teste1.append(generation)
        teste2.append(1/bestAgent.fitness)


        print(max(agents, key=attrgetter('fitness')))

    plt.plot(teste1, teste2)
    plt.title('GA Roleta Postiva 02')
    plt.ylabel('best agents fitness')
    plt.xlabel('generations')
    plt.text(teste1[3], 100,
             'Geracoes: 2000 | Populacao: 1000 | Mutacao: 0.01 | Cross: 0.08')
    plt.text(teste2[3], 70, 'Precisao: 12 Bits | Intervalo: -5.12, 5.12 | Dimensao: 30' )

    plt.show()



execGA(crossover_percentage, mutation_percentage)
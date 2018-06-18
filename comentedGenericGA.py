import random
import copy
from operator import attrgetter

# Global

population = 100 # Size of population
generations = 1000 # Number of generations
dimensions = 30 # Each dimension can be interpreted as a variable (e.g: x, y, z = 3 dimensions)
crossover_percentage = int(0.8 * population)
mutation_percentage = 0.001
intervals = [[-100.0, 100.0]] * dimensions  # Represents one interval for each dimension
chromosome_alleles_number = 10 * dimensions # Using a 10 precision chromosome for each dimension


def function_x(chromosome_vector_solution): # Define the function to be calculated
    # chromosome_vector_solution represents will be represented later on code by the integers of the chromosomeINT attr

    result = 0

    for x in range(dimensions):
        result += (chromosome_vector_solution[x] ** 2)

    return result


def generate_binary_chromosome(): # Generate aleatory vector of binaries
    chromosome = []
    for _ in range(chromosome_alleles_number):
        if random.random() >= 0.5:
            chromosome.append(1)
        else:
            chromosome.append(0)

    return chromosome


def interval_precision(interval_value, chromosome_position, x): # Define the precision of each interval in each
    # dimension, in this case, a 1024 precision intervals.

    xintervals = intervals[x][0] + chromosome_position * ((interval_value[1] - (interval_value[0])) / 1024)

    return xintervals


def convert_binary_to_decimal(chromosome): # Convert each binary dimension to your decimal representation based on inter
    # val precision.

    binary_chromosome_representation = []  # Representa as variaveis que vao adquirir o valor binario da parcial
    real_chromosome_representation = []  # Representa as variaves que vao adquirir o valor real das variaveis binarias

    parcial = int(chromosome_alleles_number / dimensions)

    while len(binary_chromosome_representation) != dimensions:
        binary_chromosome_representation.append(chromosome[:parcial])
        chromosome = chromosome[parcial:]

    for x in range(len(binary_chromosome_representation)):  # len de binaryChrome = len de variaveis da function
        binary_chromosome_representation[x] = ''.join(str(x) for x in binary_chromosome_representation[x])
        # Get a list of multiple lists each one representing a single dimension

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
        return "Fitness: {}".format(1 / self.fitness)


def initialize_population(population):
    return [Agent() for _ in range(population)]


def define_fitness(agents):

    for agent in agents:
        agent.fitness = 1 / function_x(agent.chromosomeINT)

    return agents


def find_global_best(agents, bestAgent):
    new_possible_best = max(agents, key=attrgetter('fitness'))

    if bestAgent.fitness < new_possible_best.fitness:
        bestAgent = copy.deepcopy(new_possible_best)

    return bestAgent


def calculate_fitness_percentage(agents):
    _sum = 0
    for agent in agents:
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
        del agents[0]  # Destruo todas as referencias dos objetos antigos

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


def crossover(selected_list, crossover_percentage, agents, bestAgent):
    new_generation = []

    for _ in range(int(crossover_percentage / 2)):  # Crossando sempre 80% da population

        random_dad = random.choice(selected_list)
        dad = copy.deepcopy(random_dad)

        random_mom = random.choice(selected_list)
        while random_mom == random_dad:
            random_mom = random.choice(selected_list)

        mom = copy.deepcopy(random_mom)

        child1 = Agent()
        child2 = Agent()
        # ONE POINT CROSSOVER
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
    new_generation.remove(min(agents, key=attrgetter('fitness')))
    new_generation.append(bestAgent)

    new_generation = define_fitness(new_generation)

    return new_generation


def mutar(agents, mutation_percentage):
    mutations_number = int((population * chromosome_alleles_number) * mutation_percentage)

    for _ in range(mutations_number):
        randomic_agent = random.choice(agents)

        while randomic_agent.mutated == True:
            randomic_agent = random.choice(agents)

        agent_tobe_muted = copy.deepcopy(randomic_agent)
        agents.remove(randomic_agent)

        pontoCorte = random.randint(1, chromosome_alleles_number - 1)
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
    agents = initialize_population(population)  # Inicio uma population aleatoria
    bestAgent = copy.deepcopy(agents[0])

    for generation in range(generations):
        print("Geracao " + str(generation))

        agents = define_fitness(agents)  # Defino a fitness
        agents = calculate_fitness_percentage(agents)  # Calculo o percentual na rolate
        agents = define_roulette_range(agents)  # Defino o range na roleta
        bestAgent = find_global_best(agents, bestAgent)
        agents = select_by_roulette(agents)
        print("BEST AGENT", bestAgent)
        selected_list, agents = select_for_crossover(
            agents)  # Seleciono novos individuos a partir da generation anterior
        agents = crossover(selected_list, crossover_percentage, agents, bestAgent)  # Crosso esses individuos
        agents = mutar(agents, mutation_percentage)  # Muto eles

        print(max(agents, key=attrgetter('fitness')))


execGA(crossover_percentage, mutation_percentage)
from debug import debug_print
import random
from measure import Measure
import math


def initial_population(population_count, num_measures=1):
    random.seed()
	# population is represented as a list of lists where the inner lists are each a list of measures (which represents one gene)
	# TODO: add parameters for random_measure from user options
    return [[Measure.random_measure() for _ in range(num_measures)] for _ in range(population_count)]


# fitness is calculated as follows:
# sum(abs(target_measure - actual_measure) for each measure)
# measurement_funcs is a list of functions that calculate measurements of a series of notes
# measurement_targets is a list of the values for each measure that contribute the most fitness for that measure
# measurement_weights is a list of weights to add influence to the values of various measures
# if no list of weights is provided, all measures are weighted equally
def fitness(gene, measurement_funcs=Measure.DEFAULT_MEASUREMENTS, measurement_targets=Measure.DEFAULT_TARGETS, measurement_weights=None):
	if len(measurement_funcs) == 0 or len(measurement_targets) == 0:
		raise ValueError("Measurement functions and measure target values must be provided.")
	if len(measurement_funcs) != len(measurement_targets):
		raise ValueError("The same number of measurement functions and target values must be provided.")
	if measurement_weights is None:
		measurement_weights = [1 for _ in range(len(measurement_funcs))]
	if len(measurement_weights) != len(measurement_funcs):
		raise ValueError("The same number of measurement weights and measurement functions must be provided.")
	result = 0
	# TODO: allow for measurements that take into account neighboring measures
    for measure in gene:
		for i in range(len(measurement_funcs)):
			measure_val = measurement_funcs[i](measure)
			result -= math.abs(measure_val - measurement_targets[i]) * measurement_weights[i]
    return result


def selection(population):
    if not population:
        return []
    # TODO: allow different options for the fitness function
    fitnesses = [fitness(x) for x in population]
    mean_fitness = sum(fitnesses) / len(fitnesses)
    selected_population = []
    for i in range(len(population)):
        proportion = fitnesses[i] // mean_fitness
        for _ in range(int(proportion)):
            selected_population.append(population[i])
    diff_len = len(population) - len(selected_population)
    for _ in range(diff_len):
        selected_population.append(random.choice(population))
    return selected_population


# granularity is the power of 2 division that the crossover point will be chosen at
def crossover(population, percentage, granularity=3):
    mates = [x for x in population if random.random() < percentage]
    result = []
    if len(mates) % 2 == 1:
        mates.append(random.choice(population))
    for i in range(0, len(mates), 2):
        crossover_point = random.randint(0, 2 ** granularity)
		crossover_point *= 1 / (2 ** granularity)
		first = []
		second = []
		for measure_index in range(len(population[i])):
			first_split = population[i][measure_index].split(crossover_point)
			second_split = population[i + 1][measure_index].split(crossover_point)
			first.append(first_split[0] + second_split[1])
			second.append(first_split[1] + second_split[0])
        result.append(first)
        result.append(second)
		# TODO: add a step that fixes the resulting measures so that they are valid
    return result


# TODO: code below this line still needs to be refactored
def mutate(population, percentage):
    result = []
    for x in population:
        mutations = 0
        for i in range(GENE_BIT_COUNT):
            mutations |= (random.random() < percentage) << i
        result.append(x ^ mutations)
    return result


def run(options):
    num_measures = options['midi']['measures']
    num_notes = num_measures * 16
    num_iterations = options['genetic']['iterations']
    crossover_percentage = options['genetic']['crossover']
    mutation_percentage = options['genetic']['mutation']
    start_note = 60
    scale = options['midi']['scale']
	# TODO: chang ethe way initial population length is calculated
    num_initial_population = int(num_notes * (options['genetic']['crossover'] ** -options['genetic']['iterations']))
    debug_print("Calculated initial population: {}".format(num_initial_population))
    pop = initial_population(num_initial_population)
    favor_array = [1, 1, 1.5, 1, 2, 1, 1]
    favor_gain = 0.25
    for i in range(num_iterations):
        selected_pop = selection(pop, start_note, scale, favor_array, favor_gain)
        next_gen = crossover(selected_pop, crossover_percentage)
        pop = mutate(next_gen, mutation_percentage)
        debug_print('[')
        for item in pop:
            debug_print(format(item, '#011b'))
        debug_print(']')
        if len(pop) <= num_notes:
            break
    return pop

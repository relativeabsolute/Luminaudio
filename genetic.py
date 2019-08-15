from debug import debug_print
import random
from measure import Measure
from decimal import Decimal
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
		measurement_weights = [Decimal(1) for _ in range(len(measurement_funcs))]
	if len(measurement_weights) != len(measurement_funcs):
		raise ValueError("The same number of measurement weights and measurement functions must be provided.")
	result = Decimal(0)
	# TODO: allow for measurements that take into account neighboring measures
	for measure in gene:
		for i in range(len(measurement_funcs)):
			measure_val = Decimal(measurement_funcs[i](measure))
			result -= abs(measure_val - measurement_targets[i]) * measurement_weights[i]
	return result


def selection(population):
	if not population:
		return []
	# TODO: allow different options for the fitness function
	fitnesses = [fitness(x) for x in population]
	# min_fitness = min(fitnesses)
	# fitnesses = list(map(lambda fitness: fitness - min_fitness, fitnesses))
	# we use truncation selection for now
	selected = sorted(enumerate(fitnesses), key=lambda x: x[1])
	num_selected = len(selected)
	result = []
	for i in range(num_selected // 2, num_selected):
		result.append(population[selected[i][0]])
	return result


# granularity is the power of 2 division that the crossover point will be chosen at
def crossover(population, percentage, granularity=3):
	mates = random.sample(population, int(len(population) * percentage))
	result = []
	if len(mates) % 2 == 1:
		mates.append(random.choice(population))
	for i in range(0, len(mates), 2):
		crossover_point = Decimal(random.randint(0, 2 ** granularity))
		crossover_point *= Decimal(1 / (2 ** granularity))
		first = []
		second = []
		for measure_index in range(len(population[i])):
			first_split = population[i][measure_index].split(crossover_point)
			second_split = population[i + 1][measure_index].split(crossover_point)
			first_measure = Measure(first_split[0] + second_split[1])
			first_measure.fix()
			first.append(first_measure)
			second_measure = Measure(first_split[1] + second_split[0])
			second_measure.fix()
			second.append(second_measure) 
		result.append(first)
		result.append(second)
	return result


# creates a new population with the given percentage of notes mutated
# to have their midi note numbers changed
# the change is calculated from a gaussian distribution centered around the old note number
def mutate(population, percentage):
	result = []
	for gene in population:
		new_gene = []
		for measure in gene:
			new_notes = []
			for note in measure.notes:
				new_note = note
				if random.random() < percentage:
					# for now we vary the note number since
					# changing the note length would require the measure to be fixed
					new_note.midi_num = math.floor(random.gauss(note.midi_num, Measure.midi_number_stdev(measure)))
				new_notes.append(new_note)
			new_gene.append(Measure(new_notes))
		result.append(new_gene)
	return result


def run(options):
	# num_measures = options['midi']['measures']
	num_iterations = options['genetic']['iterations']
	crossover_percentage = options['genetic']['crossover']
	mutation_percentage = options['genetic']['mutation']
	#scale = options['midi']['scale']
	pop = initial_population(options['genetic']['population'])
	for i in range(num_iterations):
		if len(pop) == 1:
			break
		selected_pop = selection(pop)
		next_gen = selected_pop
		if len(selected_pop) > 1:
			next_gen = crossover(selected_pop, crossover_percentage)
		pop = mutate(next_gen, mutation_percentage)
	return pop

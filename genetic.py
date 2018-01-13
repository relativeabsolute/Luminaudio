from debug import debug_print
import random

# gene encoding: first bit represents positive change (increase) or negative change (decrease)
# next bits represent change in number of semitones
GENE_BIT_COUNT = 9

def initial_population(num):
    result = []
    random.seed()
    for _ in range(num):
        shift = random.gauss(4, 2) * 12
        sign = shift >= 48
        if sign:
            shift -= 48
        result.append((sign << 8) | int(shift))
    return result

def fitness(gene, start_note, scale):
    direction = 1 - 2 * ((gene & 0x100) >> 8)
    note_change_val = gene & 0xFF
    dest_note = start_note + note_change_val * direction
    result = 0
    if dest_note < 0 or dest_note > 127:
        result = 0
    else:
        # factors: for now simply note distance and interval type
        # perfect intervals: +0.5
        # major intervals: +0.4
        # minor intervals: +0.2
        # within octave: +1
        # within two octaves: +0.5
        # greater than 3 octaves: -0.75
        # TODO: allow different scales
        num_octaves = note_change_val // 12
        if num_octaves < 1:
            result += 1
        elif num_octaves < 2:
            result += 0.5
        elif num_octaves > 3:
            result -= 0.75
        base_interval = note_change_val - num_octaves * 12
        if not (base_interval in scale):
            result -= 0.25
        else:
            # TODO: favor certain interval types depending on the previous interval(s)
            result += 0.25
    return result

def selection(population, start_note, scale):
    if not population:
        return []
    # TODO: allow different starting notes
    fitnesses = [fitness(x, start_note, scale) for x in population]
    mean_fitness = sum(fitnesses) / len(fitnesses)
    debug_print("Fitnesses:")
    debug_print('\t{}'.format(str(fitnesses)))
    debug_print("Mean fitness:")
    debug_print('\t{}'.format(mean_fitness))
    selected_population = []
    for i in range(len(population)):
        proportion = fitnesses[i] // mean_fitness
        for _ in range(int(proportion)):
            selected_population.append(population[i])
    diff_len = len(population) - len(selected_population)
    for _ in range(diff_len):
        selected_population.append(random.choice(population))
    return selected_population

def crossover(population, percentage):
    mates = [x for x in population if random.random() < percentage]
    result = []
    if len(mates) % 2 == 1:
        mates.append(random.choice(population))
    for i in range(0, len(mates), 2):
        crossover_point = random.randrange(GENE_BIT_COUNT - 1)
        min_mask = 0x1ff >> (GENE_BIT_COUNT - crossover_point)
        max_mask = 0x1ff ^ min_mask
        first = mates[i] & min_mask | mates[i + 1] & max_mask
        second = mates[i + 1] & min_mask | mates[i] & max_mask
        result.append(first)
        result.append(second)
    return result

def mutate(population, percentage):
    result = []
    for x in population:
        mutations = 0
        for i in range(GENE_BIT_COUNT):
            mutations |= (random.random() < percentage) << i
        result.append(x ^ mutations)
    return result

def run(num_initial_population, num_iterations, crossover_percentage,
    mutation_percentage, start_note, scale):
    pop = initial_population(num_initial_population)
    for i in range(num_iterations):
        selected_pop = selection(pop, start_note, scale)
        next_gen = crossover(selected_pop, crossover_percentage)
        pop = mutate(next_gen, mutation_percentage)
        print('[', end='')
        for item in pop:
            print(format(item, '#011b'), end=',')
        print(']')
        if len(pop) <= 4:
            break
    return pop

from measure import Measure
import random
import requests
import measurements

# population generators must generate a population of measures based on
# the given parameters
# they must also (for now) have the side effect of settings the min and max
# notes in the measurement units dictionary

def from_json(options):
	population_count = options['genetic']['population']
	num_measures = options['genetic']['num_measures']

	parameters = options['randomness_source']['parameters']
	rest_chance = parameters['rest_chance']
	min_note = parameters['min_note']
	max_note = parameters['max_note']
	
	measurements.UNITS['note_num']['min'] = float(min_note)
	measurements.UNITS['note_num']['max'] = float(max_note)

	random.seed()
	# population is represented as a list of lists where the inner lists are each a list of measures (which represents one gene)
	return [[Measure.random_measure(rest_chance, min_note, max_note) for _ in range(num_measures)] for _ in range(population_count)]


def from_owm(options):
	population_count = options['genetic']['population']
	num_measures = options['genetic']['num_measures']

	parameters = options['randomness_source']['parameters']
	random.seed()

	url = 'https://api.openweathermap.org/data/2.5/forecast'
	payload = { 'zip': parameters['zip'], 'appid': parameters['client_key'],
		'units': 'metric' }
	resp = requests.get(url, params=payload)
	resp.raise_for_status()

	# TODO: fill in parameters based on weather forecast data
	return [[Measure.random_measure(rest_chance, min_note, max_note) for _ in range(num_measures)] for _ in range(population_count)]



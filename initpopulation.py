from measure import Measure
import random
import requests
import measurements
import statistics

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
		'units': 'imperial' } # using imperial because fahrenheit is easier to map to notes
	resp = requests.get(url, params=payload)
	resp.raise_for_status()

	resp_json = resp.json()
	min_temp = min(map(lambda item: item['main']['temp'], resp_json['list']))
	max_temp = max(map(lambda item: item['main']['temp'], resp_json['list']))

	temp_range = max_temp - min_temp
	
	min_note = int(min_temp * (60 / temp_range)) - 60
	max_note = int(max_temp * (60 / temp_range)) - 60

	print("min_temp: {}".format(min_temp))
	print("max_temp: {}".format(max_temp))
	print("min_note: {}".format(min_note))
	print("max_note: {}".format(max_note))

	measurements.UNITS['note_num']['min'] = float(min_note)
	measurements.UNITS['note_num']['max'] = float(max_note)

	return [[Measure.random_measure(0, min_note, max_note) for _ in range(num_measures)] for _ in range(population_count)]



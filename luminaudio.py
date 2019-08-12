import handle_options
import requests
import genetic
import midi
import json
import debug
from debug import debug_print
import argparse


# read json from specified file
# if specified file cannot be read, read config from config.json
def read_config(file_name):
	result_json = {}
	try:
		with open(file_name) as file_handle:
			result_json = json.load(file_handle)
	except FileNotFoundError:
		try:
			with open('config.json') as file_handle:
				result_json = json.load(file_handle)
		except FileNotFoundError:
			# we do this because there may be other exceptions we don't expect
			pass
	default_json = {}
	try:
		with open('defaults.json') as file_handle:
			default_json = json.load(file_handle)
	except FileNotFoundError:
		pass
	for default_category, default_keys in default_json.items():
		if default_category not in result_json:
			result_json[default_category] = default_keys
		else:
			for default_key, default_value in default_keys.items():
				if default_key not in result_json[default_category]:
					result_json[default_category][default_key] = default_value
	return result_json


# simply get some data to start with
def main():
	parser = argparse.ArgumentParser()

	parser.add_argument('--config_json', help='location of json configuration', default='config.json')
	options = vars(parser.parse_args())
	config_json = read_config(options['config_json'])
	debug.debug_flag = config_json['system']['debug']
	
	#url = 'https://api.openweathermap.org/data/2.5/weather?zip={}&appid={}'.format(options['zip'], options['owmkey'])
	#r = requests.get(url)
	#print(str(r.json()))
	ticks_per_quarter = config_json['midi']['ticks_per_quarter']
	example = midi.Midi(ticks_per_quarter)
	trk_chk = midi.Midi.TrackChunk(ticks_per_quarter)
	# TODO: calculate initial population size and number of iterations better
	# based on number of measures
	
	# for now: calculate it back based on crossover percentage and number of measures
	num_measures = config_json['midi']['measures']
	num_notes = num_measures * 16
	debug_print('Num notes: {}'.format(num_notes))
	# final_count = initial_population * (cross_over_percent ** num_iterations)
	# fix num_iterations since solving for an exponent is harder
	# final_count / initial_population = cross_over_percent ** num_iterations
	# initial_population = final_count * (cross_over_percent ** -num_iterations)
	
	
	start_note = 60
	debug_print("Start note: {}".format(start_note))
	result_sequence = genetic.run(config_json)
	sixteenth_note = ticks_per_quarter // 4
	trk_chk.add_event(1, 0, start_note, 96, 0)
	trk_chk.add_event(0, 0, start_note, 0, sixteenth_note)
	for item in result_sequence:
		new_note = get_new_note(start_note, item)
		debug_print('start_note = {}, new_note = {}'.format(start_note, new_note))
		trk_chk.add_event(1, 0, new_note, 96, 0)
		trk_chk.add_event(0, 0, new_note, 0, sixteenth_note)
	example.chunks.append(trk_chk)
	example.write_to_file(config_json['midi']['output'])
	

def get_new_note(start_note, encoded_change):
	sign = encoded_change & (0x100) > 0
	return start_note + (encoded_change & 0xFF) * sign


if __name__ == "__main__":
	main()


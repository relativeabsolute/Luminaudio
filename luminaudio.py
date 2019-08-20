#import requests
import genetic
import midi
import json
import argparse


def read_default_options():
	default_json = {}
	try:
		with open('defaults.json') as file_handle:
			default_json = json.load(file_handle)
	except FileNotFoundError:
		pass
	return default_json


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
	default_json = read_default_options()
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
	parser.add_argument('--force_defaults', help='force the use of default parameters (overriding user specified config)', action='store_true')
	options = vars(parser.parse_args())

	config_json = {}
	if options['force_defaults']:
		config_json = read_default_options()
	else:
		config_json = read_config(options['config_json'])
	
	ticks_per_quarter = config_json['midi']['ticks_per_quarter']
	midi_output = midi.Midi(ticks_per_quarter)
	trk_chk = midi.Midi.TrackChunk(ticks_per_quarter)
	
	
	# result sequence is a list containing a single list containing the resulting measures from the algorithm
	result_sequence = genetic.run(config_json)
	
	for measure in result_sequence[0]:
		print("Result measure: {}".format(measure))
		for note in measure.notes:
			note_length_ticks = int(ticks_per_quarter * note.note_len * 4)
			trk_chk.add_event(1, 0, note.midi_num, 96, 0)
			trk_chk.add_event(0, 0, note.midi_num, 0, note_length_ticks)
	midi_output.chunks.append(trk_chk)
	midi_output.write_to_file(config_json['midi']['output'])
	

if __name__ == "__main__":
	main()


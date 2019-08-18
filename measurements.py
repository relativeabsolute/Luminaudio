from operator import attrgetter
import statistics
from measure import Note


# contains measurement functions that only operate on a single measure
class SingleMeasurements:


	# calculate the percentage of the measure that are rests
	def percent_vacant(measure):
		return float(sum(map(attrgetter('note_len'), filter(attrgetter('is_rest'), measure.notes))))


	def note_length_stdev(measure):
		if len(measure.notes) <= 1:
			return 0
		return float(statistics.stdev(map(attrgetter('midi_num'), measure.notes)))


	def note_length_mean(measure):
		if len(measure.notes) < 1:
			return 0
		return float(statistics.mean(map(attrgetter('midi_num'), measure.notes)))


	def midi_number_stdev(measure):
		if len(measure.notes) <= 1:
			return 0
		return float(statistics.stdev(map(attrgetter('midi_num'), measure.notes)))

	
	def midi_number_mean(measure):
		if len(measure.notes) < 1:
			return 0
		return float(statistics.mean(map(attrgetter('midi_num'), measure.notes)))


UNITS = {
	'note_length': { 'min': 0.0, 'max': 1.0 },
	# the values for note_num are just placeholders
	# since they get changed by the user config anyway
	'note_num': { 'min': 0, 'max': 128 }, 
	'percent': { 'min': 0.0, 'max': 1.0 }
}


def min_max_normalize(value, unit):
	min_value = UNITS[unit]['min']
	max_value = UNITS[unit]['max']
	return (value - min_value) / (max_value - min_value)


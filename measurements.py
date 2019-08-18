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
	'note_num': { 'min': float(Note.MIN_MIDI_NOTE), 'max': float(Note.MAX_MIDI_NOTE) },
	'percent': { 'min': 0.0, 'max': 1.0 }
}


def min_max_normalize(value, unit):
	min_value = UNITS[unit]['min']
	max_value = UNITS[unit]['max']
	return (value - min_value) / (max_value - min_value)


DEFAULT_MEASUREMENTS = [SingleMeasurements.percent_vacant,
	SingleMeasurements.note_length_stdev, SingleMeasurements.note_length_mean,
	SingleMeasurements.midi_number_stdev, SingleMeasurements.midi_number_mean]

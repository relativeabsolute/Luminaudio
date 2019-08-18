from operator import attrgetter
import statistics


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


DEFAULT_MEASUREMENTS = [SingleMeasurements.percent_vacant,
	SingleMeasurements.note_length_stdev, SingleMeasurements.note_length_mean,
	SingleMeasurements.midi_number_stdev, SingleMeasurements.midi_number_mean]

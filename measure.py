from decimal import Decimal
import math
import random
import statistics


class Note:
	MIN_MIDI_NOTE = 21
	MAX_MIDI_NOTE = 108
	decimal_two = Decimal(2)


	def __init__(self, note_num=60, note_len=Decimal(0.25), dotted=False, is_rest=False):
		self.midi_num = note_num
		self.note_len = Decimal(note_len)
		self.dotted = dotted
		self.is_rest = is_rest


	# checks if the note has a valid length
	# returns true if log_2(note_length) is a nonpositive integer
	def is_valid_length(self):
		log = self.note_len.log10() / Note.decimal_two.log10()
		return log <= 0 and math.ceil(log) == math.floor(log)


	# calculate the note's length, taking into account if the note is dotted
	def actual_length(self):
		multiplier = 1
		if self.dotted:
			multiplier = 1.5
		return self.note_len * multiplier


	def __str__(self):
		return "(Note number = {}, length = {}, is_rest = {}, dotted = {})".format(self.midi_num,
			self.note_len, self.is_rest, self.dotted)


class Measure:


	def __init__(self, notes=[]):
		self.notes = notes


	def __str__(self):
		return str(self.notes)


	# checks if the measure is a valid sequence of notes
	# for now we default to 4/4
	# measure is valid if each note is valid and if the note lengths
	# add up to 1
	def check_valid(self):
		sum_lengths = 0
		for note in self.notes:
			if not note.is_valid_length():
				return False
			sum_lengths += note.actual_length()
		return sum_lengths == 1


	# most basic possible random measure generation
	def random_measure(rests_chance=0, min_note=Note.MIN_MIDI_NOTE, max_note=Note.MAX_MIDI_NOTE):
		length_left = Decimal(1)
		max_power = 0
		min_power = -4 # go down to sixteenth notes for now
		result = []
		while length_left > 0:
			note_length = Note.decimal_two ** random.randint(min_power, max_power)
			length_left -= note_length
			if length_left > 0:
				while length_left < Note.decimal_two ** max_power:
					max_power -= 1
			note_num = random.randint(min_note, max_note)
			is_rest = random.random() < rests_chance
			result.append(Note(note_num=note_num, note_len=note_length, is_rest=is_rest))
		return Measure(notes=result)


	# calculate the percentage of the measure that are rests
	def percent_vacant(self):
		return sum(map(lambda note: note.actual_length(), filter(lambda note: note.is_rest, self.notes)))


	def note_length_stdev(self):
		return statistics.stdev(map(lambda note: note.actual_length(), self.notes))


	def midi_number_stdev(self):
		return statistics.stdev(map(lambda note: note.midi_num, self.notes))


	# TODO: include measure for presence of patterns/motifs in the measure

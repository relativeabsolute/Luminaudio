from decimal import Decimal
import math
import random


class Note:
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
			note_length = note.note_len
			if note.dotted:
				note_length *= 1.5
			sum_lengths += note_length
		return sum_lengths == 1


	# most basic possible random measure generation
	def random_measure(rests_chance=0, min_note=21, max_note=108):
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

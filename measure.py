from decimal import Decimal
import math
import random


class Note:
	decimal_two = Decimal(2)


	def __init__(self, note_num=60, note_len=Decimal(0.25), is_rest=False):
		self.midi_num = note_num
		self.note_len = Decimal(note_len)
		self.is_rest = is_rest


	# checks if the note has a valid length
	# returns true if the note is a multiple of a nonpositive power of two
	def is_valid_length(self):
		numer, denom = map(Decimal, self.note_len.as_integer_ratio())
		log = denom.log10() / self.decimal_two.log10()
		return math.ceil(log) == math.floor(log) and numer <= denom


	def __str__(self):
		return "(Note number = {}, length = {}, is_rest = {})".format(self.midi_num,self.note_len, self.is_rest)


class Measure:
	def __init__(self, notes=[]):
		self.notes = notes


	def __str__(self):
		return '[{}]'.format(', '.join(str(note) for note in self.notes))


	def total_note_length(self):
		return sum(map(lambda note: note.note_len, self.notes))


	# checks if the measure is a valid sequence of notes
	# for now we default to 4/4
	# measure is valid if the total length of the notes is 1	
	def check_valid(self):
		return self.total_note_length() == 1


	# splits the measure at the specified cutoff point and 
	# returns a tuple containing the note lists of the two halves
	def split(self, cutoff_point):
		running_total = 0
		current_index = 0
		while running_total < cutoff_point:
			running_total += self.notes[current_index].note_len
			current_index += 1
		if running_total > cutoff_point:
			current_index -= 1
		return (self.notes[0: current_index], self.notes[current_index:])


	# fix note lengths so that the measure is valid
	def fix(self):
		total_length = self.total_note_length()
		if total_length == 1:
			return
		new_notes = []			
		new_length = 0
		current_index = 0
		while new_length < 1 and current_index < len(self.notes):
			next_sum = new_length + self.notes[current_index].note_len
			if next_sum <= 1:
				new_length = next_sum
				new_notes.append(self.notes[current_index])
				current_index += 1
			else:
				# this is necessary for the cases where the last note in the list
				# would go over 1, causing an infinite loop
				break
		if new_length < 1:
			diff = 1 - new_length
			new_notes[-1].note_len += diff
		self.notes = new_notes
				


	# most basic possible random measure generation
	def random_measure(rests_chance, min_note, max_note):
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



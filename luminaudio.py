import handle_options
import requests
import genetic
import midi
from debug import debug_print

# simply get some data to start with
def main():
    options = handle_options.parse_args()
    debug_print('Options passed:')
    debug_print(str(options))
    #url = 'https://api.openweathermap.org/data/2.5/weather?zip={}&appid={}'.format(options['zip'], options['owmkey'])
    #r = requests.get(url)
    #print(str(r.json()))
    ticks_per_quarter = options.get('ticks_per_quarter', 960)
    example = midi.Midi(ticks_per_quarter)
    trk_chk = midi.Midi.TrackChunk(ticks_per_quarter)
    # TODO: calculate initial population size and number of iterations better
    # based on number of measures
    
    # for now: calculate it back based on crossover percentage and number of measures
    num_measures = options.get('num_measures', 4)
    num_notes = num_measures * 16
    debug_print('Num notes: {}'.format(num_notes))
    # final_count = initial_population * (cross_over_percent ** num_iterations)
    # fix num_iterations since solving for an exponent is harder
    # final_count / initial_population = cross_over_percent ** num_iterations
    # initial_population = final_count * (cross_over_percent ** -num_iterations)
    initial_population = int(num_notes * (options['crossover'] ** -options['iterations']))
    debug_print("Calculated initial population: {}".format(initial_population))
    start_note = options.get('start_note', 60)
    debug_print("Start note: {}".format(start_note))
    result_sequence = genetic.run(initial_population, options['iterations'],
        options['crossover'], options['mutation'], start_note, options['scale'])
    sixteenth_note = ticks_per_quarter // 4
    trk_chk.add_event(1, 0, start_note, 96, 0)
    trk_chk.add_event(0, 0, start_note, 0, sixteenth_note)
    for item in result_sequence:
        new_note = get_new_note(start_note, item)
        debug_print('start_note = {}, new_note = {}'.format(start_note, new_note))
        trk_chk.add_event(1, 0, new_note, 96, 0)
        trk_chk.add_event(0, 0, new_note, 0, sixteenth_note)
    example.chunks.append(trk_chk)
    example.write_to_file(options['output'])
    

def get_new_note(start_note, encoded_change):
    sign = encoded_change & (0x100) > 0
    return start_note + (encoded_change & 0xFF) * sign

if __name__ == "__main__":
    main()


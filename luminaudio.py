import handle_options
import requests
import genetic
import midi

# simply get some data to start with
def main():
    options = handle_options.parse_args()
    if options['debug']:
        print('Options passed:')
        print(str(options))
    #url = 'https://api.openweathermap.org/data/2.5/weather?zip={}&appid={}'.format(options['zip'], options['owmkey'])
    #r = requests.get(url)
    #print(str(r.json()))
    example = midi.Midi()
    trk_chk = midi.Midi.TrackChunk(960)
    result_sequence = genetic.run(options['population'], options['iterations'],
        options['crossover'], options['mutation'])
    current_note = 60
    sixteenth_note = 960 // 4
    trk_chk.add_event(1, 0, 60, 96, 0)
    trk_chk.add_event(0, 0, 60, 0, sixteenth_note)
    for item in result_sequence:
        new_note = get_new_note(current_note, item)
        print('current_note = {}, new_note = {}'.format(current_note, new_note))
        trk_chk.add_event(1, 0, new_note, 96, 0)
        trk_chk.add_event(0, 0, new_note, 0, sixteenth_note)
    example.chunks.append(trk_chk)
    example.write_to_file('example2.mid')
    

def get_new_note(current_note, encoded_change):
    sign = encoded_change & (0x100) > 0
    return current_note + (encoded_change & 0xFF) * sign

if __name__ == "__main__":
    main()


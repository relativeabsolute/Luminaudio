import argparse
import debug

# as it is now, arguments in a file will overwrite those specified on command line
# TODO: figure out how to reverse that

# options that yet to have command line arguments:
# favor_gain: coefficient for favored intervals
# favor_intervals: array of degrees to favor certain intervals.  Must be same length as the scale array.
def parse_args():
    parser = argparse.ArgumentParser()

    # TODO: put weather info in
    #parser.add_argument('owmkey', help='key needed to access OpenWeatherMap API.  Can be key itself or textfile')
    #parser.add_argument('zip', help='zip code for location to find weather data for.')
    parser.add_argument('-o', '--output', help='name of the file to output resulting MIDI to.', default='output.mid')
    parser.add_argument('--debug', help='Print verbose debug info.', action='store_true')
    parser.add_argument('-n', '--iterations', help='number of iterations to perform in the genetic algorithm.', default=4, type=int)
    parser.add_argument('-p', '--population', help='initial population count.', default=20, type=int)
    parser.add_argument('-c', '--crossover', help='crossover percentage', default=0.5, type=float)
    parser.add_argument('-m', '--mutation', help='mutation percentage', default=0.01, type=float)
    parser.add_argument('--midi_config', help='location of file containing midi options', default='')
    parser.add_argument('--genetic_config', help='location of file containing parameters for the genetic algorithm', default='')
    parser.add_argument('--scale_file', help='location of file containing scale', default='')
    options = vars(parser.parse_args())
    debug.debug_flag = options['debug']
    options.update(read_options_file(options['midi_config']))
    options.update(read_options_file(options['genetic_config']))
    if not 'scale' in options:
        options['scale'] = get_scale(options['scale_file'])
    #if options['owmkey'].endswith('.txt'):
    #    filename = options['owmkey']
    #    with open(filename, 'r') as file_content:
    #        content = file_content.read()
    #        options['owmkey'] = content.strip()
    return options


def read_options_file(file_name):
    result = {}
    if file_name:
        with open(file_name) as f:
            for line in f:
                split = line.strip().split('=')
                result[split[0]] = float(split[1])
    return result


# ticks_per_quarter (default = 960)
# num_measures (default = 4)
# start_note (default = 60)
def get_midi_options(midi_config_file):
    result = {}
    if midi_config_file:
        with open(midi_config_file) as f:
            for line in f:
                split = line.strip().split('=')
    return result


# note: scale is number of semitones away from the *root* note
# TODO: figure out in terms of previous note instead of root note
def get_scale(scale_file):
    # major scale
    default_scale = [0, 2, 4, 5, 7, 9, 11]
    result = default_scale
    if scale_file:
        with open(scale_file) as f:
            result = [int(x) for x in f.read().strip().split(',')]
    return result

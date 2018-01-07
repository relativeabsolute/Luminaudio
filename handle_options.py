import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('owmkey', help='key needed to access OpenWeatherMap API.  Can be key itself or textfile')
    parser.add_argument('zip', help='zip code for location to find weather data for.')
    parser.add_argument('-o', '--output', help='name of the file to output resulting MIDI to.', default='output.midi')
    parser.add_argument('--debug', help='Print verbose debug info.', action='store_true')
    parser.add_argument('-n', '--iterations', help='number of iterations to perform in the genetic algorithm.', default=100, type=int)
    parser.add_argument('-p', '--population', help='initial population count.', default=20, type=int)
    parser.add_argument('-c', '--crossover', help='crossover percentage', default=0.5, type=float)
    parser.add_argument('-m', '--mutation', help='mutation percentage', default=0.01, type=float)
    options = vars(parser.parse_args())
    if options['owmkey'].endswith('.txt'):
        filename = options['owmkey']
        with open(filename, 'r') as file_content:
            content = file_content.read()
            options['owmkey'] = content.strip()
    return options


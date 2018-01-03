import argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('owmkey', help='key needed to access OpenWeatherMap API.  Can be key itself or textfile')
    parser.add_argument('zip', help='zip code for location to find weather data for.')
    parser.add_argument('-o', '--output', help='name of the file to output resulting MIDI to.', default='output.midi')
    parser.add_argument('--debug', help='Print verbose debug info.', action='store_true')
    options = vars(parser.parse_args())
    if options['owmkey'].endswith('.txt'):
        filename = options['owmkey']
        with open(filename, 'r') as file_content:
            content = file_content.read()
            options['owmkey'] = content.strip()
    return options


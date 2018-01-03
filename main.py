import handle_options
import requests


# simply get some data to start with
def main():
    options = handle_options.parse_args()
    if options['debug']:
        print('Options passed:')
        print(str(options))
    url = 'https://api.openweathermap.org/data/2.5/weather?zip={}&appid={}'.format(options['zip'], options['owmkey'])
    r = requests.get(url)
    print(str(r.json()))

if __name__ == "__main__":
    main()


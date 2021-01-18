import json
from events import Events


def setup():
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    return config


def main():
    config = setup()
    events = Events(config['apiKey'])


if __name__ == "__main__":
    main()
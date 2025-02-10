import json

def load_config(config_file='config.txt'):
    """Load configuration from a text file."""
    config = {}
    with open(config_file, 'r') as file:
        for line in file:
            key, value = line.strip().split('=', 1)
            config[key] = value
    return config

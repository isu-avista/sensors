import yaml


def save(map, file):
    """Saves the current configuration"""
    with open(file, 'w') as f:
        yaml.dump(map, f)


def load(file):
    """Loads a configuration"""
    with open(file, 'r') as f:
        return yaml.load(f, Loader=yaml.FullLoader)

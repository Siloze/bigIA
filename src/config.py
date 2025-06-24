import configparser
import os

def load_config(filepath):
    config = configparser.ConfigParser()
    if not os.path.exists(filepath):
        return {}  # fichier absent => dict vide
    config.read(filepath, encoding='utf-8')
    result = {}
    for section in config.sections():
        result[section] = dict(config.items(section))
    return result

def get_param(filepath, section, key, default=None):
    config = configparser.ConfigParser()
    if not os.path.exists(filepath):
        return default
    config.read(filepath, encoding='utf-8')
    if config.has_section(section) and config.has_option(section, key):
        return config.get(section, key)
    else:
        return default

def set_param(filepath, section, key, value):
    config = configparser.ConfigParser()
    if os.path.exists(filepath):
        config.read(filepath, encoding='utf-8')
    if not config.has_section(section):
        config.add_section(section)
    config.set(section, key, str(value))
    with open(filepath, 'w', encoding='utf-8') as f:
        config.write(f)

import configparser
import os

from pyqt_openai import MAXIMUM_MESSAGES_IN_PARAMETER, DEFAULT_USER_IMAGE_PATH, DEFAULT_AI_IMAGE_PATH, \
    DEFAULT_FONT_SIZE, DEFAULT_FONT_FAMILY, QFILEDIALOG_DEFAULT_DIRECTORY, CONFIG_DATA

_config_cache = None


def parse_value(value):
    # Boolean conversion
    if value.lower() in ('true', 'false'):
        return value.lower() == 'true'
    # Numeric conversion
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            pass
    # Default: return the value as is (string)
    return value


def convert_list(value):
    # Convert comma-separated string to list
    return [item.strip() for item in value.split(',')]


def ini_to_yaml():
    ini_old_filename = 'pyqt_openai.ini'
    if os.path.exists(ini_old_filename):
        ini_new_filename = 'config.ini'
        if os.path.exists(ini_old_filename):
            os.rename(ini_old_filename, ini_new_filename)

        # Open INI file
        config = configparser.ConfigParser()

        config.read(ini_new_filename)

        # Convert to yaml data
        yaml_data = {}
        for section in config.sections():
            yaml_data[section] = {}
            for key, value in config.items(section):
                if key in ['chat_column_to_show', 'image_column_to_show']:
                    yaml_data[section][key] = convert_list(value)
                else:
                    yaml_data[section][key] = parse_value(value)

        os.remove(ini_new_filename)
    else:
        yaml_data = CONFIG_DATA

    yaml_filename = 'config.yaml'
    if not os.path.exists(yaml_filename):
        # Save as YAML file
        with open(yaml_filename, 'w') as yaml_file:
            yaml.dump(yaml_data, yaml_file, default_flow_style=False)

def load_config(file_path='config.yaml'):
   global _config_cache
   if _config_cache is None:
       with open(file_path, 'r') as file:
           _config_cache = yaml.safe_load(file)
   return _config_cache


import yaml

class ConfigManager:
    def __init__(self, yaml_file):
        self.yaml_file = yaml_file
        self.config = self._load_yaml()

    def _load_yaml(self):
        with open(self.yaml_file, 'r') as file:
            return yaml.safe_load(file)

    def _save_yaml(self):
        with open(self.yaml_file, 'w') as file:
            yaml.safe_dump(self.config, file)

    # Getter methods
    def get_dalle(self):
        return self.config.get('DALLE', {})

    def get_general(self):
        return self.config.get('General', {})

    def get_dalle_property(self, key):
        return self.config.get('DALLE', {}).get(key)

    def get_general_property(self, key):
        return self.config.get('General', {}).get(key)

    # Setter methods
    def set_dalle_property(self, key, value):
        if 'DALLE' not in self.config:
            self.config['DALLE'] = {}
        self.config['DALLE'][key] = value
        self._save_yaml()

    def set_general_property(self, key, value):
        if 'General' not in self.config:
            self.config['General'] = {}
        self.config['General'][key] = value
        self._save_yaml()

# yaml_filename = 'config.yaml'

# with open(yaml_filename, 'w') as yaml_file:
#     yaml.dump(CONFIG_DATA, yaml_file, default_flow_style=False)

# ini_to_yaml()
# config = ConfigManager('config.yaml')
# print(type(config.get_dalle()['directory']))
# print(type(config.get_dalle()['prompt']))
import configparser
import os

# Crear un objeto ConfigParser
config_process = configparser.ConfigParser()

config_path = os.path.join(os.path.dirname(__file__), 'process.properties')
config_process.read(config_path)

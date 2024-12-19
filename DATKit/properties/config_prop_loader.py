import configparser
import os

# Crear un objeto ConfigParser
config_config = configparser.ConfigParser()

config_path = os.path.join(os.path.dirname(__file__), 'config.properties')
# print(f"Ruta del archivo de configuración: {config_path}")

config_config.read(config_path)
# print(f"Secciones disponibles en config: {config_config.sections()}")

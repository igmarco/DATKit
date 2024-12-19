import logging
# import os
import sys
from DATKit.properties.config_prop_loader import config_config
from DATKit.properties.prop_parser import parse_value

# Manejo de excepciones en configuraciones
try:
    # print("Contenido de DEFAULT:", config_config['DEFAULT'])
    log = parse_value(config_config.get('DEFAULT', 'log', fallback=True))
    log_filename = parse_value(config_config.get('LOGGING', 'log_filename', fallback='log.log'))

    # log_path = os.path.join(os.path.dirname(__file__), log_filename)

    # Configuración del logger
    logger = logging.getLogger("my_logger")
    if log and not logger.handlers:
        handler = logging.FileHandler(log_filename)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.ERROR)


    def log_uncaught_exceptions(exc_type, exc_value, exc_traceback):
        if not issubclass(exc_type, KeyboardInterrupt):  # Ignorar interrupciones del teclado
            logger.error(
                "Excepción no manejada",
                exc_info=(exc_type, exc_value, exc_traceback)
            )
        # Llamar al comportamiento por defecto de excepthook
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    # Establecer la función para manejar excepciones globalmente
    sys.excepthook = log_uncaught_exceptions

    if logger:
        logger.error("Prueba de log: el logger está configurado correctamente.")

except Exception as e:
    print(f"Error al parsear configuraciones: {e}")
    log = False  # Desactiva logging si ocurre un error

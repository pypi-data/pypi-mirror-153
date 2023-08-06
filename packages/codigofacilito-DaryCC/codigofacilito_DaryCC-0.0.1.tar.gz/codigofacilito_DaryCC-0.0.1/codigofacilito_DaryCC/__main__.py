from codigofacilito_DaryCC import unreleased
import logging
"""
INFO-> 10
DEBUG-> 20
WARNING-> 30
ERROR-> 40
CRITICAL-> 50
"""
logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    logging.debug(">>> Estamos comenzando la ejecución del paquete.")
    # workshop = unreleased()
    logging.debug(help(unreleased)
                  )
    logging.debug(">>> Estamos finalizando la ejecución del paquete.")

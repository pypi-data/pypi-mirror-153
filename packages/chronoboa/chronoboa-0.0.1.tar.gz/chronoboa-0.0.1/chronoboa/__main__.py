import logging
from chronoboa import unreleased

"""
INFO -> 10
DEBUG -> 20
WARNING -> 30
ERROR -> 40
CRITICAL ->50
"""

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    logging.debug('>>> Estamos comenzando la ejecucion del paquete.')

    print('Hola, nos econtramos un paquete en python')
    # se ejecutan las pruebas
    # workshops = unreleased()
    # logging.debug(workshops)
    # print(workshops)
    logging.debug(help(unreleased))

    # print('Hola, nos econtramos un paquete en python')
    logging.debug('>>> Finalizando la ejecucion del paquete.')

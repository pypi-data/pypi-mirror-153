# archivo para ejecutar el paquete sin necesidad de llamarlo en un archivo

import logging
'''
    Imprime diferentes tipos de mensajes:
        info        10
        debug       20
        warning     30
        error       40
        critical    50
'''
from pythonPackageCodigofacilito import unreleased

logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    workshops = unreleased()
    # logging.debug(help(unreleased))
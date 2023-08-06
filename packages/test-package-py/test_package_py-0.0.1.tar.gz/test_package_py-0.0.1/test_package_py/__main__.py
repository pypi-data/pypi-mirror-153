import logging
from test_package_py import unreleased

logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    logging.debug(">>> Comenzado ejecucion del paquete.")

    workshops = unreleased()

    logging.debug(">>> Finalizado ejecucion del paquete.")

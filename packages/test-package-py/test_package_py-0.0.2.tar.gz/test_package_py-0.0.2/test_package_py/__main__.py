import logging
from test_package_py import unreleased

logging.basicConfig(level=logging.INFO)

def main():
    logging.info(unreleased())


if __name__ == '__main__':
    logging.debug(">>> Comenzado ejecucion del paquete.")

    main()

    logging.debug(">>> Finalizado ejecucion del paquete.")

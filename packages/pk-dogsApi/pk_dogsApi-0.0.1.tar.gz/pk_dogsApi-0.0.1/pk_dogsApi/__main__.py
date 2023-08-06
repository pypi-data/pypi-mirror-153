import logging 

logging.basicConfig(level=logging.DEBUG)

from pk_dogsApi import dogsList

if __name__ == '__main__':
    def main(): # Llamamos el método
        logging.info(dogsList())

    logging.debug('>>> Iniciando ejecución de Dogs List')
    logging.debug(help(dogsList.__doc__))

    main() # Ejecución del método

    logging.debug('>>> Finalizando ejecución')
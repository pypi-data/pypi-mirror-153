import logging 

logging.basicConfig(level=logging.DEBUG)

from pk_dogsApi import dogsList

def main(): # Llamamos el método
    logging.info(dogsList())

if __name__ == '__main__':

    logging.debug('>>> Iniciando ejecución de Dogs List')
    logging.debug(help(dogsList.__doc__))

    main() # Ejecución del método

    logging.debug('>>> Finalizando ejecución')
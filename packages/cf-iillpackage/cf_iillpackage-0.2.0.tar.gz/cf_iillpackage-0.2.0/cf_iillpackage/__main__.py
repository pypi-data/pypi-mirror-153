import logging

from cf_iillpackage import unreleased

"""
LOGGING

INFO -> 10
DEBUG -> 20
WARNING -> 30
ERROR -> 40
CRITICAL -> 50
"""

logging.basicConfig(level=logging.INFO)

def main():
    logging.info(unreleased())

if __name__ == '__main__':
    logging.debug('\n>>> Se está comenzando la ejecución del paquete.\n')

    main()

    logging.debug('\n>>> Dos visualizaciones sobre el docstring.\n')
    logging.debug(unreleased.__doc__)
    logging.debug(help(unreleased))

    logging.debug('\n>>> Se está finalizando la ejecución del paquete.')

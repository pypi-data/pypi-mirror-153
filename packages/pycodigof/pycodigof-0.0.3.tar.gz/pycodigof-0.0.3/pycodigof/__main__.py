import logging
from pycodigof import unreleased, all

#Config Level of logging
logging.basicConfig(level=logging.DEBUG)
def main():
    logging.info(">>> Todos los Workshops de CódigoFacilito.")
    logging.info(all())
    logging.info(">>> Los Workshops de CódigoFacilito que vienen a futuro.")
    logging.info(unreleased())

if __name__ == '__main__':
    logging.debug(">>> Estamos comenzando a ejecutar el paquete.")
    main()
    logging.debug(">>> Estamos finalizando la ejecución del paquete.")


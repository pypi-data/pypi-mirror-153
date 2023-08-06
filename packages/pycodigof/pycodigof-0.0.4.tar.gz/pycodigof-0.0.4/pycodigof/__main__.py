import logging
from pycodigof import unreleased, all, lastArticles

#Config Level of logging
logging.basicConfig(level=logging.INFO)
def main():
    logging.info(">>> Todos los Workshops de CódigoFacilito.")
    logging.info(all())
    logging.info(">>> Los Workshops de CódigoFacilito que vienen a futuro.")
    logging.info(unreleased())
    logging.info(">>> Los últimos 20 articulos publicados en CódigoFacilito.")
    logging.info(lastArticles())

if __name__ == '__main__':
    logging.debug(">>> Estamos comenzando a ejecutar el paquete. <<<\n")
    main()
    logging.debug(">>> Estamos finalizando la ejecución del paquete. <<<")


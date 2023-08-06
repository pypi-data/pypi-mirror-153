import logging
from pycodigof import unreleased

#Config Level of logging
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    workshops = unreleased()
    logging.debug(">>> Estamos obteniendo la información...")
    logging.debug(workshops)



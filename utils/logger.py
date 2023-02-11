import logging
import os

LOG_LEVEL = os.environ.get('LOGLEVEL', 'INFO').upper()

class Log:

    def __init__(self):
        logging.basicConfig(
            format='%(asctime)s %(levelname)-85 %(message)s', 
            level=LOG_LEVEL,
            datefmt='%Y-%m-%d %H:%M:%S'
            )

    def i(self, message: str):
        logging.info(message)

    def d(self, message: str):
        logging.debug(message)
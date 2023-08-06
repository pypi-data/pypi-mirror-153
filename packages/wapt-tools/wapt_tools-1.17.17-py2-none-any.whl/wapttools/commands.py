import logging
import sys

log = logging.getLogger()


def commands(downloader=None):
    """ Default main function for WAPT setup.py
    """

    logging_config = logging.StreamHandler(sys.stdout)
    logging_config.setFormatter(logging.Formatter('[%(asctime)s - %(levelname)8s] %(message)s'))
    log.addHandler(logging_config)
    log.setLevel(logging.INFO)

    if 'debug' in sys.argv:
        log.setLevel(logging.DEBUG)
        log.debug('DEBUG mode enabled')

    if downloader is not None:
        downloader()

import logging
import os

log = logging.getLogger()


def isPackage():
    """ Check if current folder is a WAPT package folder
    """
    if not os.path.isdir('WAPT'):
        log.debug('WAPT folder not found')
        return False

    path = os.path.join('WAPT', 'control')
    if not os.path.isfile(path):
        log.debug('WAPT/control file not found')
        return False

    path = os.path.join('WAPT', 'icon.png')
    if not os.path.isfile(path):
        log.debug('WAPT/icon.png file not found')
        return False

    path = os.path.join('version-check.json')
    if not os.path.isfile(path):
        log.debug('version-check.json file not found')
        return False

    path = os.path.join('setup.py')
    if not os.path.isfile(path):
        log.debug('setup.py file not found')
        return False

    return True

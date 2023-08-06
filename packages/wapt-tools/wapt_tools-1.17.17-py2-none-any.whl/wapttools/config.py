import logging
import json
import os
import sys

log = logging.getLogger(__name__)


def loadVersionCheck():
    """ Load version-check.json configuration file

    Returns
    -------
    config: dict
        configuration dictionnary
    """

    if not os.path.isfile('version-check.json'):
        log.critical('version-check.json file not found')
        sys.exit(1)

    with open('version-check.json') as file:
        config = json.load(file)

    return config


def loadControl():
    """ Load WAPT/control configuration file

    This only extract name and version.

    Returns
    -------
    config: dict
        configuration dictionnary
    """
    if not os.path.isdir('WAPT'):
        log.critical('WAPT folder not found')
        sys.exit(1)

    path = os.path.join('WAPT', 'control')
    if not os.path.isfile(path):
        log.critical('WAPT/control file not found')
        sys.exit(1)

    config = dict()
    with open(path, 'r') as control:
        for line in control:
            if line.startswith('package'):
                config['package'] = line.split(':')[1].strip()
            if line.startswith('name'):
                config['name'] = line.split(':')[1].strip()
            if line.startswith('version'):
                config['version'] = line.split(':')[1].split('-')[0].strip()
                config['build'] = line.split(':')[1].split('-')[1].strip()
            if line.startswith('architecture'):
                config['architecture'] = line.split(':')[1].strip()
            if line.startswith('maturity'):
                config['maturity'] = line.split(':')[1].strip()
            if line.startswith('homepage'):
                config['homepage'] = line.split(':', 1)[1].strip()

    return config

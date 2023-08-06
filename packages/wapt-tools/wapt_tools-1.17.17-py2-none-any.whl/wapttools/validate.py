import fnmatch
import json
import logging
import re
import os
from .control import controlCheck

log = logging.getLogger()


def validate():
    """ Validate a package
    """
    # Validate *.json files
    for root, _, files in os.walk('.'):
        for file in fnmatch.filter(files, '*.json'):
            path = os.path.join(root, file)
            log.debug('Validating json file {}'.format(path))
            with open(path, 'r') as json_file:
                try:
                    json.load(json_file)
                except ValueError:
                    log.error('{} is not a valid json file'.format(path))
                    return False

    # Validate WAPT/control file
    if not controlCheck():
        return False

    log.debug('Check for WAPT/icon.png')
    if not os.path.exists(os.path.join('WAPT', 'icon.png')):
        log.error('WAPT/icon.png missing')
        return False

    # Validate setup.py
    patterns = {
        r'^def install\(': False,
        r'^def uninstall\(': False,
        r'^def session_setup\(': False,
        r'^def audit\(': False,
        r'^def update_package\(': False,
        r'^def download_sources\(': False,
        r'.*__main__': False,
        r'.*wapttools\.commands\(': False,
    }
    with open('setup.py', 'r') as file:
        for line in file:
            if line[-2:] == '\r\n':
                log.error('Found CRLF in setup.py')
                return False

            log.debug('line: {}'.format(line[:-1]))

            for pattern in patterns.keys():
                if re.match(pattern, line):
                    log.debug('pattern {} found'.format(pattern))
                    patterns[pattern] = True

    check = True
    for key in patterns.keys():
        if not patterns[key]:
            log.error('{} not found in setup.py'.format(key))
        check &= patterns[key]

    return check

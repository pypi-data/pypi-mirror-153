import logging
import os
import re
import sys

log = logging.getLogger()

repo_base_url = 'https://gitlab.it.geovar.net/wapt/packages/'

ok = {
    'package': False,
    'name': False,
    'version': False,
    'architecture': False,
    'section': False,
    'maintainer': False,
    'description': False,
    'description_fr': False,
    'description_es': False,
    'description_pt': False,
    'depends': False,
    'conflicts': False,
    'maturity': False,
    'locale': False,
    'target_os': False,
    'min_os_version': False,
    'max_os_version': False,
    'min_wapt_version': False,
    'sources': False,
    'installed_size': False,
    'impacted_process': False,
    'audit_schedule': False,
    'editor': False,
    'licence': False,
    'keywords': False,
    'homepage': False,
    'changelog': False
}


def controlCheck():
    """ Validate WAPT/control configuration file
    """
    if not os.path.isdir('WAPT'):
        log.critical('WAPT folder not found')
        sys.exit(1)

    path = os.path.join('WAPT', 'control')
    if not os.path.isfile(path):
        log.critical('WAPT/control file not found')
        sys.exit(1)

    package_name = ''

    check = True

    with open(path, 'r') as control:
        for line in control:
            key = line.rstrip().split(':', 1)[0].strip()
            if line[-2:] == '\r\n':
                log.error('WAPT/control {} line contains CRLF'.format(key))
                check = False
            else:
                value = line.rstrip().split(':', 1)[1].strip()
                log.debug('{} => {}'.format(key, value))

                if key == 'package':
                    if value.startswith('geovar-'):
                        ok[key] = True
                        package_name = value
                    else:
                        log.warning('WAPT/control {}: value do not start with geovar-'.format(key))

                elif key == 'name':
                    if not value:
                        log.warning('WAPT/control {}: value is empty'.format(key))
                    else:
                        ok[key] = True

                elif key == 'version':
                    if value.endswith('-0'):
                        ok[key] = True
                    else:
                        log.warning('WAPT/control {}: value do not ends with -0'.format(key))

                elif key == 'architecture':
                    if re.match('^(all|x86|x64)$', value):
                        ok[key] = True
                    else:
                        log.warning('WAPT/control {}: invalid value {}, should be (all|x86|x64)'.format(key, value))

                elif key == 'section':
                    if value == 'base':
                        ok[key] = True
                    else:
                        log.warning('WAPT/control {}: invalid value {}, should be base'.format(key, value))

                elif key == 'maintainer':
                    if value == 'Geovariances IT Service (sysadmin@geovariances.com)':
                        ok[key] = True
                    else:
                        log.warning('WAPT/control {}: invalid value'.format(key))

                elif key.startswith('description'):
                    if not value:
                        log.warning('WAPT/control {}: empty value'.format(key))
                    else:
                        if value[-1:] == '.':
                            ok[key] = True
                        else:
                            log.warning('WAPT/control {}: do not end with a dot'.format(key))

                elif key == 'depends':
                    if package_name != 'geovar-wapt-tools' and 'geovar-wapt-tools' not in value:
                        log.warning('WAPT/control {}: should contains geovar-wapt-tools'.format(key))
                    else:
                        ok[key] = True

                elif key == 'conflicts':
                    ok[key] = True

                elif key == 'maturity':
                    if value != 'BETA':
                        log.warning('WAPT/control {}: should always be BETA'.format(key))
                    else:
                        ok[key] = True

                elif key == 'locale':
                    ok[key] = True

                elif key == 'target_os':
                    ok[key] = True

                elif key == 'min_os_version':
                    ok[key] = True

                elif key == 'max_os_version':
                    ok[key] = True

                elif key == 'min_wapt_version':
                    ok[key] = True

                elif key == 'sources':
                    if value.startswith(repo_base_url):
                        ok[key] = True
                    else:
                        log.warning('WAPT/control {}: should starts with {}'.format(key, repo_base_url))

                elif key == 'installed_size':
                    if not value or value.isdigit():
                        ok[key] = True
                    else:
                        log.warning('WAPT/control {}: should be an integer'.format(key))

                elif key == 'impacted_process':
                    ok[key] = True

                elif key == 'audit_schedule':
                    if value.isdigit():
                        ok[key] = True
                    else:
                        log.warning('WAPT/control {}: should be an integer'.format(key))

                elif key == 'editor':
                    if not value:
                        log.warning('WAPT/control {}: value is empty'.format(key))
                    else:
                        ok[key] = True

                elif key == 'licence':
                    if not value:
                        log.warning('WAPT/control {}: value is empty'.format(key))
                    else:
                        ok[key] = True

                elif key == 'keywords':
                    if not value:
                        log.warning('WAPT/control {}: value is empty'.format(key))
                    else:
                        ok[key] = True

                elif key == 'homepage' or key == 'changelog':
                    if value.startswith('https://'):
                        ok[key] = True
                    else:
                        log.warning('WAPT/control {}: should be an url'.format(key))

                else:
                    log.warning('WAPT/control {}: unwanted key'.format(key))
                    check = False

    for key in ok.keys():
        if not ok[key]:
            log.error('WAPT/control {}: invalid or missing value'.format(key))
        check &= ok[key]

    log.debug('check = {}'.format(check))

    return check

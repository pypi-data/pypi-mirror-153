import logging
import os
import requests
import time
from .check import isPackage
from .config import loadControl

log = logging.getLogger()


def annotate():
    """ Generate annotation

    Parameters
    ----------
    """
    if not isPackage():
        log.error('current folder does not contain a WAPT package')
        return False

    if os.environ.get('CI') is None:
        log.error('annotate should only be used under CI context')
        return False

    if os.environ.get('CI_COMMIT_BRANCH') is None or os.environ['CI_COMMIT_BRANCH'] != 'master':
        log.error('annotate should only be used on master branch')
        return False

    if os.environ.get('GRAFANA_SERVER') is None:
        log.error('missing GRAFANA_SERVER envrionment variable')
        return False

    if os.environ.get('GRAFANA_USER') is None:
        log.error('missing GRAFANA_USER envrionment variable')
        return False

    if os.environ.get('GRAFANA_PASSWD') is None:
        log.error('missing GRAFANA_PASSWD envrionment variable')
        return False

    if os.environ.get('GITLAB_USER_LOGIN') is None:
        log.error('missing GITLAB_USER_LOGIN environment variable')
        return False

    if os.environ.get('CI_PIPELINE_URL') is None:
        log.error('missing CI_PIPELINE_URL environment variable')
        return False

    url = 'https://{user}:{passwd}@{server}/api/annotations'.format(
        server=os.environ['GRAFANA_SERVER'],
        user=os.environ['GRAFANA_USER'],
        passwd=os.environ['GRAFANA_PASSWD']
    )

    control = loadControl()
    build_number = control['build']
    if os.environ.get('CI_PIPELINE_IID') is not None:
        build_number = os.environ.get('CI_PIPELINE_IID')

    payload = {
        'time': int(time.time()) * 1000,
        'timeEnd': int(time.time()) * 1000,
        'tags': ['wapt', '{package}'.format(package=control['package'])],
        'text': '{package} {version}-{build} ({hash})\n'
                'builded by {user} - see <a href={url}>build {pipeline}</a>'.format(
            package=control['name'],
            version=control['version'],
            build=build_number,
            hash=os.environ['CI_COMMIT_SHORT_SHA'],
            user=os.environ['GITLAB_USER_LOGIN'],
            url=os.environ['CI_PIPELINE_URL'],
            pipeline=os.environ['CI_PIPELINE_ID'])}

    r = requests.post(url, json=payload)
    if r.status_code != 200:
        log.info('Annotation creation failed with code: {}'.format(r.status_code))

    return True

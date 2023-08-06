import anybadge
import bs4
import datetime
import json
import logging
import pefile
import re
import requests
import tempfile
import os
from packaging import version
from pkg_resources import resource_string
from .config import loadControl, loadVersionCheck
from .download import save_url_to_file

log = logging.getLogger()


def getExeVersion(file):
    pe = pefile.PE(file)

    if 'VS_FIXEDFILEINFO' not in pe.__dict__:
        version = '0.0.0.0'
    elif not pe.VS_FIXEDFILEINFO:
        version = '0.0.0.0'
    else:
        verinfo = pe.VS_FIXEDFILEINFO[0]

        version = '{:d}.{:d}.{:d}.{:d}'.format(
            verinfo.FileVersionMS >> 16,
            verinfo.FileVersionMS & 0xFFFF,
            verinfo.FileVersionLS >> 16,
            verinfo.FileVersionLS & 0xFFFF)

    pe.close()
    return version


def latestVersion(force=False):
    """ Extract latest version defined by version-check.json

    Parameters
    ----------
    force: bool
        force download of big files to check version

    Returns
    -------
    version: string
        version extracted from web page
    """
    config = loadVersionCheck()

    if 'external_check' not in config:
        config['external_check'] = True

    control = loadControl()

    if not config['external_check']:
        return control['version'].split('-')[0]

    url_info = requests.head(config['url_version'], allow_redirects=True)
    # log.debug(url_info)
    if url_info.headers['Content-Type'] != 'application/octet-stream':
        content = requests.get(config['url_version']).text.strip()

        if config['html'] is True:
            soup = bs4.BeautifulSoup(content, 'html.parser')
            if 'index' in config:
                index = config['index']
            else:
                index = 0

            latest_version = soup.select(config['selector'])[index].contents[0].strip()

            # log.debug('index = {}'.format(index))
            # selected = soup.select(config['selector'])
            # log.debug('selected = {}'.format(selected))
            # log.debug('selected[{}] = {}'.format(index, selected[index]))
            # log.debug('selected[{}].contents[0] = {}'.format(index, selected[index].contents[0]))
            # latest_version = selected[index].contents[0].strip()
        else:
            latest_version = content

        if 'cleaners' in config and len(config['cleaners']) > 0:
            for cleaner in config['cleaners']:
                # log.debug('applying cleaner: {}'.format(cleaner))
                if 'grep' not in cleaner:
                    latest_version = re.sub(
                            cleaner['pattern'],
                            cleaner['rewrite'],
                            latest_version,
                            flags=re.DOTALL).strip()
                else:
                    result = []
                    for line in latest_version.split('\n'):
                        if re.match(cleaner['pattern'], line):
                            result.append(re.sub(cleaner['pattern'], cleaner['rewrite'], line))

                    if 'sort' in cleaner and cleaner['sort'] is True:
                        result.sort(key=lambda s: map(int, s.split('.')))
                        result = result[::-1]  # reverse list

                    latest_version = result[0]

    else:
        # log.debug(url_info.headers)
        if int(url_info.headers['Content-Length']) > 5000000:
            log.debug('file is {}Mb, more than 5Mb'.format(int(url_info.headers['Content-Length']) / 1000000))
        if int(url_info.headers['Content-Length']) < 5000000 or datetime.date.today().weekday() == 3 or force:
            file = tempfile.mkstemp()
            os.close(file[0])
            save_url_to_file(config['url_version'], file[1])
            latest_version = getExeVersion(file[1])
            os.unlink(file[1])
        else:
            log.debug('file size greater than 5Mb, returning current version')
            # log.debug(control['version'])
            latest_version = control['version'].split('-')[0]

    return latest_version.replace('\n', ' ').replace('\r', '')


# TODO:
# Check https://stackoverflow.com/questions/8049520/web-scraping-javascript-page-with-python
# to render javascript before extracting
def versionChecker(chat=False, badge=False, force=False):
    """ Compare latest version defined by version-check.json, versus WAPT/control one

    Parameters
    ----------
    chat: bool
        send results to chat
    badge: bool
        generate upstream badge

    Returns
    -------
    results: bool
        no upgrade needed, the current version is greater or equal to to latest version
    """
    control = loadControl()
    log.info('Current {} version: {}'.format(control['name'], control['version']))
    v_current = version.parse(control['version'])
    log.debug('v_current ' + str(v_current))

    latest_version = latestVersion(force)
    log.info('Latest {} version: {}'.format(control['name'], latest_version))
    v_latest = version.parse(latest_version)
    log.debug('v_latest ' + str(v_latest))

    if v_latest > v_current:
        log.info('New version available, please upgrade package')

        if chat:
            log.debug('Sending message to Chat webhook ...')
            if 'CHAT_WEBHOOK_URL' in os.environ:
                payload = resource_string('wapttools.data', 'chat_message.json')
                payload = payload.replace('{package}', control['name'])
                payload = payload.replace('{old_version}', control['version'])
                payload = payload.replace('{new_version}', latest_version)
                payload = payload.replace('{homepage}', control['homepage'])

                # Compact JSON string
                payload = json.dumps(json.loads(payload), separators=(',', ':'))

                requests.session().post(
                    os.environ['CHAT_WEBHOOK_URL'],
                    data=payload,
                    headers={'Content-Type': 'application/json; charset=UTF-8'}
                )
            else:
                log.warning('CHAT_WEBHOOK_URL environment variable not defined, unable to send chat message')
            log.debug('... done.')

        if badge:
            log.debug('generating badge ...')
            badge = anybadge.Badge(label='upstream', value='new', default_color='red')
            badge.write_badge('upstream.svg')

        return True

    if badge:
        log.debug('generating badge ...')
        badge = anybadge.Badge(label='upstream', value='ok', default_color='green')
        badge.write_badge('upstream.svg')

    return False

import datetime
import logging
import subprocess
import sys
from .config import loadControl

log = logging.getLogger()


def release():
    """ Release a package
    """
    version = loadControl()['version']
    hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).strip()
    date = datetime.datetime.now().strftime('%d/%m/%Y, %H:%M:%S')
    branch = 'release/v{version}-{hash}'.format(version=version, hash=hash)
    message = '"Release v{version} ({hash}) on {date}"'.format(version=version, hash=hash, date=date)
    message_noci = message[:-1] + ' [skip ci]"'

    def git_clean():
        exit_code = subprocess.call('git diff-index --quiet HEAD', shell=True)
        if exit_code == 0:
            return True
        else:
            subprocess.call('git diff-index HEAD', shell=True)
            return False

    def git_action(message, command, error='failed'):
        log.info(message)
        log.debug('command: {}'.format(command))
        exit_code = subprocess.call(command, shell=True)
        log.debug('exit code = {}'.format(exit_code))
        if exit_code != 0:
            log.error('failed')
            sys.exit(1)

    if not git_clean():
        log.critical('Cannot release with a dirty repository, please commit your changes')
        sys.exit(1)

    git_action('check if merge is needed', 'git pull --no-edit')
    # if not git_clean() what to do?

    git_action('retrieve remote tags', 'git pull --tags')

    git_action('create release branch', 'git checkout -b {branch} develop'.format(branch=branch))

    git_action('move to master branch', 'git checkout master')
    git_action('pull if needed', 'git pull --no-edit')
    git_action('merge release branch to master', 'git merge --no-ff {branch} --no-commit'.format(branch=branch))
    if not git_clean():
        git_action('commit the merged result', 'git commit -m {message} -a'.format(message=message))
    git_action('tag the merged result', 'git tag -a v{version}-{hash} -m {message}'.format(
        version=version,
        hash=hash,
        message=message))

    git_action('move to develop branch', 'git checkout develop')
    git_action('merge release branch to develop', 'git merge --no-ff {branch} --no-commit'.format(branch=branch))
    if not git_clean():
        git_action('commit the merged result', 'git commit -m {message} -a'.format(message=message_noci))

    git_action('delete release branch', 'git branch -d {branch}'.format(branch=branch))

    git_action('push all commits', 'git push --all')
    git_action('push all tags', 'git push --tags')

import logging
import gitlab
import os
import random
import sys
from pkg_resources import resource_string

log = logging.getLogger()

pipeline = '[![{text} status]({url}/wapt/packages/{package}/badges/{branch}/pipeline.svg?key_text={text})]({url}/wapt/packages/{package}/-/pipelines?&ref={branch})\n' # noqa
upstream = '![{text}]({url}/wapt/packages/{package}/-/jobs/artifacts/develop/raw/upstream.svg?job=version-check)'


def create(package, verbose=False):
    """ Create a new package
    """
    gl = gitlab.Gitlab.from_config()
    log.debug('Gitlab url: {}'.format(gl.url))

    if not package:
        log.critical('Package name missing, use --name')
        sys.exit(1)

    # Check if gitlab project exists
    projects = gl.projects.list(search=package)
    if len(projects) > 0:
        for project in projects:
            if project.name == package:
                log.error('Gitlab project {} already exists, aborting.'.format(package))
                sys.exit(1)

    if os.path.isdir(package):
        log.error('folder {} already exists, aborting.'.format(package))
        sys.exit(1)

    wapt_group = gl.groups.list(search='wapt')[0]
    packages_group = wapt_group.subgroups.list(search='packages')[0]
    project = gl.projects.create({'name': package, 'namespace_id': packages_group.id})

    command = 'git clone {}:wapt/packages/{}'.format(gl.url.replace('https://', 'git@'), package)
    log.debug(command)
    os.system(command)
    os.chdir(package)

    log.debug('creating README.md file')
    with open('README.md', 'w') as file:
        file.write('# WAPT {} package\n'.format(package))
        file.write('\n')
        file.write(pipeline.format(text='PROD', branch='master', url=gl.url, package=package))
        file.write(pipeline.format(text='DEV', branch='develop', url=gl.url, package=package))
        file.write(upstream.format(text='Upstream', url=gl.url, package=package))

    command = 'git add -A'
    log.debug(command)
    os.system(command)

    command = 'git commit -m "Add README.md" README.md'
    log.debug(command)
    os.system(command)

    command = 'git push'
    log.debug(command)
    os.system(command)

    command = 'git flow init -d'
    log.debug(command)
    os.system(command)

    log.debug('creating Visual Studio Code configuration')
    os.mkdir('.vscode')
    with open(os.path.join('.vscode', 'extensions.json'), 'w') as file:
        file.write(resource_string('wapttools.data', 'vscode_extensions.json'))
    with open(os.path.join('.vscode', 'launch.json'), 'w') as file:
        file.write(resource_string('wapttools.data', 'vscode_launch.json'))
    with open(os.path.join('.vscode', 'settings.json'), 'w') as file:
        file.write(resource_string('wapttools.data', 'vscode_settings.json'))

    log.debug('creating WAPT')
    os.mkdir('WAPT')
    with open(os.path.join('WAPT', 'control'), 'w') as file:
        file.write(resource_string('wapttools.data', 'wapt_control.txt').format(url=gl.url, package=package))
    with open(os.path.join('WAPT', 'icon.png'), 'wb') as file:
        file.write(resource_string('wapttools.data', 'default_icon.png'))

    log.debug('creating config')
    os.mkdir('config')
    open(os.path.join('config', '.gitkeep'), 'a').close()

    log.debug('creating sources')
    os.mkdir('sources')
    with open(os.path.join('sources', '.gitignore'), 'w') as file:
        file.write('*\n')
        file.write('!.gitignore\n')

    log.debug('creating miscellanous files')
    with open('.editorconfig', 'w') as file:
        file.write(resource_string('wapttools.data', 'editorconfig.ini'))

    with open('.env', 'w') as file:
        file.write('PYTHONHOME=C:\\Program Files (x86)\\wapt\n')
        file.write('PYTHONPATH=C:\\Program Files (x86)\\wapt\n')

    with open('.gitignore', 'w') as file:
        file.write('# Ignore genrated files\n')
        file.write('*.pyc\n')
        file.write('WAPT/certificate.crt\n')
        file.write('WAPT/*.sha256\n')
        file.write('WAPT/wapt.psproj\n')

    with open('.gitlab-ci.yml', 'w') as file:
        file.write('include:\n')
        file.write('  - project: "wapt/ci"\n')
        file.write('    file: "/wapt.yml"\n')

    with open('.flake8', 'w') as file:
        file.write(resource_string('wapttools.data', 'flake8.txt'))

    with open('.pre-commit-config.yaml', 'w') as file:
        file.write(resource_string('wapttools.data', 'pre-commit-config.yaml'))

    with open('version-check.json', 'w') as file:
        file.write(resource_string('wapttools.data', 'version-check.json'))

    script = resource_string('wapttools.data', 'setup.tmpl')
    with open('setup.py', 'w') as file:
        file.write(script)

    command = 'git add .'
    log.debug(command)
    os.system(command)

    command = 'git commit -m "Initial commit" -a'
    log.debug(command)
    os.system(command)

    # command = 'git push --all'
    # log.debug(command)
    # os.system(command)

    # Create schedule named AutoVersionChecker
    scheds = project.pipelineschedules.list()
    found = False
    for sched in scheds:
        if sched.description == 'AutoVersionChecker':
            found = True

    if not found:
        sched = project.pipelineschedules.create({
            'ref': 'develop',
            'description': 'AutoVersionChecker',
            'cron_timezone': 'Europe/Paris',
            'cron': '{} 5 * * *'.format(random.randint(0, 59)),
            'active': True
        })

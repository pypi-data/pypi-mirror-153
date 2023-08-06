import argparse
import logging
import os
import sys
from .vers import __version__
from .check import isPackage
from .version import versionChecker
from .validate import validate
from .create import create
from .build import build
from .release import release
from .hash import sha256sum
from .annotate import annotate
from .upload import upload
from .update import update

log = logging.getLogger()


def cli():
    parser = argparse.ArgumentParser(prog='wapt', description='WAPT packaging utility.')
    subparsers = parser.add_subparsers(
        title='commands',
        dest='command')

    subparsers.add_parser(
        'version',
        help='display cli version')

    parser_check = subparsers.add_parser(
        'check-version',
        help='check if new upstream package exists')

    parser_check.add_argument(
        '--force',
        help='force download for big files',
        action='store_true')

    parser_check.add_argument(
        '--chat',
        help='send results to chat',
        action='store_true')

    parser_check.add_argument(
        '--badge',
        help='generate badge',
        action='store_true')

    subparsers.add_parser(
        'validate',
        help='validate package')

    parser_new = subparsers.add_parser(
        'create',
        help='create a new package')

    parser_new.add_argument(
        '--name',
        help='name of the new package to create',
        type=str)

    parser_build = subparsers.add_parser(
        'build',
        help='build package from current folder')

    parser_build.add_argument(
        '--key',
        help='key path to sign package',
        type=str)

    parser_build.add_argument(
        '--release',
        help='release number of package',
        type=int)

    parser_build.add_argument(
        '--maturity',
        help='maturity of package, overrides WAPT/control content',
        type=str)

    parser_upload = subparsers.add_parser(
        'upload',
        help='upload package')

    parser_upload.add_argument(
        '--server',
        help='WAPT server',
        type=str)

    parser_upload.add_argument(
        '--user',
        help='User to connect server with',
        type=str)

    parser_upload.add_argument(
        '--keyfile',
        help='SSH private key',
        type=str)

    parser_upload.add_argument(
        '--filename',
        help='File to upload',
        type=str)

    subparsers.add_parser(
        'update',
        help='update package to latest version and download sources')

    subparsers.add_parser(
        'release',
        help='release package to production')

    subparsers.add_parser(
        'setup',
        help='initialize folder after git clone')

    parser_checksum = subparsers.add_parser(
        'checksum',
        help='compute checksum')

    parser_checksum.add_argument(
        '--file',
        help='file to be analyzed',
        type=str)

    # parser_annotate = subparsers.add_parser(
    subparsers.add_parser(
        'annotate',
        help='add annotation to grafana')

    parser.add_argument('--verbose', help='verbose output', action='store_true')
    parser.add_argument('--silent', help='no output except critical messages', action='store_true')

    args = parser.parse_args()

    logging_config = logging.StreamHandler(sys.stdout)
    logging_config.setFormatter(logging.Formatter('[%(asctime)s - %(levelname)8s] %(message)s'))
    log.addHandler(logging_config)

    if args.silent:
        log.setLevel(logging.CRITICAL)
    elif args.verbose:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    log.info('WAPT cli v{}'.format(__version__))

    if args.command == 'version':
        sys.exit(0)

    if args.command == 'check-version':
        if not isPackage():
            sys.exit(1)

        mismatch = versionChecker(chat=args.chat, badge=args.badge, force=args.force)
        if mismatch:
            if 'CI' in os.environ:
                sys.exit(0)
            else:
                sys.exit(1)
        else:
            sys.exit(0)

    if args.command == 'validate':
        if not isPackage():
            sys.exit(1)

        if not validate():
            log.error('not a valid package')
            sys.exit(1)
        else:
            log.info('valid package')
            sys.exit(0)

    if args.command == 'create':
        create(args.name)
        sys.exit(0)

    if args.command == 'build':
        build(key=args.key, release=args.release, maturity=args.maturity)
        sys.exit(0)

    if args.command == 'upload':
        upload(server=args.server, user=args.user, keyfile=args.keyfile, filename=args.filename)
        sys.exit(0)

    if args.command == 'update':
        if not isPackage():
            sys.exit(1)

        update()
        sys.exit(0)

    if args.command == 'release':
        if not isPackage():
            sys.exit(1)

        release()
        sys.exit(0)

    if args.command == 'setup':
        if sys.platform == 'win32':
            command = 'git config --local core.fileMode false'
            log.debug(command)
            os.system(command)
        command = 'git flow init --defaults --force'
        log.debug(command)
        os.system(command)
        if sys.platform != 'win32':
            command = 'pre-commit install'
            log.debug(command)
            os.system(command)
        sys.exit(0)

    if args.command == 'checksum':
        checksum = sha256sum(args.file)
        log.info('{file} checksum is {checksum}'.format(file=args.file, checksum=checksum))
        sys.exit(0)

    if args.command == 'annotate':
        annotate()
        log.info('Adding annotation')
        sys.exit(0)

import hashlib
import os
import logging
from .check import isPackage
from .control import controlCheck

log = logging.getLogger()


def sha256sum(filename):
    h = hashlib.sha256()
    b = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    return h.hexdigest()


def build(key, release, maturity):
    """ Build package

    Parameters
    ----------
    key: string
        pathname of signing private key
    release: int
        release number
    maturity: string
        maturity of the package
    """
    if not isPackage():
        log.error('current folder does not contain a WAPT package')
        return False

    if not controlCheck():
        log.error('WAPT/control invalid')
        return False

    log.debug('List files from current folder')
    list = []
    for root, dirs, files in os.walk('.'):
        for filename in files:
            if root == '.':
                if filename != '.git':
                    list.append(os.path.join(root, filename))
                    print('{}/{}'.format(root, filename))
            elif root == './WAPT':
                if filename != 'manifest.sha256':
                    list.append(os.path.join(root, filename))
                    print('{}/{}'.format(root, filename))
            elif root == './sources':
                if filename != '.gitignore':
                    list.append(os.path.join(root, filename))
                    print('{}/{}'.format(root, filename))
            elif root == './config':
                if filename != '.gitkeep':
                    list.append(os.path.join(root, filename))
                    print('{}/{}'.format(root, filename))

    log.debug('Creating WAPT/manifest.sha256')

    content = '['
    for file in list:
        hash256 = sha256sum(file)
        content += '["{}", "{}"],'.format(file[2:], hash256)
    content = content[:-1] + ']'

    with open(os.path.join('WAPT', 'manifest.sha256'), 'w') as output:
        output.write(content)

# printf "\n Creation of \"manifest.sha1\"\n"
# create_manifest_sha1 > WAPT/manifest.sha1
#   ## On enleve la virgule à l'avant derniere ligne.
# sed -i 'x; ${s/,//;p;x}; 1d' WAPT/manifest.sha1
# printf "\n File signature of manifest.sha1 with ${PRIVATE_KEY}\n"
# sign_manifest > WAPT/signature
# printf "\n Zipping folder as <wapt>.wapt\n"
# zip_to_wapt
# upload_package "${PACKAGE_package}_${PACKAGE_version}_${PACKAGE_architecture}"
# rm -f "${TEMP_FILE}"

    return True

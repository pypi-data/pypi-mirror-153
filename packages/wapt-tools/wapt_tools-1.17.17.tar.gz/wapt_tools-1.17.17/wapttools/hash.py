import hashlib
import logging
import os
import sys

log = logging.getLogger()


def sha256sum(filename):
    if not os.path.isfile(filename):
        log.critical('file "{file}" does not exists'.format(file=filename))
        sys.exit(1)

    h = hashlib.sha256()
    b = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        for n in iter(lambda: f.readinto(mv), 0):
            h.update(mv[:n])
    computed = h.hexdigest()

    return computed

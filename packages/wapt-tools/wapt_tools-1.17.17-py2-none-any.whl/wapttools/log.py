import logging
import os
import platform
try:
    import psutil
except ImportError:
    psutil = None
import tempfile


def logger(package, userspace=False):
    """
    TODO: need a documentation
    """
    logger = logging.getLogger(package)
    logger.setLevel(logging.DEBUG)

    if userspace:
        if psutil:
            current_user = psutil.Process().username().lower()
        else:
            current_user = os.getlogin()

        # Remove Windows domain if needed
        if '\\' in current_user:
            current_user = current_user.split('\\')[1]

        if platform.system() == 'Windows':
            logfile = os.path.join(os.environ['SYSTEMROOT'], 'WAPT.{}'.format(current_user), package + '.log')
        else:
            logfile = os.path.join(tempfile.gettempdir(), 'WAPT.{}'.format(current_user), package + '.log')
    else:
        if platform.system() == 'Windows':
            logfile = os.path.join(os.environ['SYSTEMROOT'], 'WAPT', package + '.log')
        else:
            logfile = os.path.join(tempfile.gettempdir(), 'WAPT', package + '.log')

    if not os.path.isdir(os.path.dirname(logfile)):
        os.makedirs(os.path.dirname(logfile))

    handler = logging.FileHandler(logfile)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(funcName)s: %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

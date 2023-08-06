import logging
import plumbum

log = logging.getLogger()


def upload(server, user, keyfile, filename):
    """ Upload *filename* to *user*@*server*:/var/www/wapt/ using SSH key *keyfile*
    """

    remote = plumbum.machines.SshMachine(server, user=user, keyfile=keyfile)
    fro = plumbum.local.path(filename)
    to = remote.path('/var/www/wapt/' + filename)
    plumbum.path.utils.copy(fro, to)
    to.chown('wapt', 'www-data')
    to.chmod(0644)

    remote['wapt-scanpackages /var/www/wapt/']

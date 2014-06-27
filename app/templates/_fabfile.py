import os
import re
from fabric.api import local, run, sudo, task, settings, env, cd
from fabric.tasks import Task


class IdentityTask(Task):
    """ Tasks which ultimately perform remote actions on the VM should
        inherit from this class in order to ensure the proper key filename,
        username, and host string are available. """

    def __init__(self, func, *args, **kwargs):
        super(IdentityTask, self).__init__(*args, **kwargs)
        self.func = func

    def run(self, *args, **kwargs):
        conf = {"host_string": "<%= hostIP %>",
                "key_filename": self.get_identity_file(),
                "user": "vagrant",
                "password": "vagrant"}
        with settings(**conf):
            return self.func(*args, **kwargs)

    def get_identity_file(self):
        ifile = None

        try:
            with open('.ifile', 'r') as f:
                ifile = f.read()
            print ("Cached SSH IdentityFile path: " + ifile)
            print ("(If incorrect, delete .ifile to rediscover)")

        except IOError:
            sshconf = local('vagrant ssh-config', capture=True)

            for line in sshconf.splitlines():
                if line.strip().startswith("IdentityFile"):
                    match = re.search(r'IdentityFile (.+)', line)
                    if match:
                        ifile = os.path.normpath(match.group(1).strip('"\''))
                        print ("Found SSH IdentityFile: " + ifile)
                        break

            if ifile is None:
                raise RuntimeError("Can't find IdentityFile in vagrant ssh-config")

            with open('.ifile', 'w') as f:
                f.write(ifile)

        return ifile


@task
def start(ip_port=''):
    """ Execute manage.py runserver """
    manage.run('runserver {0}'.format(ip_port))


@task
def rebuild():
    """ Destroy and re-create the VM. """
    local('vagrant destroy --force')
    with settings(warn_only=True):
        local('vagrant up')
        local('vagrant provision')
    local('vagrant reload --provision')


@task(task_class=IdentityTask)
def manage(c=""):
    run('cd <%= wwwDir %> && python manage.py {0}'.format(c))


@task(task_class=IdentityTask)
def migrate(app):
    """ Execute migration with --no-initial-data. """
    manage.run('migrate {0} --no-initial-data'.format(app))


@task(task_class=IdentityTask)
def migration(app):
    """ Create migration with --auto. """
    manage.run('schemamigration {0} --auto'.format(app))


@task(task_class=IdentityTask)
def initmigration(app):
    """ Create migration with --init. """
    manage.run('schemamigration {0} --initial'.format(app))


FIXTURE_PATH = '<%= wwwDir %>/fixtures/data.json'
EXCLUDE_APPS = ['cms_bsm', 'django_cron', 'south', 'thumbnail',
                'sessions', 'contenttypes', 'auth.Permission']


@task(task_class=IdentityTask)
def dumpdata():
    """ Export data and media to /fixtures. """
    run('cp -r /www/media <%= wwwDir %>/fixtures')
    run('rm -rf <%= wwwDir %>/fixtures/media/cache')
    manage.run('dumpdata -n {0} > {1}'.format(
        ' '.join(['-e ' + app for app in EXCLUDE_APPS]),
        FIXTURE_PATH))


@task(task_class=IdentityTask)
def loaddata():
    """ Import data and media from /fixtures """
    sudo('rm -rf /www/media')
    sudo('cp -r <%= wwwDir %>/fixtures/media /www')
    sudo('chown --recursive <%= projectUser %>:<%= projectGroup %> /www/media')
    sudo('chmod --recursive 774 /www/media')
    sudo('find /www/media -type f -exec chmod 664 {} +')
    manage.run('flush --noinput')
    manage.run('migrate --fake')
    manage.run('loaddata ' + FIXTURE_PATH)
    manage.run('thumbnail clear')


@task(task_class=IdentityTask)
def cleardata():
    """ Flush the database and load own fixtures. """
    sudo('rm -rf /www/media/*')
    manage.run('flush --noinput')


@task(task_class=IdentityTask)
def restart():
    """ Restart production stack. """
    sudo('service uwsgi restart')
    sudo('service nginx restart')


@task(task_class=IdentityTask)
def adlib(lib):
    """ Install latest version of library from pip 
        and add it to requirements.txt """
    # TODO: Sort requirements.txt alphabetically for extra pizzazz
    sudo('pip install {0}'.format(lib))
    sudo('pip freeze | grep -- {0} >> /vagrant/requirements.txt'.format(lib))

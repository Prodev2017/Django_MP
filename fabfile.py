import os
from contextlib import contextmanager
from fabric.api import cd, env, prefix, run, sudo, task


PROJECT_NAME = 'mapala'
PROJECT_ROOT = '/var/www/%s' % PROJECT_NAME
VENV_DIR = os.path.join(PROJECT_ROOT, '.env')
REPO = 'git@bitbucket.org:black_boxx/%s.git' % PROJECT_NAME

env.hosts = []


@task
def production():
    env.hosts = ['root@158.69.210.48']
    env.environment = 'production'


@contextmanager
def source_virtualenv():
    with prefix('source ' + os.path.join(VENV_DIR, 'bin/activate')):
        yield


def chown():
    """Sets proper permissions"""
    sudo('chown -R www-data:www-data %s' % PROJECT_ROOT)


def restart():
    sudo('systemctl restart nginx')
    sudo('systemctl restart mapala')


@task
def fetch(blockchain):
    with cd(PROJECT_ROOT):
        with source_virtualenv():
            run('./manage fetch %s' % blockchain)


@task
def deploy():
    """
    Deploys the latest tag to the production server
    """
    # sudo('chown -R %s:%s %s' % (env.user, env.user, PROJECT_ROOT))

    with cd(PROJECT_ROOT):
        run('git pull origin master --no-edit')
        with source_virtualenv():
            run('source .env/bin/activate && pip install -r requirements.txt')
            run('npm install')
            run('npm run build')
            run('./manage collectstatic --noinput')
            run('./manage migrate')

    #chown()
    restart()

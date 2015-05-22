import os

from fabric.api import *
from fabric.colors import green, red


def production():
    env.host_string = 'senexcycles.com'
    env.user = 'andermic'
    env.path = "/srv/www/senexcycles.com"

    if not os.path.exists('./fabfile.py'):
        print "Run in the directory containing fabfile.py"
        return

def staging():
    env.host_string = 'senexcycles.com'
    env.user = 'senex'
    env.path = "/srv/www/staging.senexcycles.com"

def deploy():
    print(red("Beginning Deployment:"))
    with cd("%s/senex" % path):
        with prefix('source %s/venv/bin/activate' % path):
            run("pwd")
            print(green("Pulling master from GitHub..."))
            run("git pull origin master")
            print(green("Installing requirements..."))
            run("pip install -r ../requirements/production.txt")
            print(green("Collecting static files..."))
            run("python manage.py collectstatic --noinput")
            # print(green("Syncing the database..."))
            # run("python manage.py syncdb")
            print(green("Migrating the database"))
            run("python manage.py migrate")
            print(green("Restarting the uwsgi process..."))
            sudo("restart gunicorn-senex")
            # run("touch %s/senex/senex/wsgi.py" % path)
    print(red("DONE..."))
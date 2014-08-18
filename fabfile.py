from fabric.api import *
from fabric.colors import green, red


def build_commit(warn_only=True):
    """Build a commit"""
    local_branch = prompt("checkout branch: ")
    rebase_branch = prompt("rebase branch: ")

    local('git checkout %s' % local_branch)
    local('git add -p')
    local('git add -u')

    message = prompt("commit message: ")

    local('git commit -m %s' % message)
    local('git checkout %s' % rebase_branch)
    local('git pull origin %s' % rebase_branch)
    local('git checkout %s' % local_branch)
    local('git rebase %s' % rebase_branch)
    local('git checkout %s' % rebase_branch)
    local('git merge %s' % local_branch)
    local('git push origin %s' % rebase_branch)
    local('git checkout %s' % local_branch)


def deploy():
    env.host_string = 'senexcycles.com'
    env.user = 'andermic'

    if not os.path.exists('./fabfile.py'):
        print "Run in the directory containing fabfile.py"
        return


def staging():
    path = "/srv/www/staging.senexcycles.com"

    print(red("Beginning Deployment:"))
    with cd("%s/senex" % path):
        run("pwd")
        print(green("Pulling develop from GitHub..."))
        run("git pull origin develop")
        print(green("Installing requirements..."))
        run("%s/venv/bin/pip install -r ../requirements/production.txt" % path)
        print(green("Collecting static files..."))
        run("%s/venv/bin/python manage.py collectstatic --noinput" % path)
        print(green("Syncing the database..."))
        run("%s/venv/bin/python manage.py syncdb" % path)
        print(green("Migrating the database"))
        run("%s/venv/bin/python manage.py migrate" % path)
        print(green("Restarting the uwsgi process..."))
        run("touch %s/senex/senex/wsgi.py" % path)
    print(red("DONE..."))


def production():
    path = "/srv/www/senexcycles.com/src/senex"
    process = "nginx"

    print(red("Beginning Deployment:"))
    with cd("%s/app" % path):
        run("pwd")
        print(green("Pulling master from GitHub..."))
        run("git pull origin master")
        print(green("Installing requirements..."))
        run(" %s/venv/bin/python && pip install -r requirements.txt" % path)
        print(green("Collecting static files..."))
        run("source %s/venv/bin/activate && python manage.py collectstatic --noinput" % path)
        print(green("Syncing the database..."))
        run("source %s/venv/bin/activate && python manage.py syncdb" % path)
        print(green("Migrating the database"))
        run("source %s/venv/bin/activate && python manage.py migrate" % path)
        print(green("Restarting the uwsgi process..."))
        run("sudo server %s restart" % process)
    print(red("DONE..."))


def prepare_deployment(branch_name):
    local('python manage.py test senex')
    local('git add -p && git commit')
    local('git checkout master && git merge ' + branch_name)

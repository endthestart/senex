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


def prepare_deployment(branch_name):
    local('python manage.py test senex')
    local('git add -p && git commit')
    local('git checkout master && git merge ' + branch_name)

def deploy():
    with lcd('/srv/www/senexcycles.com/senex/'):
        local('git pull origin')

        # With both
        local('python manage.py migrate senex')
        local('python manage.py test senex')
        local('service nginx restart')

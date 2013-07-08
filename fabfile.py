from fabric.api import lcd, local

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

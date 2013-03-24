from fabric.api import lcd, local

def prepare_deployment(branch_name):
    local('python manage.py test senex')
    local('git add -p && git commit')

def deploy():
    with lcd('/srv/www/senexcycles.com/'):
        local('git pull repo')

        # With both
        local('python manage.py migrate senex')
        local('python manage.py test senex')
        local('service nginx restart')

from __future__ import with_statement
from fabric.api import *
from fabric.colors import green, red

import os
HOME = os.getenv('HOME')

KEY_LOCATION = '/home/traveler/.keys/milesense.pem' 

@task
def prod():
    env.user = 'milesense'
    env.hosts = ['milesense.com']
    env.key_filename = [KEY_LOCATION,]

# sudo cp /opt/django-trunk/xlab_server/uwsgi/uwsgi.conf /etc/init/uwsgi.conf
# sudo start uwsgi
# sudo cp /opt/django-trunk/xlab_server/nginx/xlab.conf /etc/nginx/sites-available
# sudo ln -s /etc/nginx/sites-available/xlab.conf /etc/nginx/sites-enabled/xlab.conf

@task(alias='dd')
def deploy_django():
    local("./manage.py migrate")
    
    env_home = '/home/milesense/web-env'
    code_dir = "%s/modechoice" % env_home
    with cd(code_dir):
        run("svn update")
        run("%s/bin/python manage.py migrate" % env_home)
        run("touch /var/run/uwsgi-reload")

        # print status to make sure it restarted correctly
        run('supervisorctl status')

@task(alias='dj')
def deploy_javaserver():
    code_dir = '/home/milesense/server/framework'
    with cd(code_dir):
        run("svn update")
        run("ant dist")

        # restart the app
        run("supervisorctl restart javaserver")

        # print status to make sure it restarted correctly
        run('supervisorctl status')

#@task(alias='ddd')
#def download_db_dump():
#    # Add a time of day check?
#    print(green("Dumping database milesense on server..."))
#    run("PGPASSWORD=p2xilmt83sc2lx5zs3v4g6cf2 pg_dump --schema-only --no-acl --no-owner -h ec2-107-20-227-222.compute-1.amazonaws.com -U um3bnwrvow3e6b1 dc19h02p9rnsjhw | gzip -c > /tmp/milesense.dump.gz")
#    
#
#    print(green("Downloading dump file..."))
#    local("scp -i %s milesense@milesense.com:/tmp/milesense.dump.gz /tmp/" % KEY_LOCATION)
#
#    print(green("Deleting file on server..."))
#    run("rm -rf /tmp/milesense.dump.gz")

#@task(alias='id')
#def import_db():
#    download_db_dump()
#
#    print(green("Decompressing downloaded file..."))
#    local("gunzip /tmp/milesense.dump.gz")
#
#    drop = prompt(red('Drop local database milesense? (yes/no)'), default='yes')
#
#    if drop == 'yes':
#        local("dropdb --username=postgres milesense")
#        local("createdb --owner=postgres --username=postgres milesense")
#        local("psql -U postgres -d milesense -f /tmp/milesense.dump > /dev/null")
#        print(green("New database created and data imported..."))
#
#    print(green("Deleting dump file..."))
#    local("rm -rf /tmp/milesense.dump")
    
@task(alias='ddd')
def download_db_dump():
    # Add a time of day check?
    print(green("Dumping database milesense on server..."))
    run("PGPASSWORD=p2xilmt83sc2lx5zs3v4g6cf2 pg_dump --data-only --table=slicer_modedeterminationmodel --no-acl --no-owner -h ec2-107-20-227-222.compute-1.amazonaws.com -U um3bnwrvow3e6b1 dc19h02p9rnsjhw | gzip -c > /tmp/milesense.dump.gz")
    

    print(green("Downloading dump file..."))
    local("scp -i %s milesense@milesense.com:/tmp/milesense.dump.gz /tmp/" % KEY_LOCATION)

    print(green("Deleting file on server..."))
    run("rm -rf /tmp/milesense.dump.gz")

@task(alias='id')
def import_db():
    download_db_dump()

    print(green("Decompressing downloaded file..."))
    local("gunzip /tmp/milesense.dump.gz")

#    drop = prompt(red('Drop local database milesense? (yes/no)'), default='yes')
#
#    if drop == 'yes':
#        local("dropdb --username=postgres milesense")
#        local("createdb --owner=postgres --username=postgres milesense")
#        local("psql -U postgres -d milesense -f /tmp/milesense.dump > /dev/null")
#        print(green("New database created and data imported..."))
#
#    print(green("Deleting dump file..."))
#    local("rm -rf /tmp/milesense.dump")


@task(alias='twl')
def tail_web_logs():
    log_dir = '/home/milesense/logs/web-env'
    with cd(log_dir):
        run("tail -f modechoice.log")

@task(alias='tjl')
def tail_javaserver_logs():
    log_dir = '/home/milesense/logs/server'
    with cd(log_dir):
        run("tail -f milesense.log")

@task(alias='dnb')
def deploy_nightly():
    env_home = '/home/milesense/web-env'
    code_dir = "%s/modechoice/static/apps" % env_home
    with cd(code_dir):
        run("svn update")


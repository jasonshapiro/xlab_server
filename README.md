XLab Server
===========

The server-side component of the XLab-Mobile research project at UC Berkeley.

Installation
------------

The installation assumes a fresh EC2 instance running Ubuntu 12.04. If you are having sys-admin troubles, it is probably best to restart with a fresh instance.

Install required packages

	sudo apt-get install postgresql postgresql-server-dev-all python-virtualenv python2.7-dev git nginx acl

Make directories

	sudo mkdir /opt/django-trunk /opt/venvs /opt/log /opt/log/{django,uwsgi,nginx}

Make user ubuntu the owner of these directories

	sudo chown -R ubuntu:ubuntu /opt/*

Create empty log files with the touch command

	touch /opt/log/uwsgi/xlab.log /opt/log/nginx/xlab.log /opt/log/django/xlab.log

Clone git repo (read-only connection is fine)

	git clone git://github.com/dvizzini/xlab_server.git /opt/django-trunk/xlab_server

Create xlab_env

	virtualenv /opt/venvs/xlab_env

Activate this virtual environment

	source /opt/venvs/xlab_env/bin/activate

Install python packages

	pip install -r /opt/django-trunk/xlab_server/deployment/requirements.txt

Give the www-data user (which runs both uwsgi and nginx tasks) write access to the log files

	setfacl -Rm u:www-data:rx /opt/log

Start postgres command-line utility (psql)

	sudo su postgres -c psql template1

In psql, create 'xlab' user and give it password 'xlab'

	postgres=# CREATE USER xlab WITH PASSWORD 'xlab';

In psql, create xlab database 

	postgres=# CREATE DATABASE xlab;

In psql, grant privlidges to user xlab

	postgres=# GRANT ALL PRIVILEGES ON DATABASE xlab to xlab;

Exit psql

	postgres=# \q

Open pg_hba.conf to modify postgres permissions

	sudo vim /etc/postgresql/9.1/main/pg_hba.conf

Hit "insert" or the "i" key, and then add the following line to the top of the file

	local   xlab            xlab                                    md5

Hit "escape" and then save the file

	:w

Exit vim

	:q

Note, if the above does not work, you may need to set top permission to the following

	local   all            all                                    trust

Restart the postgres server

	sudo service postgresql restart

cd into django root

	cd /opt/django-trunk/xlab_server

Sync the database (make sure the virtualenv is still activated)

	./manage.py syncdb

When prompted, created a user called xlab. Give it password xlab and email xtech@haas.berkeley.edu

Copy nginx config file

	sudo cp /opt/django-trunk/xlab_server/deployment/xlab_nginx.conf /etc/nginx/sites-available/

Link this file in sites-available

	sudo ln -s /etc/nginx/sites-available/xlab_nginx.conf /etc/nginx/sites-enabled/xlab_nginx.conf

Copy the Upstart file to the appropriate folder

	sudo cp /opt/django-trunk/xlab_server/deployment/xlab_uwsgi.conf /etc/init/xlab_uwsgi.conf

# sudo start uwsgi

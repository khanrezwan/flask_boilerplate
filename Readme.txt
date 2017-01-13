Flask boilerplate
I will assume you are using virtualenv to install $ sudo apt-get install virtualenv
[1] $ cd path/to/flask_boilerplate (I will assume u r in this directory)
[2] $ virtualenv venv
[3] $ source path/to/venv/bin/activate
[5] $ pip install -r requirements.txt
    [a] If you use any new library just call $ pip install library_name (e.g. pip install sqlalchemy )
    [b] Every time you add new library run $ pip freeze > requirements.txt

[6] in Pycharm create new project > flask
    [a] Interpreter: show the path path/to/venv/bin/python
    [b] Location : path/to/flask_boilerplate . Pycharm will say that there is existing file and if you would like to use those instead. Click Yes / OK
[7] To run open manage.py
    [a] goto Run>Edit Configurations..
    [b] put 'runserver' (without quotes) in the Script Parameters text field and click apply
[8] Run manage.py

        1. login name: admin pass: admin
        2. login name: user pass: user

[9] Add all the routes/ views / controller in the app/main/views.py
[10] Add all the wtf form classes in app/main/forms.py
[11] Add all template files under app/templates . Also in Pycharm right-click on the folder Mark Directory As > Template Folder
    [a] Use copy_my_code_view.html as boilerplate of new template files
[12] Add all database models under app/models.py file
[13] I have used wind_data_parser.py in views.index method
[14] Finally run $ decativate to quit virtualenv

Migrations:
must be db admin for this
[1] under migrations folder create versions folder if not exists 
[2] manage.py init
[3] python manage.py db revision --autogenerate
[4] manage.py db upgrade head
[5] in a new machine drop the alembic_version table first. if db is not migrated

Deployment NGINX:
1 gunicorn --daemon --bind 127.0.0.1:8000 --timeout 600 manage:app
1 Might want to test the --daemon in gunicorn
2. follow this guide https://realpython.com/blog/python/kickstarting-flask-on-ubuntu-setup-and-deployment/
3. before pip install MySQL-python: sudo apt-get install libmysqlclient-dev
4. in /etc/nginx/nginx.conf add these lines under http
# set client body size to 50M #
client_max_body_size 50M;
# proxy read timeout
proxy_read_timeout 600s;
5. for nginx settings goto http://wiki.nginx.org/HttpProxyModule#proxy_read_timeout

Deployment Apache2:

[1] sudo apt-get install libapache2-mod-wsgi python-dev
[2] sudo a2enmod wsgi 
[3] cd /var/www
[4] sudo git clone https://rezwankhan@bitbucket.org/rezwankhan/cse_fest.git
[5] sudo apt-get install python-pip
[6] sudo pip install virtualenv
[7] cd /var/www/cse_fest
[8] sudo virtualenv venv
[9] source venv/bin/activate
[10] sudo pip install -r requirements.txt
[11] sudo chown www-data /var/www/cse_fest/data-dev.sqlite  ##use this to enable sqlite
[12] sudo chown www-data /var/www/cse_fest  ## use this to enable sqlite
[13] sudo nano /var/www/cse_fest/cse_fest.wsgi
 #add following lines 
#!/usr/bin/python

activate_this = '/var/www/cse_fest/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
import sys
import logging
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,'/var/www/cse_fest')

from manage import app as application


[14] sudo nano /etc/apache2/sites-available/cse_fest.conf   and add following lines for apache2-mpm-prefork

<VirtualHost *:80>
                WSGIScriptAlias / /var/www/cse_fest/cse_fest.wsgi
                <Directory /var/www/cse_fest/>
                        Order allow,deny
                        Allow from all
                </Directory>
                Alias /static /var/www/cse_fest/app/static
                <Directory /var/www/cse_fest/app/static/>
                        Order allow,deny
                        Allow from all
                </Directory>
                ErrorLog ${APACHE_LOG_DIR}/error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

[15] sudo a2ensite cse_fest
[16] sudo service apache2 restart 

apache2_mpm_ worker

[1] sudo apt-get purge apache2-mpm-prefork
[2] sudo apt-get purge apache2
[3] sudo apt-get install apache2-mpm-worker
[4] a2query -M
It may b prefork / event or worker
[5] sudo a2dismod mpm_event
[6] sudo a2dismod mpm_prefork
[7] sudo a2enmod mpm_worker



<VirtualHost *:80>
		WSGIDaemonProcess cse_fest user=www-data group=www-data threads=5                
		WSGIScriptAlias / /var/www/cse_fest/cse_fest.wsgi
                <Directory /var/www/cse_fest/>
			WSGIProcessGroup cse_fest
        		WSGIApplicationGroup %{GLOBAL}
                        Order allow,deny
                        Allow from all
                </Directory>
                Alias /static /var/www/cse_fest/app/static
                <Directory /var/www/cse_fest/app/static/>
                        Order allow,deny
                        Allow from all
                </Directory>
                ErrorLog ${APACHE_LOG_DIR}/error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>

This one also works
<VirtualHost *:80>
		ServerName csefest.local		
		WSGIDaemonProcess cse_fest user=www-data group=www-data threads=5                
		WSGIScriptAlias / /var/www/cse_fest/cse_fest.wsgi
                <Directory /var/www/cse_fest/>
			WSGIProcessGroup cse_fest
        		WSGIApplicationGroup %{GLOBAL}
                        Order allow,deny
                        Allow from all
                </Directory>
                Alias /static /var/www/cse_fest/app/static
                <Directory /var/www/cse_fest/app/static/>
                        Order allow,deny
                        Allow from all
                </Directory>
                ErrorLog ${APACHE_LOG_DIR}/error.log
                LogLevel warn
                CustomLog ${APACHE_LOG_DIR}/access.log combined
</VirtualHost>


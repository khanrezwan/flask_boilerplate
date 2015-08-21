Flask boilerplate
I will assume you are using virtualenv to install $ sudo apt-get install virtualenv
[1] $ cd path/to/wind_data_flask (I will assume u r in this directory)
[2] $ virtualenv venv
[3] $ source path/to/venv/bin/activate
[5] $ pip install -r requirements.txt
    [a] If you use any new library just call $ pip install library_name (e.g. pip install sqlalchemy )
    [b] Every time you add new library run $ pip freeze > requirements.txt

[6] in Pycharm create new project > flask
    [a] Interpreter: show the path path/to/venv/bin/python
    [b] Location : path/to/wind_data_flask. Pycharm will say that there is existing file and if you would like to use those
    instead. Click Yes / OK
[7] To run open manage.py
    [a] goto Run>Edit Configurations..
    [b] put 'runserver' (without quotes) in the Script Parameters text field and click apply
[8] Run manage.py

[9] Add all the routes/ views / controller in the app/main/views.py
[10] Add all the wtf form classes in app/main/forms.py
[11] Add all template files under app/templates . Also in Pycharm right-click on the folder Mark Directory As > Template Folder
    [a] Use copy_my_code_view.html as boilerplate of new template files
[12] Add all database models under app/models.py file
[13] I have used wind_data_parser.py in views.index method
[14] Finally run $ decativate to quit virtualenv

Deployment:
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

1. login name: admin pass: admin
2. login name: user pass: user
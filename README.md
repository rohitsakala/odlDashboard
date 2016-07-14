# odlDashboard
Under Development

#Installation
- sudo apt-get install git
- sudo apt-get install python-pip
- git clone https://github.com/rohitsakala/odlDashboard
- sudo pip install requests
- sudo pip install virtualenvwrapper
- export WORKON_HOME=~/Envs
- source /usr/local/bin/virtualenvwrapper.sh
- mkvirtualenv odl
- workon odl
- sudo apt-get install libpq-dev python-dev
- sudo apt-get install postgresql postgresql-contrib
- cd odlDashboard
- pip install -r requirements.txt
- sudo su - postgres
- createdb dashboard
- createuser -P odluser
- Put password as odl
- GRANT ALL PRIVILEGES ON dashboard mydb TO odluser;
- cd dashboard/dashboard
- open settings.py and put the ip address in ALLOWED_HOSTS = []
- sudo apt-get install screen
- screen
- cd ..
- python manage.py runserver 0.0.0.0:8000
- 

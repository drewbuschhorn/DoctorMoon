#!/bin/bash

#sudo easy_install virtualenv
#virtualenv my_doctormoon --no-site-packages
#cd my_doctormoon
#source bin/activate
#http://mitchfournier.com/2010/06/25/getting-started-with-virtualenv-isolated-python-environments/
#git clone git@github.com:drewbuschhorn/DoctorMoon.git
#cd DoctorMoon

#### Easy dependencies
../bin/easy_install django psycopg2 mimeparse python_digest #Doctor Moon ( django site ) dependencies
../bin/easy_install twisted psycopg2
../bin/easy_install sunburnt httplib2 lxml #Doctor Moon ( twisted site ) dependencies 
####

#### Challenging dependencies
../bin/easy_install egenix-mx-base
##apt-get install libgraphviz-dev
../bin/easy_install pygraphviz 
../bin/easy_install numpy 
../bin/easy_install matplotlib #Doctor Moon ( twisted site ) dependencies
####


#### Setup Postgres Django database 
# ( database name = drmoon, username="postgres", password="django13" )

#cd drmoon_project/
#../../bin/python manage.py syncdb
# provide superuser

#http://localhost:8000/accounts/register
# provide test user

#http://localhost:8000/accounts/login
#http://localhost:8000/networkgraphs/form
# doi:[10.1371/journal.pmed.0020124]

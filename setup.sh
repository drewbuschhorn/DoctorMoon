#!/bin/bash

#sudo easy_install virtualenv
#virtualenv my_doctormoon --no-site-packages
#cd my_doctormoon
#source bin/activate
#http://mitchfournier.com/2010/06/25/getting-started-with-virtualenv-isolated-python-environments/
#git clone git@github.com:drewbuschhorn/DoctorMoon.git

#### Easy dependencies
../bin/easy_install django psycopg2 #Doctor Moon ( django site ) dependencies
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

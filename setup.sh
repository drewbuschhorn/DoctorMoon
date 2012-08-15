#!/bin/bash
sudo apt-get install python-dev libfreetype6-dev libpng-dev libxslt-dev libxml2-dev libpq-dev postgresql python-pip python-dev build-essential libgraphviz-dev screen
sudo pip install --upgrade pip 
sudo pip install --upgrade virtualenv 

#sudo easy_install virtualenv
#virtualenv my_doctormoon --no-site-packages
#cd my_doctormoon
#source bin/activate
#http://mitchfournier.com/2010/06/25/getting-started-with-virtualenv-isolated-python-environments/
#git clone git@github.com:drewbuschhorn/DoctorMoon.git
#cd DoctorMoon

pip install numpy
pip install -r requirements.txt
####


#### Setup Postgres Django database 
# ( database name = drmoon, username="postgres", password="django13" )
echo "Creating the postgres database. May take a few seconds"
sudo -u postgres createdb -E UTF-8 drmoon

echo "Setting the postgress user password.  Recommend django13 for dev password, but this is highly insecure.  Will also reset any other application using postfres on this machine."
echo "Proceed? [Y/N]"
read a
if [[ $a == "Y" || $a == "y" || $a = "" ]]; then
	sudo -u postgres psql <<< "\password postgres"
fi


cd drmoon_project/
python manage.py syncdb
# provide superuser

#http://localhost:8000/accounts/register
# provide test user

#http://localhost:8000/accounts/login
#http://localhost:8000/networkgraphs/form
# doi:[10.1371/journal.pmed.0020124]

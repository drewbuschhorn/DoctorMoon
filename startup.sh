#!/bin/bash

type -P screen &> /dev/null
if [ $? -ne 0 ]; then
  echo "command 'screen' not found. Please install screen to run this demo."
  exit
fi

screen -d -m -S drmoon_django python drmoon_project/manage.py runserver
screen -d -m -S drmoon_twisted ./twisted_startup.sh
screen -ls

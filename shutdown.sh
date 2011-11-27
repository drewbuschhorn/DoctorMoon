#!/bin/bash

type -P screen &> /dev/null
if [ $? -ne 0 ]; then
  echo "command 'screen' not found. Please install screen to run this demo."
  exit
fi

screen -wipe > /dev/null

screen -S drmoon_django -X quit > /dev/null
if [ $? -eq 0 ]; then
  echo "Shutdown drmoon_django screen session"
fi

screen -S drmoon_twisted -X quit > /dev/null
if [ $? -eq 0 ]; then
  echo "Shutdown drmoon_twisted screen session"
fi

echo "Remaing live screen sessions:"
screen -ls

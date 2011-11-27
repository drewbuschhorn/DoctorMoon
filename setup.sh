#!/bin/bash

####
../bin/easy_install django psycopg2 #Doctor Moon ( django site ) dependencies
../bin/easy_install twisted psycopg2
../bin/easy_install sunburnt httplib2 lxml #Doctor Moon ( twisted site ) dependencies 

## Challenging dependencies
../bin/easy_install egenix-mx-base
##apt-get install libgraphviz-dev
../bin/easy_install pygraphviz 
../bin/easy_install numpy 
../bin/easy_install matplotlib #Doctor Moon ( twisted site ) dependencies

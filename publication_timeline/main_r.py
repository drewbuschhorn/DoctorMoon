# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 19:57:39 2018

@author: drewb
"""

import networkx as nx
import uuid

from twisted.internet import reactor, threads
from twisted.internet.task import deferLater
from twisted.web.server import Site,NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.python.log import err
from twisted.enterprise import adbapi

from Grapher_r import Grapher_r

from S2SearchStrategy import S2SearchStrategy
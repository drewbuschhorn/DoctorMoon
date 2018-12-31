#!/usr/bin/env python
# encoding: utf-8
"""
d3_js.py

Description: Read and write files in the D3.js JSON file format.  This
can be used to generate interactive Java Script embeds from NetworkX
graph objects.

These functions will read and write the D3.js JavaScript Object Notation (JSON)
format for a graph object. There is also a function to write write HTML and Javascript 
files need to render force-directed layout of graph object in a browser.  The default
redering options are based on the force-directed example by Mike Bostock at
(http://mbostock.github.com/d3/ex/force.html).

Created by Drew Conway (drew.conway@nyu.edu) on 2011-07-13 
# Copyright (c) 2011, under the Simplified BSD License.  
# For more information on FreeBSD see: http://www.opensource.org/licenses/bsd-license.php
# All rights reserved.
"""

__author__="""Drew Conway (drew.conway@nyu.edu)"""

__all__=['d3_json']

import os
import sys
from shutil import copyfile
from networkx.utils import _get_fh, make_str
import networkx as nx
import json
import re

def _doc_to_json(searcher,node_labels,node):
	index = node[1][0]
	node = node[1][1]
	
	return 	{	
			'name': "%s::%s::%s::%d" %(node.path_index,node.publication_date,node.id,node.hasMatchingAuthorsName(searcher.core_authors())), 
			'group' : node.path_index,
			'doi': node.id,
			'publication_date': node.publication_date,
			'path_index': node.path_index,
            'authors': node.author_names,
			'is_original_author': 'true' if node.hasMatchingAuthorsName(searcher.core_authors()) else 'false',
			'title': node.title,
			'index': index
			}

def d3_json(G, group=None, searcher = None):
	"""Converts a NetworkX Graph to a properly D3.js JSON formatted dictionary
	
	Parameters
	----------
	G : graph
		a NetworkX graph
	group : string, optional
		The name 'group' key for each node in the graph. This is used to 
		assign nodes to exclusive partitions, and for node coloring if visualizing.
		
	Examples
	--------
	>>> from networkx.readwrite import d3_js
	>>> G = nx.path_graph(4)
	>>> G.add_nodes_from(map(lambda i: (i, {'group': i}), G.nodes()))
	>>> d3_js.d3_json(G)
	{'links': [{'source': 0, 'target': 1, 'value': 1},
	  {'source': 1, 'target': 2, 'value': 1},
	  {'source': 2, 'target': 3, 'value': 1}],
	 'nodes': [{'group': 0, 'nodeName': 0},
	  {'group': 1, 'nodeName': 1},
	  {'group': 2, 'nodeName': 2},
	  {'group': 3, 'nodeName': 3}]}
	"""
	
	first_label = 0
	N=G.number_of_nodes()+first_label
	nlist=G.nodes()
	nlist = sorted(nlist, key = lambda k: k.publication_date)
	mapping=dict(zip(nlist,range(first_label,len(nlist))))
	H=nx.relabel_nodes(G,mapping)
	H.name="("+G.name+")_with_int_labels"
	H.node_labels=mapping
	
	#ints_graph = nx.convert_node_labels_to_integers(G, discard_old_labels=False)
	ints_graph = H
	graph_nodes = ints_graph.nodes(data=True)
	graph_edges = ints_graph.edges(data=True)
	
	node_labels = [(b,a) for (a,b) in ints_graph.node_labels.items()]
	#node_labels.sort()
	
	# Build up node dictionary in JSON format
	if group is None:
		graph_json = 	{'nodes': 
							map(lambda n : _doc_to_json(searcher,node_labels,n), enumerate(node_labels)
							)
						}
	else:
		try:
			graph_json = {'nodes' : map(lambda i,n: {
                    'name': str(node_labels[n][1]), 
                    'group' : graph_nodes[n][1][group]}, 
                    enumerate(range(len(node_labels))))}
		except KeyError:
			raise nx.NetworkXError("The graph had no node attribute for '"+group+"'")
		
	# Build up edge dictionary in JSON format
	json_edges = list()
	for j, k, w in graph_edges:
		e = {'source' : j, 'target' : k}
		if any(map(lambda k: k=='weight', w.keys())):
			e['value'] = w['weight']
		else:
			e['value'] = 1
		
		e['index'] = len(json_edges)
		json_edges.append(e)
	
	graph_json['links'] = json_edges
	return graph_json

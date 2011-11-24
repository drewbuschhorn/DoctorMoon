'''
Created on Jul 6, 2011

@author: dbuschho
'''
import networkx as nx

from Grapher import Grapher
from PlosSearchStrategy import PlosSearchStrategy

if __name__ == '__main__':
    
    import logging
    logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)
    
    searcher = PlosSearchStrategy('10.1371/journal.pmed.0020124')
    searcher.subnodelookup()
    
    grapher = Grapher()
    
    newg = nx.Graph()
    for path in searcher.useful_paths:
        newg.add_path(path)
        grapher.paths.append(path)
    
    
    grapher.graph = newg
    grapher.render(searcher,searcher.core_node)
    
''' 
Created on Jul 6, 2011

@author: dbuschho
Y'''

START_PAPER = u"7ba400225356a7d389f04e13e2d2506f40774fc8" #u"dba56b1d8b91142cc772b04655797d0d0f2fc532"
CORPUS_PATH = u"D:\\corpus\\"
CORPUS_SQLLITE_PATH = u"D:\\corpus\\processed_data\\id_positions.sqlite3"
TEMP_NODE_STORE = u"D:\\corpus\\processed_data\\tmp.json"

import sys, time, os
sys.path.append('../libs/networkx')
import networkx
from networkx.readwrite import d3_js
import uuid
import json as jsn

from twisted.internet import reactor, threads
from twisted.internet.task import deferLater
from twisted.web.server import Site,NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.internet import reactor, threads, defer
from twisted.python.log import err


from Grapher import Grapher
from S2SearchStrategy import S2SearchStrategy
from timeline_generator.generators.S2Generator import S2Generator

if __name__ == '__main__':
    class Maintainer(object):
        def __init__(self):
            self.searcher = None
            self.uuid = uuid.uuid4()
        
        def start(self):#,params):
            self.searcher = S2SearchStrategy(START_PAPER, self)
            
            start = False
            if os.path.isfile(TEMP_NODE_STORE):
                print (u"Temp node store " + TEMP_NODE_STORE + u" exists.")
                print (u"Do you want to purge it and start the search over again? [Y/N]")
                removeFile = None
                while removeFile is not 'Y' and removeFile is not 'N':
                    removeFile = input() 
                if removeFile is 'Y':
                    os.remove(TEMP_NODE_STORE)
                    start = True
            else:
                start = True
            
            if start:
                self.searcher.start()
            else:
                self.grapher()
        
        def stop(self):
            print ("ending: %s" %(self.searcher._opennodes,))
            self.grapher()
        
        @defer.inlineCallbacks 
        # subset = (start, end)
        def grapher(self, subset=None):
                #First grab the data and cut it down to size
                with open(TEMP_NODE_STORE, "r") as f:
                    data = jsn.load(f)
                    if subset is not None:
                        data_subset = data[subset[0], subset[1]]
                    else:
                        data_subset = data
                
                generator = S2Generator(CORPUS_PATH,
                                     CORPUS_SQLLITE_PATH)
                                    
                real_networks = []
                for network in data_subset: 
                    real_network = []
                    for customId in network:
                        node = yield generator.populateNodeFromCustomId(customId)
                        node.path_index = len(real_networks)
                        real_network.append(node)
                    real_networks.append(real_network)
                
                grapher = Grapher()
                newg = networkx.Graph()
                
                all_nodes = set()
                for i in real_networks:
                    for j in i:
                        all_nodes = all_nodes.union(set([j.id]))
                
                node_to_vocab = dict()
                vocab_to_node = dict()
                for i in all_nodes:
                    node_to_vocab[i] = len(node_to_vocab)
                    vocab_to_node[len(vocab_to_node)] = i
                
                for path in real_networks:
                    newg.add_path(path)
                    grapher.paths.append(path)
                
                grapher.graph = newg
                mikedewar = newg
                
                graph_json = d3_js.d3_json(mikedewar, group=None, searcher=self.searcher)
                
                if self.searcher.core_node is None:
                    self.searcher.core_node = yield generator.populateNodeFromCustomId(self.searcher.core_node_id)
                if graph_json['links'] is None or graph_json['nodes'] is None:
                    print ("Mapping failed")
                    exit()
                
                output_name = self.searcher.core_node_id + "_" +  str(int(time.time())) + ".json"
                with open('data/' + output_name, 'w+') as outputfile:
                    outputfile.write("var timelineData = ") # Just to make life easier for everyone
                    jsn.dump({'nodes':list(graph_json['nodes']), 'links':graph_json['links']}, outputfile, indent=2)
                    print ("Mapping successful. Access mapping at URL below:")
                    visualization_path = "file:///%s#%s"
                    print (visualization_path % (os.path.abspath("../../example_map.html").replace("\\","/"), output_name))
                    exit()
    
    m = Maintainer()
    m.start()
    reactor.run()

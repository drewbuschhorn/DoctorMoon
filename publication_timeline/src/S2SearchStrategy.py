'''
Created on Jul 31, 2018

@author: dbuschho
'''
import pickle
import json

from timeline_generator.generators.S2Generator import S2Generator
from twisted.internet import defer, reactor

class S2SearchStrategy(object):

    def __init__(self, core_node_id, maintainer):
        
        self.maintainer = maintainer
        self.useful_paths = []
        self.core_node = None
        self._core_authors = None
        self._opennodes = 0        
        
        self._cache = {}
        
        self.generator = S2Generator(u'D:\corpus\downloads', 
                                     u'D:\corpus\processed_data\id_positions.sqlite3')
        
        print ('started')
        #self.core_node = self.generator.populateNodeFromCustomId(core_node_id)            
        self.core_node_id = core_node_id
        print ('finished')
    
    def _handlePopulateNodeFromCustomIdTimeout(self,customId):
        pass
    
    @defer.inlineCallbacks
    def start(self):
        try:
            d = self.subnodelookup()
            d.addErrback(self._stop)
            yield d 
        except Exception as inst:
            print (inst)
            print ("start failure")
            return
        
    def _stop(self,e):
        print (e.getErrorMessage())
        print ("stopping reactor")
        reactor.stop()
        

    def _handleSearchTimeout(self,e):
        print ("subnode failed")
        print (e.getErrorMessage())
        raise
        #raise NameError("Search timed out, %s" %(e.getErrorMessage,))
        
    def core_authors(self):    
        if(self._core_authors is None):
            #Dedupe core authors
            self._core_authors = list(set([self.core_node.author[-1],self.core_node.author[0]]))
        
        return self._core_authors

    @defer.inlineCallbacks
    def subnodelookup(self, id = None, level = 0, parent = []):
        #print id
        if(level==0):
            parent = []
            
        self._opennodes += 1
        
        if(id is None):
            id = self.core_node_id
        
        node = None
        try:
            node = yield self.generator.populateNodeFromCustomId(id)
            
            if(self.core_node is None):
                self.core_node = node
                
        except Exception as e:
            print (e)   
            raise NameError("Couldn't successfully populateNodeFromCustomId: %s" % (node,))
                    
        parent.append(node)
        
        try:
            d =  self.generator.findCitingNodes(node)
            citingworks = yield d
        except Exception as inst:
            print (inst)
            print ("Failure in findCitingNodes")
            raise NameError("Couldn't successfully findCitingNodes: %s" % (node,))    
            
        count = 0;    
        for paper in citingworks:
            try:
                count = count +1
                #if(count > 100):
                #    break
                # For each author name in paper x, find any that match the 
                # authorname we're keyed on and return that paper
                #if(paper.id == '3fdb444448a3e3f28897409a3df20a5087026a07'):
                #    paper.authors.append(self.core_authors())
                
                if(paper.hasMatchingAuthorsName(self.core_authors())):
                    parent.append(paper)
                    for item in parent:
                        if hasattr(item,'path_index') is False:
                            item.path_index = len(self.useful_paths)+1
                    self.useful_paths.append(parent[:])
                    #if (any(len(path) > 5 for path in self.useful_paths)):
                    #    break
                    #print (parent)
                    parent.pop()
                else:
                    if(level<=4 and (node.id != paper.id)):
                        try:
                            d = self.subnodelookup(paper.id,level+1,parent[:])
                            d.addErrback(self._handleSearchTimeout)
                        except Exception as inst:
                            print (inst, "ending from subnodelookupfailure")
                            raise NameError("Subnode failure")
            except Exception as inst:
                print (inst)
                print ("Failure in findCitingNode2s")
                self._opennodes -= 1
                raise NameError("Couldn't successfully findCitingNodes2: %s" % (node,))  
                
                        
        
        self._opennodes -= 1
        #print ("ending subnodes: %s" %(self._opennodes,))
        if(self._opennodes is 0):
            print ("search complete: %s" %(self.useful_paths,))
            with open("D:\\corpus\\paths.json", "w", encoding="utf8") as f:
                f.write("%s" %(self.useful_paths,))
            self.maintainer.stop()
            reactor.stop()
'''
Created on Jul 31, 2011

@author: dbuschho
'''

from timeline_generator.generators.PlosGenerator import PlosGenerator

class PlosSearchStrategy(object):
    def __init__(self, core_node_id):
        self.generator = PlosGenerator(u'AVWZBXMiftO65ug')
        self.core_node = self.generator.populateNodeFromCustomId(core_node_id)
        self.useful_paths = []
        self._core_authors = None
        
    def core_authors(self):    
        if(self._core_authors is None):
            #Dedupe core authors
            self._core_authors = list(set([self.core_node.author[-1],self.core_node.author[0]]))
        
        return self._core_authors
    
    def subnodelookup(self,id=None,level=0,parent=[]):
        if(id is None):
            id = self.core_node.id
            
        node = self.generator.populateNodeFromCustomId(id)
        parent.append(node)
        citingworks = self.generator.findCitingNodes(node)
        for paper in citingworks:
            # For each author name in paper x, find any that match the 
            # authorname we're keyed on and return that paper
            if(paper.hasMatchingAuthorsName(self.core_authors())):
                parent.append(paper)
                for item in parent:
                    if hasattr(item,'path_index') is False:
                        item.path_index = len(self.useful_paths)+1
                self.useful_paths.append(parent[:])
                parent.pop()
            else:
                if(level<=4 and (node.id != paper.id)):
                    self.subnodelookup(paper.id,level+1,parent[:])

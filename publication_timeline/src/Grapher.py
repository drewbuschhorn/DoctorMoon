'''
Created on Jul 31, 2011

@author: dbuschho
'''

try:
    import matplotlib.pyplot as plt
    import networkx as nx
except:
    raise Exception('Grapher imports not loaded')

class Grapher(object):
    def __init__(self):        
        self.graph = nx.Graph()
        self.paths = []

    def determinePositions(self,searcher):
        pos = {}
        for path in self.paths:
            for item in path:
                if item.hasMatchingAuthorsName(searcher.core_authors()):
                    y = 0
                else:
                    y = item.path_index
                x = float(item.publication_date) # Let's find a sane position range
                x =  (x - 700000)/10000
                pos.update({item:[x,y]})
        return pos

    def addToGraph(self,node,all=True):

        if(node in self.graph):                      
            pass
        else:                   
            self.graph.add_node(node,data=node)
            
        
        for childnode in node.childNodes:
            
            if(self.graph.has_node(childnode)):
                pass
            else:
                self.addToGraph(childnode)            
            self.graph.add_edge(node,childnode)

        for p in node.parentNodes:          
            
            if(self.graph.has_node(p)):
                pass
            else:
                self.addToGraph(p)            
            self.graph.add_edge(node,p)           
                
    
    
    def findColor(self,i,core_authors):
        if i.hasMatchingAuthorsName(core_authors):
            return "red"
        else:
            return "blue"
    
    def render(self,searcher,center=None):
        center_pos = None
        
        if(center):
            center_pos = {center:(0,0)}
            center = [center]
        
        colors = [self.findColor(i,searcher.core_authors()) for i in self.graph]
        #pos=nx.spring_layout(self.graph,pos=self.determinePositions(),fixed=None,iterations=4,scale=10)
        pos=self.determinePositions(searcher)
        
        nx.draw(    G=self.graph,
                    pos=pos,
                    node_color=colors,
                    edge_color='#000000',
                    width=0.1,
                    with_labels=True,
                    font_size=10,
                    node_size=100
                    )
        plt.savefig("edge_colormap.png") # save as png
        
        plt.show() # display
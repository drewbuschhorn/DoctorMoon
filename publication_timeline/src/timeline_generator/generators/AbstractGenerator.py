'''
Created on Jul 6, 2011

@author: dbuschho
'''

class AbstractGenerator(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        #Identify nodes which have only skeleton data
        self._isComplete = False
        #Identify nodes which reference records that can't be found
        self._isFound = False
              
        raise NotImplementedError
       
    def getNodeCitedWorksArray(self): 
        raise NotImplementedError
    
    def getNodeCitingWorksArray(self):
        raise NotImplementedError
    
    def getNodeAuthorsArray(self):
        raise NotImplementedError
    
    def getNodePrimaryAuthor(self):
        raise NotImplementedError
    
    def getNodeUUID(self):
        raise NotImplementedError
    
    def getNodeDate(self):
        raise NotImplementedError
    
    def getNodeCustomId(self):
        raise NotImplementedError
 
    def isReady(self):
        return self._isComplete
    
    def isFound(self):
        return self._isFound
    
    def populateNodeFromCustomId(self,customId):
        raise NotImplementedError
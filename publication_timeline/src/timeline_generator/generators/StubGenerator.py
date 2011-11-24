'''
Created on Jul 6, 2011

@author: dbuschho
'''
import uuid,datetime,time
import AbstractGenerator

class StubGenerator(AbstractGenerator.AbstractGenerator):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.uuid = uuid.uuid4(); 
        self.citedWorks = [uuid.uuid4() in range(5)]
        self.citingWorks = [uuid.uuid4() in range(3)]
        self.authors = ["smith","baker","candler"]
        self.primaryauthor = ["candler"]
        self.datestamp = time.mktime(datetime.datetime(2002,1,1,1,1,1).timetuple())
       
    def getNodeCitedWorksArray(self):
        return self.citedWorks
    
    def getNodeCitingWorksArray(self):
        return self.citingWorks
    
    def getNodeAuthorsArray(self):
        return self.authors
    
    def getNodePrimaryAuthor(self):
        return self.primaryAuthor
    
    def getNodeUUID(self):
        return self.uuid
    
    def getNodeDate(self):
        return self.datestamp
    
    def getNodeCustomId(self):
        return self.getNodeUUID
    
    def populateNodeFromCustomId(self,customId):
        return True
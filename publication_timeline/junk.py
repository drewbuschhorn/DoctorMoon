'''
Created on Jul 6, 2018

@author: dbuschho
'''
import uuid, datetime, time, json
import AbstractGenerator

from twisted.internet import reactor, threads, defer
from twisted.enterprise import adbapi

class S2Generator(AbstractGenerator.AbstractGenerator):
    '''
    classdocs
    '''
    def __init__(self, corpus_path, position_database_path):
        '''
        Constructor
        '''
        self.cursor = adbapi.ConnectionPool("sqlite3", position_database_path, check_same_thread=False)        
        self.uuid = uuid.uuid4();
        self.results = dict()
       
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
    
    
    @defer.inlineCallbacks
    def populateNodeFromCustomId(self,customId):
        if(customId in self.results):
            defer.returnValue(self.results[customId])
        
        deferred = self.cursor.runQuery("SELECT * FROM positions WHERE uuid = ?", (customId,))
 
        def onResult(data):
            #data[0][0] # first row, first column
            print (data)
            with open(data[0][3]) as f:
                f.seek(data[0][4])
                json_data = json.loads(f.readline())
                self.citedWorks = json_data['outCitations']
                self.citingWorks = json_data['inCitations']
                self.authors = []
                for authors in json_data['authors']:
                    self.authors.append(authors['ids'])
                self.primaryAuthor = self.authors[-1]
                self.datestamp = datetime.date(json_data['year'],1,1)
                self.datestamp = time.mktime(self.datestamp.timetuple())
                self.getNodeUUID = json_data['id']
                
        deferred.addCallback(onResult)
        result = yield deferred
        defer.returnValue(result)
        
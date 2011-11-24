'''
Created on Jul 6, 2011

@author: dbuschho
'''

import AbstractGenerator

import sunburnt,httplib2

#####Plos<>Sunburnt Helper Class
class PlosInterface(sunburnt.SolrInterface):
    def __init__(self,api_key):
        plos_url = "http://api.plos.org/search"
        plos_schema = open('timeline_generator/generators/plos_schema.xml')#localfile handle open('../plos_schema.xml') from
                                                #http://api.plos.org/search-examples/schema.xml
        #Python base class magic ... make this class a SolrInterface like object
        #note that schemadoc if requested by url will be loaded                                      
        super(PlosInterface, self).__init__(url=plos_url,schemadoc=plos_schema)
        #Replace default connection with one that 
        self.conn = PlosInterface.PlosConnection(url=plos_url,api_key=api_key,cacheLength=31536000)    
    #Create specific PlosConnection subclass of SolrConnection
    #to force addition of API_KEY query param to all queries
    class PlosConnection(sunburnt.sunburnt.SolrConnection):
        api_key = None
        def __init__(self, url, api_key,cacheLength=0):
            self.api_key = api_key
            h = PlosInterface.PlosCachingHTTP(cache="/var/tmp/plos_cache")
            h._cacheLength = cacheLength
            super(PlosInterface.PlosConnection, self).__init__(url=url,http_connection=h)
        def select(self, params):
            params.append((u'api_key',self.api_key))
            return sunburnt.sunburnt.SolrConnection.select(self,params)
    
    ##Force caching to be polite
    class PlosCachingHTTP(httplib2.Http):
        _cacheLength = 0;
        
        def request(self,uri, method="GET", body=None, headers={}, redirections=httplib2.DEFAULT_MAX_REDIRECTS, connection_type=None):
            if 'cache-control' not in headers:
                headers['cache-control']='max-age='+str(self._cacheLength)
            return super(PlosInterface.PlosCachingHTTP,self).request(uri,method,body,headers,redirections,connection_type)
            
#####end Plos<>Sunburnt Helper Class


import uuid,datetime,time,string

class PlosGenerator(AbstractGenerator.AbstractGenerator):

    '''
    classdocs
    '''
    
    fields=['author','title','reference','id','publication_date']
    
    def __init__(self,api_key):
        '''
        Constructor
        '''
        self.api_key = api_key
        self.search = PlosInterface(api_key)
        self.uuid = uuid.uuid4()
        self.results = {}
                
    def _PlosDocumentConstructor(self,**keywords):
        return PlosDocument(owningGenerator=self,**keywords)
    
    def _PlosDocumentHash(self,_plosDoc):
        return {string.strip(_plosDoc.id):_plosDoc}           
                
    def populateNodeFromCustomId(self,customId):
        if(customId in self.results):
            return self.results[customId]
        
        response = self.search.query(id=customId).field_limit(self.fields).execute(constructor=self._PlosDocumentConstructor)
        if len(response.result.docs) != 1:
            raise NameError('PlosSearch results on customId returned: %s results' % len(response.result.docs))
        
        result = response.result.docs[0]
        if result.id not in self.results:
            result_hash = self._PlosDocumentHash(result)
            self.results.update(result_hash) 
        
        result = self.results.get(result.id)
               
        return result

    def findCitingNodes(self,_plosDoc):
        authornames = self.search.Q()
        for fullname in _plosDoc.getNodeAuthorsArray():
            authornames = authornames | self.search.Q(reference=string.split(fullname,' ')[-1]) 
        
        query = self.search.query(self.search.Q(reference=_plosDoc.getNodeTitle()) & authornames)
        response = query.field_limit(self.fields).execute(constructor=self._PlosDocumentConstructor)
        
        results = []
        for result in response.result.docs:
            if result.id not in self.results:
                self.results.update(self._PlosDocumentHash(result))
            else:                
                result = self.results.get(result.id)
 
            result.addParentNode(_plosDoc)
            _plosDoc.addChildNode(result)
            results.append(result)
    
        return results
        

            
class PlosDocument(object):  #Maybe switch to proxy object and duck-type
    def __repr__(self):
        return self.id    
    def __str__(self):
        return self.id
    
    def __init__ (self,owningGenerator=None,**keywords):
        for key in keywords:
            self.__setattr__(key, keywords[key])
        self.owner = owningGenerator # Generator used to create this node
        self.uuid = uuid.uuid4()
        self.parentNodes = []
        self.childNodes = []

    def getNodeCitedWorksArray(self): 
        if(self.reference is None):
            raise NameError('references not set')
        
        return self.reference
    
    def getNodeTitle(self):
        if(self.title is None):
            raise NameError('title not set')
        return self.title        
    
    def getNodeCitingWorksArray(self):        
        return self.owner.findCitingNodes(self)
    
    def getNodeAuthorsArray(self):
        if(self.author is None):
            raise NameError('author array not set')
        
        return self.author
            
    def getNodePrimaryAuthor(self):
        if(self.author is None):
            raise NameError('author array (primary author) not set')
        
        name = self.author[-1]
        name = string.split(name,' ')[-1]
        
        return name
                
    def getNodeUUID(self):
        if(self.uuid is None):
            raise NameError('UUID not set')
        
        return self.uuid
                
    def getNodeDate(self):
        if(self.publication_date is None):
            raise NameError('publication_date not set')
        
        return self.publication_date
                
    def getNodeCustomId(self):
        if(self.id is None):
            raise NameError('id not set')
        
        return self.id
    
    def addParentNode(self,newNode):
        if (newNode is None) or (newNode.id == self.id):
            return
        
        found = False
        for parentNode in self.parentNodes:
            if parentNode.id == newNode.id:
                found = True
                break
        
        if not found:
            self.parentNodes.append(newNode)
            
    def addChildNode(self,newNode):
        if (newNode is None) or (newNode.id == self.id):
            return
        
        found = False
        for childNode in self.childNodes:
            if childNode.id == newNode.id:
                found = True
                break
        
        if not found:
            self.childNodes.append(newNode)
            
    def hasMatchingAuthorsName(self,core_authors):
        for core_author in core_authors:
            core_author = string.split(core_author,' ')[-1]
            if(any( (name.find(core_author) != -1) for name in self.author)):
            #if any( (name.find( core_author ) != -1) for name in self.author):
                    return True
        
        return False
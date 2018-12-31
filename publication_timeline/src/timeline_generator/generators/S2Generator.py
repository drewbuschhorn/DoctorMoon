'''
Created on Jul 6, 2011

@author: dbuschho
'''
import uuid, time, calendar, json
from twisted.internet import defer
from twisted.enterprise import adbapi

class S2Generator(object):

    '''
    classdocs
    '''
    
    def __init__(self, corpus_path, position_database_path):
        '''
        Constructor
        '''
        self.cursor = adbapi.ConnectionPool("sqlite3", position_database_path, check_same_thread=False, cp_max=1)        
        self.uuid = uuid.uuid4();
        self.results = dict()
             
    def _S2DocumentConstructor(self, **keywords):
        return S2Doc(owningGenerator=self, **keywords)
    
    def _S2DocumentHash(self, _S2doc):
        return {_S2doc.id:_S2doc}

    def onResult(self, data):
        # data[0][0] # first row, first column
        # data = [item][id, uuid, start_position_byte, start_position_file, in_citation_count, out_citation_count]
        try: 
            file = data[0][3]          
            with open(file, encoding='utf-8', errors='ignore') as f:
                doc = S2Doc(self)
                f.seek(data[0][2])
                line = f.readline() # Seek S2 file to byte position then read full json record (1 per line)
                json_data = json.loads(line)
                doc.id = json_data['id']
                doc.title = json_data['title']
                doc.cited_works = json_data['outCitations']
                doc.citing_works = json_data['inCitations']
                doc.authors = []
                doc.primary_author = None
                doc.author = None
                doc.author_names = str(json_data['authors'])
                for authors in json_data['authors']:
                    doc.authors.append(authors['ids'])
                    doc.primary_author = doc.authors[-1]
                    doc.author = doc.authors[-1]
                doc.datestamp = None
                if 'year' in json_data:
                    doc.datestamp = calendar.timegm(time.strptime("1 Jan " + str(json_data['year']), "%d %b %Y"))
                else:
                    # Not all records have year values
                    print ("No date info skipping: " + json_data['id'])
                    return doc
                doc.publication_date = doc.datestamp
                return doc
            
        except Exception as inst:
                print ("Error" + str(inst))
                print (json_data)
                print (data)
                return None
    
    @defer.inlineCallbacks                
    def populateNodeFromCustomId(self, custom_id, tries=0):            
        if(custom_id in self.results):
            defer.returnValue(self.results[custom_id])
        
        deferred = self.cursor.runQuery("SELECT * FROM positions WHERE uuid = ?", (custom_id,))
 
        deferred.addCallback(self.onResult)
        a = yield deferred
        defer.returnValue(a)

    def _handleSearchTimeout(self,e):
        raise NameError("Search timed out, %s" %(e.getErrorMessage,))

    @defer.inlineCallbacks
    def findCitingNodes(self, _s2Doc, tries = 0):
        results = []
        
        for item in _s2Doc.getNodeCitedWorksArray():
            try:
                d = self.populateNodeFromCustomId(item)
                d.addErrback(self._handleSearchTimeout)
                #reactor.callLater(10,d.cancel)
                result = yield d
            
            except Exception as inst:
                print (inst)
                print ("failure on findCitingNodes %s, try %s" % (_s2Doc,tries))
                
            if result.id not in self.results:
                self.results.update(self._S2DocumentHash(result))
            else:                
                result = self.results.get(result.id)
            
            if(result.datestamp is None):
                continue
     
            result.addParentNode(_s2Doc)
            _s2Doc.addChildNode(result)
            results.append(result)
    
        defer.returnValue(results)

class S2Doc(object):
    def __repr__(self):
        return self.id    
    def __str__(self):
        return self.id
    
    def __init__ (self, owning_generator=None, **keywords):
        for key in keywords:
            self.__setattr__(key, keywords[key])
        self.owner = owning_generator # Generator used to create this node
        self.uuid = uuid.uuid4()
        self.id = 1
        self.parentNodes = []
        self.childNodes = []

    def getNodeCitedWorksArray(self):
        return self.cited_works
    
    def getNodeCitingWorksArray(self):
        return self.citing_works
    
    def getNodeAuthorsArray(self):
        return self.authors
    
    def getNodePrimaryAuthor(self):
        return self.primary_author
    
    def getNodeUUID(self):
        return self.uuid
    
    def getNodeDate(self):
        return self.datestamp
    
    def getNodeCustomId(self):
        return self.getNodeUUID
    
    def addParentNode(self, new_node):
        if (new_node is None) or (new_node.id == self.id):
            return
        
        found = False
        for parent_node in self.parentNodes:
            if parent_node.id == new_node.id:
                found = True
                break
        
        if not found:
            self.parentNodes.append(new_node)
            
    def addChildNode(self, new_node):
        if (new_node is None) or (new_node.id == self.id):
            return
        
        found = False
        for child_node in self.childNodes:
            if child_node.id == new_node.id:
                found = True
                break
        
        if not found:
            self.childNodes.append(new_node)
            
    def hasMatchingAuthorsName(self,core_authors):
        for core_author in core_authors:
            if [str(core_author)] in self.authors:
            #if any( (name.find( core_author ) != -1) for name in self.author):
                    return True
        
        return False

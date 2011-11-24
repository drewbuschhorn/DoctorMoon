'''
Created on Jul 6, 2011

@author: dbuschho

http://arxiv.org/help/api/examples/python_arXiv_parsing_example.txt
'''

import urllib, feedparser
import AbstractGenerator

class ArxivGenerator(AbstractGenerator.AbstractGenerator):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.base_url = 'http://export.arxiv.org/api/query?'
        # Opensearch metadata such as totalResults, startIndex, 
        # and itemsPerPage live in the opensearch namespase.
        # Some entry metadata lives in the arXiv namespace.
        # This is a hack to expose both of these namespaces in
        # feedparser v4.1
        feedparser._FeedParserMixin.namespaces['http://a9.com/-/spec/opensearch/1.1/'] = 'opensearch'
        feedparser._FeedParserMixin.namespaces['http://arxiv.org/schemas/atom'] = 'arxiv'
        
       
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
    
    def populateNodeFromCustomId(self,customId):
        # perform a GET request using the base_url and query
        query = 'search_query=%s&start=%i&max_results=%i' % \
        (customId, 0,10)
        
        response = urllib.urlopen(self.base_url+query).read()
        
        # parse the response using feedparser
        feed = feedparser.parse(response) 
        # print out feed information
        print 'Feed title: %s' % feed.feed.title
        print 'Feed last updated: %s' % feed.feed.updated
        i = 0
        for entry in feed.entries:
            i=i+1
            print i
            print 'e-print metadata'
            print 'arxiv-id: %s' % entry.id.split('/abs/')[-1]
            print 'Published: %s' % entry.published
            print 'Title:  %s' % entry.title        
    
    
    ####
    # Private functions
    ####
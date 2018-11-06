''' 
Created on Jul 6, 2011

@author: dbuschho
'''
import networkx as nx
import uuid

from twisted.internet import reactor, threads
from twisted.internet.task import deferLater
from twisted.web.server import Site,NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.python.log import err


from Grapher import Grapher
from S2SearchStrategy import S2SearchStrategy

if __name__ == '__main__':
    
    import logging
    logging.basicConfig(filename='example.log', filemode='w', level=logging.DEBUG)
    
    class Maintainer(object):
        def __init__(self):
            self.searcher = None
            self.uuid = uuid.uuid4()
        
        def start(self):#,params):
            self.searcher = S2SearchStrategy('dba56b1d8b91142cc772b04655797d0d0f2fc532', self)
            start = self.searcher.start() 
            #start.addCallback(self._send, params = params)
            #self.params = params
        
        def stop(self):
            print ("ending: %s" %(self.searcher._opennodes,))
            self.grapher()
            #reactor.stop()
        
        def grapher(self):



    


                print ("results length : %s" % (len(self.searcher.generator.results), ))
                
                grapher = Grapher()
    
                newg = nx.Graph()




































                
                for path in self.searcher.useful_paths:
                    print ('%s' % path)
                    #print ('%s - %s' % (self.uuid,path))
                    newg.add_path(path)
                    grapher.paths.append(path)
                
                
                grapher.graph = newg
                #writer = nx.readwrite.graphml.GraphMLWriter(encoding='utf-8')
                #writer.add_graph_element(grapher.graph)
                #output = StringIO.StringIO()
                #writer.dump(self.request)
                
                from networkx.readwrite import d3_js
                
                # mikedewar = nx.read_graphml('mikedewar_rec.graphml')
                mikedewar = newg
                
                # We need to relabel nodes as Twitter name if we want to show the names in the plot
                #def gen_label(node):
                #    label = ""
                #    label = "%s::%s::%s::%d" %(node.path_index,node.publication_date.absdate,node.id,node.hasMatchingAuthorsName(self.searcher.core_authors()))
                #    print label
                #    return label
                    
                #label_dict = dict(map(lambda i : (mikedewar.nodes()[i], gen_label(mikedewar.nodes()[i])), xrange(mikedewar.number_of_nodes())))
                #mikedewar_d3 = nx.relabel_nodes(mikedewar, label_dict)    
                
                # Export 
                #d3_js.export_d3_js(mikedewar_d3, files_dir="mikedewar", graphname="mikedewar", group=None)                
                graph_json = d3_js.d3_json(mikedewar, group=None, searcher=self.searcher)
                
                import json
                #self.request.write(json.dumps(graph_json, indent=2))
                params = self.params
                params['network_graph'] = json.dumps(graph_json, indent=2)
                self.updateDatabase(params)
                
                #self.request.finish()
                #output.close()
                #grapher.render(self.searcher,self.searcher.core_node)
    
    
        def _send(self,result,params):
            #self.send("Run finished","Run finished", "dbuschho@localhost",[params['dbResult'][0][1]])
    	    pass

        def send(self,message=None, subject=None, sender=None, recipients=None, host=None):
            """
            Send email to one or more addresses.
            """
            from email.mime.text import MIMEText
            from twisted.python import log

            import warnings
            warnings.filterwarnings('ignore','.*MimeWriter*.',DeprecationWarning,'twisted' )            
            from twisted.mail.smtp import sendmail


            message = 'This is the message body'
            subject = 'This is the message subject'
            
            host = 'localhost'
            sender = 'dbuschho'
        
            msg = MIMEText(message)
            msg['Subject'] = subject
            msg['From'] = sender
            msg['To'] = ', '.join(recipients)
        
            dfr = sendmail(host, sender, recipients, msg.as_string())
            def success(r):
                return
            def error(e):
                print ("error:115")
                print (e)
            dfr.addCallback(success)
            dfr.addErrback(error)
            
    
        def getUserDataFromDatabase(self,code,entry_id):
            from twisted.enterprise import adbapi
            
            try:
                dbpool = adbapi.ConnectionPool("psycopg2", 
                                database='drmoon', user='postgres', password='django13', host='localhost', port='5432')            
                result = dbpool.runQuery("SELECT auth_user.id,auth_user.email from auth_user LEFT JOIN drmoon_userprofile ON drmoon_userprofile.user_id = auth_user.id WHERE drmoon_userprofile.request_code = %s ",(code,))
                 
                result.addCallback(self.createNewNetworkEntry,code=code,entry_id=entry_id)
                result.addErrback(self.printresult)
                #result.addErrback
            except Exception as e:
                print (e)
            
            return result
        
        def createNewNetworkEntry(self,dbResult,code,entry_id):
            from twisted.enterprise import adbapi
            dbpool = adbapi.ConnectionPool("psycopg2", 
                            database='drmoon', user='postgres', password='django13', host='localhost', port='5432')            
            
            result = dbpool.runInteraction(self._createNewNetworkEntry,dbResult=dbResult,code=entry_id)
            result.addCallback(self._handleStartActions,entry_id=entry_id,dbResult=dbResult,code=entry_id)
            result.addErrback(self.printresult)
        
        def _createNewNetworkEntry(self,txn,dbResult,code):
            user_id = dbResult[0][0]

            txn.execute("INSERT INTO drmoon_networkgraph( \
                user_id, created, modified, unique_id, graph_data, shared, complete) \
                VALUES (%s, NOW(), NOW(), %s, %s ,false,false)",(user_id,code,' '))
            
            txn.execute("SELECT lastval()")
            result = txn.fetchall()
            return result[0][0]

        def _handleStartActions(self,result,entry_id,dbResult,code):
            params = {'entry_id':entry_id,'dbResult':dbResult,'code':code,'id':result}
            self.start(params)
            
            import json
            self.request.write(json.dumps(params))
            
            self.request.finish()

        def updateDatabase(self,params):
            # Using the "dbmodule" from the previous example, create a ConnectionPool 
            from twisted.enterprise import adbapi
            dbpool = adbapi.ConnectionPool("psycopg2", 
                            database='drmoon', user='postgres', password='django13', host='localhost', port='5432')            
            
            # equivalent of cursor.execute(statement), return cursor.fetchall():
            dbpool.runInteraction(self._updateDatabase,params)
            
        def _updateDatabase(self,txn,params):
            print ("--params--")
            print (params)
            id = params['id']
                
            txn.execute(
                "SELECT id FROM drmoon_networkgraph WHERE id = %s",
                (id,)
            )
            
            result = txn.fetchone()                
            print (result)
            
            if(result):
                txn.execute(
                    "UPDATE drmoon_networkgraph SET unique_id = %s, graph_data = %s, complete = %s WHERE id = %s",
                    (params['entry_id'],params['network_graph'], True, id)
                )
            else:
                raise Exception("Database Exception")
        
        def printresult(self,x):
                print (x)
                return x
                       
    class FormPage(Resource):
        isLeaf = True
        def render_OPTIONS(self,request):
            request.setHeader('Access-Control-Allow-Origin','*')
            request.setHeader('Access-Control-Allow-Methods','POST, GET, OPTIONS')
            request.setHeader('Access-Control-Max-Age',1000)
            request.setHeader('Access-Control-Allow-Headers','*')
            request.finish()            
            return NOT_DONE_YET    
        
        def render_POST(self, request):
            return self.render_GET(request)
        
        def render_GET(self, request):
            
            request.setHeader('Content-Type','application/json')
            request.setHeader('Access-Control','allow <*>')
            request.setHeader('Access-Control-Allow-Origin','*')
            
            m = Maintainer()
            m.request = request
                        
            m.getUserDataFromDatabase(request.args['code'][0],request.args['doi'][0])
            
            #
            #
                        
            return NOT_DONE_YET
    
    #root = Resource()
    #root.putChild("form", FormPage())
    #factory = Site(root)
    #reactor.listenTCP(8880, factory)
    
    m = Maintainer()
    m.start()
    
    reactor.run()
    #m.grapher()

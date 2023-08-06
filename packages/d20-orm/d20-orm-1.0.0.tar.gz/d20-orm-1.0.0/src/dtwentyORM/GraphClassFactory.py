from pyArango.connection import *
from pyArango.collection import *
from pyArango.graph import *
from dtwentyORM import Metadata, Element
from .Error import *
import pyArango
import os
import json



class ClassFactory():


    class paymentsgraph(pyArango.graph.Graph):
        _edgeDefinitions = (pyArango.graph.EdgeDefinition ('PaysWith',
                                        fromCollections = ['Users'],
                                        toCollections = ['PaymentMethods']),
                            pyArango.graph.EdgeDefinition ('PaidBy',
                                        fromCollections = ['Charges'],
                                        toCollections = ['PaymentMethods']),
                            pyArango.graph.EdgeDefinition ('Settled',
                                        fromCollections = ['Charges'],
                                        toCollections = ['Payments']),
                            pyArango.graph.EdgeDefinition ('Checkout',
                                        fromCollections = ['Orders'],
                                        toCollections = ['Payments']),
        )
        _orphanedCollections = []





    def __init__(self, graphname, collections = [], edges = [], orphans = [], edgeDefinitions=(), prefix='', conf=None):
        if type(conf) != dict and os.environ.get(f'{prefix}_CONF') != None:
            conf = json.loads(os.environ.get(f'{prefix}_CONF'))
            arangoURL=conf.get(f'{prefix}_DBURL')
            username=conf.get(f'{prefix}_DBUSERNAME')
            password=conf.get(f'{prefix}_DBPASSWORD')
            self.db_name=conf.get(f'{prefix}_DBNAME')        
        else:
            raise MissingConfigurationException
        arangoURL=conf.get(f'{prefix}_DBURL')
        username=conf.get(f'{prefix}_DBUSERNAME')
        password=conf.get(f'{prefix}_DBPASSWORD')
        self.db_name=conf.get(f'{prefix}_DBNAME')

        self.db_client = Connection(arangoURL=arangoURL, username=username, password=password, verify=True, verbose=True, statsdClient=None, reportFileName=None, loadBalancing='round-robin', use_grequests=False, use_jwt_authentication=False, use_lock_for_reseting_jwt=True, max_retries=10)

        db_collections = collections
        db_edges = edges
        db_orphans = orphans
        db_edgeDefinitions = edgeDefinitions

        globals()[graphname] = type(graphname, (pyArango.graph.Graph,), {"_edgeDefinitions" : tuple(db_edgeDefinitions), "_orphanedCollections" : db_orphans })

        for cl in db_collections:
            globals()[cl] = type(cl, (Collection,), {"_fields" : {}})

        for cl in db_edges:
            globals()[cl] = type(cl, (Edges,), {"_fields" : {}})

        if not self.db_client.hasDatabase(self.db_name):
            self.db = self.db_client.createDatabase(self.db_name)
        else:
            self.db = self.db_client[self.db_name]
        for col in db_collections:
            if not self.db.hasCollection(col):
                self.db.createCollection(className='Collection', name=col)
        for col in db_edges:
            if not self.db.hasCollection(col):
                self.db.createCollection(className='Edges', name=col)
        if not self.db.hasGraph(graphname):
            self.db.createGraph(graphname)





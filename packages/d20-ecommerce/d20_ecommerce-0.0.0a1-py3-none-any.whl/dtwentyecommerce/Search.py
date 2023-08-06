from pyArango.connection import *
from pyArango.collection import *
from pyArango.graph import *
from dtwentyORM import Metadata, Element
from dtwentyCommunications import *
from Classes import Query, Included, Searched, Retrieved, ToCart
from tools import *
from .Error import *
import pyArango
import os
import json

#### Collections CRUD ####
#### Query ####
def create_query(create_dict:dict) -> Query:
    if not check_type_requirements('query', create_dict): 
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_query = Query('create', create_dict)
    return new_query

def get_query(id:str) -> Query:
    query = Query('find', {'_key':id})
    return query

def update_query(id:str, update_dict:dict, user_updated='native') -> Query:
    query = get_query(id)
    update_dict['_key'] = query.get('_key')
    update_dict['user_updated'] = user_updated
    updated_query = Query('update', update_dict)
    return updated_query

def delete_query(id:str) -> bool:
    query = get_query(id)
    query.delete()
    return query.get('status')



#### Retrieved ####
def create_retrived(create_dict:dict) -> Retrieved:
    if not check_type_requirements('retrived', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_retrived = Retrieved('create', create_dict)
    return new_retrived

def get_retrived(id:str) -> Retrieved:
    retrived = Retrieved('find', {'_key':id})
    return retrived

def update_retrived(id:str, update_dict:dict, user_updated='native') -> Retrieved:
    retrived = get_retrived(id)
    update_dict['_key'] = retrived.get('_key')
    update_dict['user_updated'] = user_updated
    updated_retrived = Retrieved('update', update_dict)
    return updated_retrived

def delete_retrived(id:str) -> bool:
    retrived = get_retrived(id)
    retrived.delete()
    return retrived.get('status')



#### Included ####
def create_included(create_dict:dict) -> Included:
    if not check_type_requirements('included', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_included = Included('create', create_dict)
    return new_included

def get_included(id:str) -> Included:
    included = Included('find', {'_key':id})
    return included

def update_included(id:str, update_dict:dict, user_updated='native') -> Included:
    included = get_included(id)
    update_dict['_key'] = included.get('_key')
    update_dict['user_updated'] = user_updated
    updated_included = Included('update', update_dict)
    return updated_included

def delete_included(id:str) -> bool:
    included = get_included(id)
    included.delete()
    return included.get('status')



#### ToCart ####
def create_to_cart(create_dict:dict) -> ToCart:
    if not check_type_requirements('tocart', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_to_cart = ToCart('create', create_dict)
    return new_to_cart

def get_to_cart(id:str) -> ToCart:
    to_cart = ToCart('find', {'_key':id})
    return to_cart

def update_to_cart(id:str, update_dict:dict, user_updated='native') -> ToCart:
    to_cart = get_to_cart(id)
    update_dict['_key'] = to_cart.get('_key')
    update_dict['user_updated'] = user_updated
    updated_to_cart = ToCart('update', update_dict)
    return updated_to_cart

def delete_to_cart(id:str) -> bool:
    to_cart = get_to_cart(id)
    to_cart.delete()
    return to_cart.get('status')



#### Searched ####
def create_searched(create_dict:dict) -> Searched:
    if not check_type_requirements('searched', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_searched = Searched('create', create_dict)
    return new_searched

def get_searched(id:str) -> Searched:
    searched = Searched('find', {'_key':id})
    return searched

def update_searched(id:str, update_dict:dict, user_updated='native') -> Searched:
    searched = get_searched(id)
    update_dict['_key'] = searched.get('_key')
    update_dict['user_updated'] = user_updated
    updated_searched = Searched('update', update_dict)
    return updated_searched

def delete_searched(id:str) -> bool:
    searched = get_searched(id)
    searched.delete()
    return searched.get('status')

class Search():
    db_name=''
    if os.environ.get('D20_EC_CONF') != None:
        conf = json.loads(os.environ.get('D20_EC_CONF'))
        arangoURL=conf.get('D20_EC_DBURL')
        username=conf.get('D20_EC_DBUSERNAME')
        password=conf.get('D20_EC_DBPASSWORD')
        db_name=conf.get('D20_EC_DBNAME')        
    else:
        raise MissingConfigurationException

    db_client = Connection(arangoURL=arangoURL, username=username, password=password, verify=True, verbose=True, statsdClient=None, reportFileName=None, loadBalancing='round-robin', use_grequests=False, use_jwt_authentication=False, use_lock_for_reseting_jwt=True, max_retries=10)

    db_collections = ['Queries']
    db_edges = ['Retrieved','Included', 'ToCart', 'Searched']


    class querygraph(pyArango.graph.Graph):
        _edgeDefinitions = (pyArango.graph.EdgeDefinition ('Retrieved',
                                        fromCollections = ['Queries'],
                                        toCollections = ['Products']),
                            pyArango.graph.EdgeDefinition ('Included',
                                        fromCollections = ['Users'],
                                        toCollections = ['Products', 'Brands', 'Categories', 'Promotions']),
                            pyArango.graph.EdgeDefinition ('ToCart',
                                        fromCollections = ['Queries'],
                                        toCollections = ['Carts']),
                            pyArango.graph.EdgeDefinition ('Searched',
                                        fromCollections = ['Users'],
                                        toCollections = ['Queries']),
        )
        _orphanedCollections = []
        
    for cl in db_collections:
        globals()[cl] = type(cl, (Collection,), {"_fields" : {}})

    for cl in db_edges:
        globals()[cl] = type(cl, (Edges,), {"_fields" : {}})

    def __init__(self):
        if not self.db_client.hasDatabase(self.db_name):
            self.db = self.db_client.createDatabase(self.db_name)
        else:
            self.db = self.db_client[self.db_name]
        for col in self.db_collections:
            if not self.db.hasCollection(col):
                self.db.createCollection(className='Collection', name=col)
        for col in self.db_edges:
            if not self.db.hasCollection(col):
                self.db.createCollection(className='Edges', name=col)
        if not self.db.hasGraph('ecomgraph'):
            self.db.createGraph('ecomgraph')



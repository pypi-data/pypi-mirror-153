from pyArango.connection import *
from pyArango.collection import *
from pyArango.graph import *
from dtwentyORM import Metadata, Element
from dtwentyCommunications import *
from Classes import Order, Cart, Selected, Converted, Purchased, Invoice, CartContains, OrderContains, ProductImage, Variation
from .tools import *
from .Error import *
import pyArango
import os
import json

#### Collection CRUD ####

#### Cart ####
def create_cart(create_dict:dict) -> Cart: 
    if not check_type_requirements('cart', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_cart = Cart('create', create_dict)
    return new_cart

def get_cart(id:str) -> Cart:
    cart = Cart('find', {'_key':id})
    return cart

def update_cart(id:str, update_dict:dict, user_updated='native') -> Cart:
    cart = get_cart(id)
    update_dict['_key'] = cart.get('_key')
    update_dict['user_updated'] = user_updated
    updated_cart = Cart('update', update_dict)
    return updated_cart

def delete_cart(id:str) -> bool:
    cart = get_cart(id)
    cart.delete()
    return cart.get('status')



#### Order ####
def create_order(create_dict:dict) -> Order:
    if not check_type_requirements('order', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_order = Order('create', create_dict)
    return new_order

def get_order(id:str) -> Order:
    order = Order('find', {'_key':id})
    return order

def update_order(id:str, update_dict:dict, user_updated='native') -> Order:
    order = get_order(id)
    update_dict['_key'] = order.get('_key')
    update_dict['user_updated'] = user_updated
    updated_order = Order('update', update_dict)
    return updated_order

def delete_order(id:str) -> bool:
    order = get_order(id)
    order.delete()
    return order.get('status')



#### Selected ####
def create_selected(create_dict:dict) -> Selected:
    if not check_type_requirements('selected', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_selected = Selected('create', create_dict)
    return new_selected

def get_selected(id:str) -> Selected:
    selected = Selected('find', {'_key':id})
    return selected

def update_selected(id:str, update_dict:dict, user_updated='native') -> Selected:
    selected = get_selected(id)
    update_dict['_key'] = selected.get('_key')
    update_dict['user_updated'] = user_updated
    updated_selected = Selected('update', update_dict)
    return updated_selected

def delete_selected(id:str) -> bool:
    selected = get_selected(id)
    selected.delete()
    return selected.get('status')



#### Purchased ####
def create_purchased(create_dict:dict) -> Purchased:
    if not check_type_requirements('purchased', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_purchased = Purchased('create', create_dict)
    return new_purchased

def get_purchased(id:str) -> Purchased:
    purchased = Purchased('find', {'_key':id})
    return purchased

def update_purchased(id:str, update_dict:dict, user_updated='native') -> Purchased:
    purchased = get_purchased(id)
    update_dict['_key'] = purchased.get('_key')
    update_dict['user_updated'] = user_updated
    updated_purchased = Purchased('update', update_dict)
    return updated_purchased

def delete_purchased(id:str) -> bool:
    purchased = get_purchased(id)
    purchased.delete()
    return purchased.get('status')



#### Converted ####
def create_converted(create_dict:dict) -> Converted:
    if not check_type_requirements('converted', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_converted = Converted('create', create_dict)
    return new_converted

def get_converted(id:str) -> Converted:
    converted = Converted('find', {'_key':id})
    return converted

def update_converted(id:str, update_dict:dict, user_updated='native') -> Converted:
    converted = get_converted(id)
    update_dict['_key'] = converted.get('_key')
    update_dict['user_updated'] = user_updated
    updated_converted = Converted('update', update_dict)
    return updated_converted

def delete_converted(id:str) -> bool:
    converted = get_converted(id)
    converted.delete()
    return converted.get('status')



#### CartContains ####
def create_cart_contains(create_dict:dict) -> CartContains:
    if not check_type_requirements('cartcontains', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_cart_contains = CartContains('create', create_dict)
    return new_cart_contains

def get_cart_contains(id:str) -> CartContains:
    cart_contains = CartContains('find', {'_key':id})
    return cart_contains

def update_cart_contains(id:str, update_dict:dict, user_updated='native') -> CartContains:
    cart_contains = get_cart_contains(id)
    update_dict['_key'] = cart_contains.get('_key')
    update_dict['user_updated'] = user_updated
    updated_cart_contains = CartContains('update', update_dict)
    return updated_cart_contains

def delete_cart_contains(id:str) -> bool:
    cart_contains = get_cart_contains(id)
    cart_contains.delete()
    return cart_contains.get('status')



#### OrderContains ####
def create_order_contains(create_dict:dict) -> OrderContains:
    if not check_type_requirements('ordercontains', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_order_contains = OrderContains('create', create_dict)
    return new_order_contains

def get_order_contains(id:str) -> OrderContains:
    order_contains = OrderContains('find', {'_key':id})
    return order_contains

def update_order_contains(id:str, update_dict:dict, user_updated='native') -> OrderContains:
    order_contains = get_order_contains(id)
    update_dict['_key'] = order_contains.get('_key')
    update_dict['user_updated'] = user_updated
    updated_order_contains = OrderContains('update', update_dict)
    return updated_order_contains

def delete_order_contains(id:str) -> bool:
    order_contains = get_order_contains(id)
    order_contains.delete()
    return order_contains.get('status')



#### Invoice ####
def create_invoice(create_dict:dict) -> Invoice:
    if not check_type_requirements('invoice', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_invoice = Invoice('create', create_dict)
    return new_invoice

def get_invoice(id:str) -> Invoice:
    invoice = Invoice('find', {'_key':id})
    return invoice

def update_invoice(id:str, update_dict:dict, user_updated='native') -> Invoice:
    invoice = get_invoice(id)
    update_dict['_key'] = invoice.get('_key')
    update_dict['user_updated'] = user_updated
    updated_invoice = Invoice('update', update_dict)
    return updated_invoice

def delete_invoice(id:str) -> bool:
    invoice = get_invoice(id)
    invoice.delete()
    return invoice.get('status')



#### ProductImage ####
def create_product_image(create_dict:dict) -> ProductImage:
    if not check_type_requirements('productimage', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_product_image = ProductImage('create', create_dict)
    return new_product_image

def get_product_image(id:str) -> ProductImage:
    product_image = ProductImage('find', {'_key':id})
    return product_image

def update_product_image(id:str, update_dict:dict, user_updated='native') -> ProductImage:
    product_image = get_product_image(id)
    update_dict['_key'] = product_image.get('_key')
    update_dict['user_updated'] = user_updated
    updated_product_image = ProductImage('update', update_dict)
    return updated_product_image

def delete_product_image(id:str) -> bool:
    product_image = get_product_image(id)
    product_image.delete()
    return product_image.get('status')



#### Variation ####
def create_variation(create_dict:dict) -> Variation:
    if not check_type_requirements('variation', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_variation = Variation('create', create_dict)
    return new_variation

def get_variation(id:str) -> Variation:
    variation = Variation('find', {'_key':id})
    return variation

def update_variation(id:str, update_dict:dict, user_updated='native') -> Variation:
    variation = get_variation(id)
    update_dict['_key'] = variation.get('_key')
    update_dict['user_updated'] = user_updated
    updated_variation = Variation('update', update_dict)
    return updated_variation

def delete_variation(id:str) -> bool:
    variation = get_variation(id)
    variation.delete()
    return variation.get('status')

class Shopping():
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

    db_collections = ['Carts','Orders']
    db_edges = ['Selected','Purchased','Converted','CartContains', 'OrderContains','Invoice', 'Variation']


    class ecomgraph(pyArango.graph.Graph):
        _edgeDefinitions = (pyArango.graph.EdgeDefinition ('Selected',
                                        fromCollections = ['Users'],
                                        toCollections = ['Carts']),
                            pyArango.graph.EdgeDefinition ('Purchased',
                                        fromCollections = ['Users'],
                                        toCollections = ['Orders']),
                            pyArango.graph.EdgeDefinition ('Converted',
                                        fromCollections = ['Carts'],
                                        toCollections = ['Orders']),
                            pyArango.graph.EdgeDefinition ('CartContains',
                                        fromCollections = ['Carts'],
                                        toCollections = ['Products']),
                            pyArango.graph.EdgeDefinition ('OrderContains',
                                        fromCollections = ['Orders'],
                                        toCollections = ['Products']),
                            pyArango.graph.EdgeDefinition ('Invoice',
                                        fromCollections = ['Orders'],
                                        toCollections = ['TaxProfiles']),
                            pyArango.graph.EdgeDefinition ('Variation',
                                        fromCollections = ['Products'],
                                        toCollections = ['Products']),
        )
        _orphanedCollections = ['ProductImages']
        
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



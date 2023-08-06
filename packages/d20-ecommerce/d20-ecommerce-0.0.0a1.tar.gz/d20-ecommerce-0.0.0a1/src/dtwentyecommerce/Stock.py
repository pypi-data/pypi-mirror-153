from pyArango.connection import *
from pyArango.collection import *
from pyArango.graph import *
from Classes import Brand, Stock, Makes, BelongsTo, SellsFor, Product, Holds, Category, Price, Promotion, Vendor, IncludesPromo, OfferedBy, LocatedAt, Availability
from .Error import *
from .tools import *
import pyArango
import os
import json

#### Colletion CRUD ####

#### Brand ####
def create_brand(create_dict:dict) -> Brand:
    if not check_type_requirements('brand', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_brand = Brand('create', create_dict)
    return new_brand

def get_brand(id:str) -> Brand:
    brand = Brand('find', {'_key':id})
    return brand

def update_brand(id:str, update_dict:dict, user_updated='native') -> Brand: 
    brand = get_brand(id)
    update_dict['_key'] = brand.get('_key')
    update_dict['user_updated'] = user_updated
    updated_brand = Brand('update', update_dict)
    return updated_brand

def delete_brand(id:str) -> bool:
    brand = get_brand(id)
    brand.delete()
    return brand.get('status')



#### Category ####
def create_category(create_dict:dict) -> Category:
    if not check_type_requirements('category', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_category = Category('create', create_dict)
    return new_category

def get_category(id:str) -> Category:
    category = Category('find', {'_key':id})
    return category

def update_category(id:str, update_dict:dict, user_updated='native') -> Category:
    category = get_category(id)
    update_dict['_key'] = category.get('_key')
    update_dict['user_updated'] = user_updated
    updated_category = Category('update', update_dict)
    return updated_category

def delete_category(id:str) -> bool:
    category = get_category(id)
    category.delete()
    return category.get('status')



#### Price ####
def create_price(create_dict:dict) -> Price:
    if not check_type_requirements('price', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_price = Price('create', create_dict)
    return new_price

def get_price(id:str) -> Price:
    price = Price('find', {'_key':id})
    return price

def update_price(id:str, update_dict:dict, user_updated='native') -> Price:
    price = get_price(id)
    update_dict['_key'] = price.get('_key')
    update_dict['user_updated'] = user_updated
    updated_price = Price('update', update_dict)
    return updated_price

def delete_price(id:str) -> bool:
    price = get_price(id)
    price.delete()
    return price.get('status')



#### Product ####
def create_product(create_dict:dict) -> Product:
    if not check_type_requirements('product', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_product = Product('create', create_dict)
    return new_product

def get_product(id:str) -> Product:
    product = Product('find', {'_key':id})
    return product

def update_product(id:str, update_dict:dict, user_updated='native') -> Product:
    product = get_product(id)
    update_dict['_key'] = product.get('_key')
    update_dict['user_updated'] = user_updated
    updated_product = Product('update', update_dict)
    return updated_product

def delete_product(id:str) -> bool:
    product = get_product(id)
    product.delete()
    return product.get('status')



#### Promotion ####
def create_promotion(create_dict:dict) -> Promotion:
    if not check_type_requirements('promotion', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_promotion = Promotion('create', create_dict)
    return new_promotion

def get_promotion(id:str) -> Promotion:
    promotion = Promotion('find', {'_key':id})
    return promotion

def update_promotion(id:str, update_dict:dict, user_updated='native') -> Promotion:
    promotion = get_promotion(id)
    update_dict['_key'] = promotion.get('_key')
    update_dict['user_updated'] = user_updated
    updated_promotion = Promotion('update', update_dict)
    return updated_promotion

def delete_promotion(id:str) -> bool:
    promotion = get_promotion(id)
    promotion.delete()
    return promotion.get('status')



#### Vendor ####
def create_vendor(create_dict:dict) -> Vendor:
    if not check_type_requirements('vendor', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_vendor = Vendor('create', create_dict)
    return new_vendor

def get_vendor(id:str) -> Vendor:
    vendor = Vendor('find', {'_key':id})
    return vendor

def update_vendor(id:str, update_dict:dict, user_updated='native') -> Vendor:
    vendor = get_vendor(id)
    update_dict['_key'] = vendor.get('_key')
    update_dict['user_updated'] = user_updated
    updated_vendor = Vendor('update', update_dict)
    return updated_vendor

def delete_vendor(id:str) -> bool:
    vendor = get_vendor(id)
    vendor.delete()
    return vendor.get('status')



#### Stock ####
def create_stock(create_dict:dict) -> Stock:
    if not check_type_requirements('stock', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_stock = Stock('create', create_dict)
    return new_stock

def get_stock(id:str) -> Stock:
    stock = Stock('find', {'_key':id})
    return stock

def update_stock(id:str, update_dict:dict, user_updated='native') -> Stock:
    stock = get_stock(id)
    update_dict['_key'] = stock.get('_key')
    update_dict['user_updated'] = user_updated
    updated_stock = Stock('update', update_dict)
    return updated_stock

def delete_stock(id:str) -> bool:
    stock = get_stock(id)
    stock.delete()
    return stock.get('status')



#### IncludesPromo ####
def create_includes_promo(create_dict:dict) -> IncludesPromo:
    if not check_type_requirements('includespromo', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_includes_promo = IncludesPromo('create', create_dict)
    return new_includes_promo

def get_includes_promo(id:str) -> IncludesPromo:
    includes_promo = IncludesPromo('find', {'_key':id})
    return includes_promo

def update_includes_promo(id:str, update_dict:dict, user_updated='native') -> IncludesPromo:
    includes_promo = get_includes_promo(id)
    update_dict['_key'] = includes_promo.get('_key')
    update_dict['user_updated'] = user_updated
    updated_includes_promo = IncludesPromo('update', update_dict)
    return updated_includes_promo

def delete_includes_promo(id:str) -> bool:
    includes_promo = get_includes_promo(id)
    includes_promo.delete()
    return includes_promo.get('status')



#### Availability ####
def create_availability(create_dict:dict) -> Availability:
    if not check_type_requirements('availability', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_availability = Availability('create', create_dict)
    return new_availability

def get_availability(id:str) -> Availability:
    availability = Availability('find', {'_key':id})
    return availability

def update_availability(id:str, update_dict:dict, user_updated='native') -> Availability:
    availability = get_availability(id)
    update_dict['_key'] = availability.get('_key')
    update_dict['user_updated'] = user_updated
    updated_availability = Availability('update', update_dict)
    return updated_availability

def delete_availability(id:str) -> bool:
    availability = get_availability(id)
    availability.delete()
    return availability.get('status')



#### BelongsTo ####
def create_belongs_to(create_dict:dict) -> BelongsTo:
    if not check_type_requirements('belongsto', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_belongs_to = BelongsTo('create', create_dict)
    return new_belongs_to

def get_belongs_to(id:str) -> BelongsTo:
    belongs_to = BelongsTo('find', {'_key':id})
    return belongs_to

def update_belongs_to(id:str, update_dict:dict, user_updated='native') -> BelongsTo:
    belongs_to = get_belongs_to(id)
    update_dict['_key'] = belongs_to.get('_key')
    update_dict['user_updated'] = user_updated
    updated_belongs_to = BelongsTo('update', update_dict)
    return updated_belongs_to

def delete_belongs_to(id:str) -> bool:
    belongs_to = get_belongs_to(id)
    belongs_to.delete()
    return belongs_to.get('status')



#### SellsFor ####
def create_sells_for(create_dict:dict) -> SellsFor:
    if not check_type_requirements('sellsfor', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_sells_for = SellsFor('create', create_dict)
    return new_sells_for

def get_sells_for(id:str) -> SellsFor:
    sells_for = SellsFor('find', {'_key':id})
    return sells_for

def update_sells_for(id:str, update_dict:dict, user_updated='native') -> SellsFor:
    sells_for = get_sells_for(id)
    update_dict['_key'] = sells_for.get('_key')
    update_dict['user_updated'] = user_updated
    updated_sells_for = SellsFor('update', update_dict)
    return updated_sells_for

def delete_sells_for(id:str) -> bool:
    sells_for = get_sells_for(id)
    sells_for.delete()
    return sells_for.get('status')



#### Makes ####
def create_makes(create_dict:dict) -> Makes:
    if not check_type_requirements('makes', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_makes = Makes('create', create_dict)
    return new_makes

def get_makes(id:str) -> Makes:
    makes = Makes('find', {'_key':id})
    return makes

def update_makes(id:str, update_dict:dict, user_updated='native') -> Makes:
    makes = get_makes(id)
    update_dict['_key'] = makes.get('_key')
    update_dict['user_updated'] = user_updated
    updated_makes = Makes('update', update_dict)
    return updated_makes

def delete_makes(id:str) -> bool:
    makes = get_makes(id)
    makes.delete()
    return makes.get('status')



#### OfferedBy ####
def create_offered_by(create_dict:dict) -> OfferedBy:
    if not check_type_requirements('offeredby', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_offered_by = OfferedBy('create', create_dict)
    return new_offered_by

def get_offered_by(id:str) -> OfferedBy:
    offered_by = OfferedBy('find', {'_key':id})
    return offered_by

def update_offered_by(id:str, update_dict:dict, user_updated='native') -> OfferedBy:
    offered_by = get_offered_by(id)
    update_dict['_key'] = offered_by.get('_key')
    update_dict['user_updated'] = user_updated
    updated_offered_by = OfferedBy('update', update_dict)
    return updated_offered_by

def delete_offered_by(id:str) -> bool:
    offered_by = get_offered_by(id)
    offered_by.delete()
    return offered_by.get('status')



#### Holds ####
def create_holds(create_dict:dict) -> Holds:
    if not check_type_requirements('holds', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_holds = Holds('create', create_dict)
    return new_holds

def get_holds(id:str) -> Holds:
    holds = Holds('find', {'_key':id})
    return holds

def update_holds(id:str, update_dict:dict, user_updated='native') -> Holds:
    holds = get_holds(id)
    update_dict['_key'] = holds.get('_key')
    update_dict['user_updated'] = user_updated
    updated_holds = Holds('update', update_dict)
    return updated_holds

def delete_holds(id:str) -> bool:
    holds = get_holds(id)
    holds.delete()
    return holds.get('status')



#### LocatedAt ####
def create_located_at(create_dict:dict) -> LocatedAt:
    if not check_type_requirements('locatedat', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_located_at = LocatedAt('create', create_dict)
    return new_located_at

def get_located_at(id:str) -> LocatedAt:
    located_at = LocatedAt('find', {'_key':id})
    return located_at

def update_located_at(id:str, update_dict:dict, user_updated='native') -> LocatedAt:
    located_at = get_located_at(id)
    update_dict['_key'] = located_at.get('_key')
    update_dict['user_updated'] = user_updated
    updated_located_at = LocatedAt('update', update_dict)
    return updated_located_at

def delete_located_at(id:str) -> bool:
    located_at = get_located_at(id)
    located_at.delete()
    return located_at.get('status')

class Stock():
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

    db_collections = ['Brands','Categories','Prices','Products','Promotions','Vendors','Stock']
    db_edges = ['IncludesPromo','Availability','BelongsTo','SellsFor','Makes','OfferedBy', 'Holds', 'LocatedAt']


    class offergraph(pyArango.graph.Graph):
        _edgeDefinitions = (pyArango.graph.EdgeDefinition ('IncludesPromo',
                                        fromCollections = ['Products'],
                                        toCollections = ['Promotions']),
                            pyArango.graph.EdgeDefinition ('Availability',
                                        fromCollections = ['Products'],
                                        toCollections = ['Stock']),
                            pyArango.graph.EdgeDefinition ('BelongsTo',
                                        fromCollections = ['Products'],
                                        toCollections = ['Categories']),
                            pyArango.graph.EdgeDefinition ('SellsFor',
                                        fromCollections = ['Products'],
                                        toCollections = ['Prices']),
                            pyArango.graph.EdgeDefinition ('Makes',
                                        fromCollections = ['Brands'],
                                        toCollections = ['Products']),
                            pyArango.graph.EdgeDefinition ('OfferedBy',
                                        fromCollections = ['Products'],
                                        toCollections = ['Vendors']),
                            pyArango.graph.EdgeDefinition ('Holds',
                                        fromCollections = ['Vendors'],
                                        toCollections = ['Stock']),
                            pyArango.graph.EdgeDefinition ('LocatedAt',
                                        fromCollections = ['Vendors'],
                                        toCollections = ['Addresses']),
                            pyArango.graph.EdgeDefinition ('VendorTax',
                                        fromCollections = ['Vendors'],
                                        toCollections = ['TaxProfile']),
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
        if not self.db.hasGraph('offergraph'):
            self.db.createGraph('offergraph')



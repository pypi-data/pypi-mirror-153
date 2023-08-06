from pyArango.connection import *
from pyArango.collection import *
from pyArango.graph import *
from dtwentyORM import Metadata, Element
from dtwentyCommunications import *
from .Error import *
from .tools import *
from Classes import Payment, PaymentMethod, Checkout, Charge, PaysWith, PaidBy, Settled
import pyArango
import os
import json


#### PaymentMethod ####
def create_payment_method(create_dict:dict) -> PaymentMethod:
    if not check_type_requirements('paymentmethod', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_payment_method = PaymentMethod('create', create_dict)
    return new_payment_method
def get_payment_method(id:str) -> PaymentMethod:
    payment_method = PaymentMethod('find', {'_key':id})
    return payment_method
def update_payment_method(id:str, update_dict:dict, user_updated='native') -> PaymentMethod:
    payment_method = get_payment_method(id)
    update_dict['_key'] = payment_method.get('_key')
    update_dict['user_updated'] = user_updated
    updated_payment_method = PaymentMethod('update', update_dict)
    return updated_payment_method
def delete_payment_method(id:str) -> bool:
    payment_method = get_payment_method(id)
    payment_method.delete()
    return payment_method.get('status')


#### Charge ####
def create_charge(create_dict:dict) -> Charge:
    if not check_type_requirements('charge', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_charge = Charge('create', create_dict)
    return new_charge

def get_charge(id:str) -> Charge:
    charge = Charge('find', {'_key':id})
    return charge

def update_charge(id:str, update_dict:dict, user_updated='native') -> Charge:
    charge = get_charge(id)
    update_dict['_key'] = charge.get('_key')
    update_dict['user_updated'] = user_updated
    updated_charge = Charge('update', update_dict)
    return updated_charge

def delete_charge(id:str) -> bool:
    charge = get_charge(id)
    charge.delete()
    return charge.get('status')


#### Payment ####
def create_payment(create_dict:dict) -> Payment:
    if not check_type_requirements('payment', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_payment = Payment('create', create_dict)
    return new_payment

def get_payment(id:str) -> Payment:
    payment = Payment('find', {'_key':id})
    return payment

def update_payment(id:str, update_dict:dict, user_updated='native') -> Payment:
    payment = get_payment(id)
    update_dict['_key'] = payment.get('_key')
    update_dict['user_updated'] = user_updated
    updated_payment = Payment('update', update_dict)
    return updated_payment

def delete_payment(id:str) -> bool:
    payment = get_payment(id)
    payment.delete()
    return payment.get('status')


#### PaysWith ####
def create_pays_with(create_dict:dict) -> PaysWith:
    if not check_type_requirements('payswith', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_pays_with = PaysWith('create', create_dict)
    return new_pays_with

def get_pays_with(id:str) -> PaysWith:
    pays_with = PaysWith('find', {'_key':id})
    return pays_with

def update_pays_with(id:str, update_dict:dict, user_updated='native') -> PaysWith:
    pays_with = get_pays_with(id)
    update_dict['_key'] = pays_with.get('_key')
    update_dict['user_updated'] = user_updated
    updated_pays_with = PaysWith('update', update_dict)
    return updated_pays_with

def delete_pays_with(id:str) -> bool:
    pays_with = get_pays_with(id)
    pays_with.delete()
    return pays_with.get('status')


#### PaidBy ####
def create_paid_by(create_dict:dict) -> PaidBy:
    if not check_type_requirements('paidby', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_paid_by = PaidBy('create', create_dict)
    return new_paid_by

def get_paid_by(id:str) -> PaidBy:
    paid_by = PaidBy('find', {'_key':id})
    return paid_by

def update_paid_by(id:str, update_dict:dict, user_updated='native') -> PaidBy:
    paid_by = get_paid_by(id)
    update_dict['_key'] = paid_by.get('_key')
    update_dict['user_updated'] = user_updated
    updated_paid_by = PaidBy('update', update_dict)
    return updated_paid_by

def delete_paid_by(id:str) -> bool:
    paid_by = get_paid_by(id)
    paid_by.delete()
    return paid_by.get('status')


#### Settled ####
def create_settled(create_dict:dict) -> Settled:
    if not check_type_requirements('settled', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_settled = Settled('create', create_dict)
    return new_settled

def get_settled(id:str) -> Settled:
    settled = Settled('find', {'_key':id})
    return settled

def update_settled(id:str, update_dict:dict, user_updated='native') -> Settled:
    settled = get_settled(id)
    update_dict['_key'] = settled.get('_key')
    update_dict['user_updated'] = user_updated
    updated_settled = Settled('update', update_dict)
    return updated_settled

def delete_settled(id:str) -> bool:
    settled = get_settled(id)
    settled.delete()
    return settled.get('status')


#### Checkout ####
def create_checkout(create_dict:dict) -> Checkout:
    if not check_type_requirements('checkout', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_checkout = Checkout('create', create_dict)
    return new_checkout

def get_checkout(id:str) -> Checkout:
    checkout = Checkout('find', {'_key':id})
    return checkout

def update_checkout(id:str, update_dict:dict, user_updated='native') -> Checkout:
    checkout = get_checkout(id)
    update_dict['_key'] = checkout.get('_key')
    update_dict['user_updated'] = user_updated
    updated_checkout = Checkout('update', update_dict)
    return updated_checkout

def delete_checkout(id:str) -> bool:
    checkout = get_checkout(id)
    checkout.delete()
    return checkout.get('status')

class Payment():
    if os.environ.get('D20_EC_CONF') != None:
        conf = json.loads(os.environ.get('D20_EC_CONF'))
        arangoURL=conf.get('D20_EC_DBURL')
        username=conf.get('D20_EC_DBUSERNAME')
        password=conf.get('D20_EC_DBPASSWORD')
        db_name=conf.get('D20_EC_DBNAME')        
    else:
        raise MissingConfigurationException

    db_client = Connection(arangoURL=arangoURL, username=username, password=password, verify=True, verbose=True, statsdClient=None, reportFileName=None, loadBalancing='round-robin', use_grequests=False, use_jwt_authentication=False, use_lock_for_reseting_jwt=True, max_retries=10)



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

    db_collections = ['PaymentMethods','Charges','Payments']
    db_edges = ['PaysWith','PaidBy','Settled','Checkout']


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
        if not self.db.hasGraph('paymentsgraph'):
            self.db.createGraph('paymentsgraph')





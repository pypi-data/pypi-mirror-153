from pyArango.connection import *
from pyArango.collection import *
from pyArango.graph import *
from dtwentyORM import Metadata, Element
from dtwentyCommunications import *
from Classes import DeliveredBy, Delivery, DeliveryRule, AppliesTo, SentBy, SentTo
from .tools import *
from .Error import *
import pyArango
import os
import json


#### Collection CRUD ####

#### Delivery ####
def create_delivery(create_dict:dict) -> Delivery:
    if not check_type_requirements('delivery', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_delivery = Delivery('create', create_dict)
    return new_delivery

def get_delivery(id:str) -> Delivery:
    delivery = Delivery('find', {'_key':id})
    return delivery

def update_delivery(id:str, update_dict:dict, user_updated='native') -> Delivery:
    delivery = get_delivery(id)
    update_dict['_key'] = delivery.get('_key')
    update_dict['user_updated'] = user_updated
    updated_delivery = Delivery('update', update_dict)
    return updated_delivery

def delete_delivery(id:str) -> bool:
    delivery = get_delivery(id)
    delivery.delete()
    return delivery.get('status')



#### DeliveryRule ####
def create_delivery_rule(create_dict:dict) -> DeliveryRule:
    if not check_type_requirements('deliveryrule', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_delivery_rule = DeliveryRule('create', create_dict)
    return new_delivery_rule

def get_delivery_rule(id:str) -> DeliveryRule:
    delivery_rule = DeliveryRule('find', {'_key':id})
    return delivery_rule

def update_delivery_rule(id:str, update_dict:dict, user_updated='native') -> DeliveryRule:
    delivery_rule = get_delivery_rule(id)
    update_dict['_key'] = delivery_rule.get('_key')
    update_dict['user_updated'] = user_updated
    updated_delivery_rule = DeliveryRule('update', update_dict)
    return updated_delivery_rule

def delete_delivery_rule(id:str) -> bool:
    delivery_rule = get_delivery_rule(id)
    delivery_rule.delete()
    return delivery_rule.get('status')



#### DeliveredBy ####
def create_delivered_by(create_dict:dict) -> DeliveredBy:
    if not check_type_requirements('deliveredby', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_delivered_by = DeliveredBy('create', create_dict)
    return new_delivered_by

def get_delivered_by(id:str) -> DeliveredBy:
    delivered_by = DeliveredBy('find', {'_key':id})
    return delivered_by

def update_delivered_by(id:str, update_dict:dict, user_updated='native') -> DeliveredBy:
    delivered_by = get_delivered_by(id)
    update_dict['_key'] = delivered_by.get('_key')
    update_dict['user_updated'] = user_updated
    updated_delivered_by = DeliveredBy('update', update_dict)
    return updated_delivered_by

def delete_delivered_by(id:str) -> bool:
    delivered_by = get_delivered_by(id)
    delivered_by.delete()
    return delivered_by.get('status')



#### SentBy ####
def create_sent_by(create_dict:dict) -> SentBy:
    if not check_type_requirements('sentby', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_sent_by = SentBy('create', create_dict)
    return new_sent_by

def get_sent_by(id:str) -> SentBy:
    sent_by = SentBy('find', {'_key':id})
    return sent_by

def update_sent_by(id:str, update_dict:dict, user_updated='native') -> SentBy:
    sent_by = get_sent_by(id)
    update_dict['_key'] = sent_by.get('_key')
    update_dict['user_updated'] = user_updated
    updated_sent_by = SentBy('update', update_dict)
    return updated_sent_by

def delete_sent_by(id:str) -> bool:
    sent_by = get_sent_by(id)
    sent_by.delete()
    return sent_by.get('status')



#### SentTo ####
def create_sent_to(create_dict:dict) -> SentTo:
    if not check_type_requirements('sentto', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_sent_to = SentTo('create', create_dict)
    return new_sent_to

def get_sent_to(id:str) -> SentTo:
    sent_to = SentTo('find', {'_key':id})
    return sent_to

def update_sent_to(id:str, update_dict:dict, user_updated='native') -> SentTo:
    sent_to = get_sent_to(id)
    update_dict['_key'] = sent_to.get('_key')
    update_dict['user_updated'] = user_updated
    updated_sent_to = SentTo('update', update_dict)
    return updated_sent_to

def delete_sent_to(id:str) -> bool:
    sent_to = get_sent_to(id)
    sent_to.delete()
    return sent_to.get('status')



#### AppliesTo ####
def create_applies_to(create_dict:dict) -> AppliesTo:
    if not check_type_requirements('appliesto', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_applies_to = AppliesTo('create', create_dict)
    return new_applies_to

def get_applies_to(id:str) -> AppliesTo:
    applies_to = AppliesTo('find', {'_key':id})
    return applies_to

def update_applies_to(id:str, update_dict:dict, user_updated='native') -> AppliesTo:
    applies_to = get_applies_to(id)
    update_dict['_key'] = applies_to.get('_key')
    update_dict['user_updated'] = user_updated
    updated_applies_to = AppliesTo('update', update_dict)
    return updated_applies_to

def delete_applies_to(id:str) -> bool:
    applies_to = get_applies_to(id)
    applies_to.delete()
    return applies_to.get('status')


class Shipping():
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

    db_collections = ['Deliveries', 'DeliveryRules']
    db_edges = ['DeliveredBy', 'SentBy', 'SentTo', 'AppliesTo']


    class deliveriesgraph(pyArango.graph.Graph):
        _edgeDefinitions = (pyArango.graph.EdgeDefinition ('DeliveredBy',
                                        fromCollections = ['Orders'],
                                        toCollections = ['Deliveries']),
                            pyArango.graph.EdgeDefinition ('SentBy',
                                        fromCollections = ['Deliveries'],
                                        toCollections = ['Vendors']),
                            pyArango.graph.EdgeDefinition ('SentTo',
                                        fromCollections = ['Deliveries'],
                                        toCollections = ['Addresses']),
                            pyArango.graph.EdgeDefinition ('AppliesTo',
                                        fromCollections = ['DeliveryRules'],
                                        toCollections = ['Stock']),
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
        if not self.db.hasGraph('deliveriesgraph'):
            self.db.createGraph('deliveriesgraph')



from pyArango.connection import *
from pyArango.collection import *
from pyArango.graph import *

from arangodb_python_orm.src.dtwentyORM.Error import MissingRequiredParamatersException

from .tools import *
from .Error import *
import pyArango
import os
import json
from Classes import User, Address, TaxProfile, ReceivesAt, InvoiceAt, TaxAddress


#### Collection CRUD ####
#### User ####
def create_user(create_dict:dict) -> User:
    if not check_type_requirements('user', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_user = User('create', create_dict)
    return new_user

def get_user(id:str) -> User:
    user = User('find', {'_key':id})
    return user
    
def update_user(id:str, update_dict:dict, user_updated='native') -> User:
    user = get_user(id)
    update_dict['_key'] = user.get('_key')
    update_dict['user_updated'] = user_updated
    updated_user = User('update', update_dict) 
    return updated_user
    
def delete_user(id:str) -> bool:
    user = get_user(id)
    user.delete()
    return user.get('status')
    

#### Address ####
def create_address(create_dict:dict) -> Address:
    if not check_type_requirements('address', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_address = Address('create', create_dict)
    return new_address

def get_address(id:str) -> Address:
    address = Address('find', {'_key':id})
    return address
    
def update_address(id:str, update_dict:dict, user_updated='native') -> Address:
    address = get_address(id)
    update_dict['_key'] = address.get('_key')
    update_dict['user_updated'] = user_updated
    updated_address = Address('update', update_dict) 
    return updated_address
    
def delete_address(id:str) -> bool:
    address = get_address(id)
    address.delete()
    return address.get('status')
    

#### TaxProfile ####
def create_tax_profile(create_dict:dict) -> TaxProfile:
    if not check_type_requirements('taxprofile', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_tax_profile = TaxProfile('create', create_dict)
    return new_tax_profile

def get_tax_profile(id:str) -> TaxProfile:
    tax_profile = TaxProfile('find', {'_key':id})
    return tax_profile
    
def update_tax_profile(id:str, update_dict:dict, user_updated='native') -> TaxProfile:
    tax_profile = get_tax_profile(id)
    update_dict['_key'] = tax_profile.get('_key')
    update_dict['user_updated'] = user_updated
    updated_tax_profile = TaxProfile('update', update_dict) 
    return updated_tax_profile
    
def delete_tax_profile(id:str) -> bool:
    tax_profile = get_tax_profile(id)
    tax_profile.delete()
    return tax_profile.get('status')

#### ReceivesAt ####
def create_receives_at(create_dict:dict) -> ReceivesAt:
    if not check_type_requirements('receivesat', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_receives_at = ReceivesAt('create', create_dict)
    return new_receives_at

def get_receives_at(id:str) -> ReceivesAt:
    receives_at = ReceivesAt('find', {'_key':id})
    return receives_at
    
def update_receives_at(id:str, update_dict:dict, user_updated='native') -> ReceivesAt:
    receives_at = get_receives_at(id)
    update_dict['_key'] = receives_at.get('_key')
    update_dict['user_updated'] = user_updated
    updated_receives_at = ReceivesAt('update', update_dict) 
    return updated_receives_at
    
def delete_receives_at(id:str) -> bool:
    receives_at = get_receives_at(id)
    receives_at.delete()
    return receives_at.get('status')

#### TaxAddress ####
def create_tax_address(create_dict:dict) -> TaxAddress:
    if not check_type_requirements('taxaddress', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_tax_address = TaxAddress('create', create_dict)
    return new_tax_address

def get_tax_address(id:str) -> TaxAddress:
    tax_address = TaxAddress('find', {'_key':id})
    return tax_address
    
def update_tax_address(id:str, update_dict:dict, user_updated='native') -> TaxAddress:
    tax_address = get_tax_address(id)
    update_dict['_key'] = tax_address.get('_key')
    update_dict['user_updated'] = user_updated
    updated_tax_address = TaxAddress('update', update_dict) 
    return updated_tax_address
    
def delete_tax_address(id:str) -> bool:
    tax_address = get_tax_address(id)
    tax_address.delete()
    return tax_address.get('status')

#### InvoiceAt ####
def create_invoice_at(create_dict:dict) -> InvoiceAt:
    if not check_type_requirements('invoiceat', create_dict):
        raise MissingRequiredParamatersException
    create_dict.pop('_key', None)
    new_invoice_at = InvoiceAt('create', create_dict)
    return new_invoice_at

def get_invoice_at(id:str) -> InvoiceAt:
    invoice_at = InvoiceAt('find', {'_key':id})
    return invoice_at
    
def update_invoice_at(id:str, update_dict:dict, user_updated='native') -> InvoiceAt:
    invoice_at = get_invoice_at(id)
    update_dict['_key'] = invoice_at.get('_key')
    update_dict['user_updated'] = user_updated
    updated_invoice_at = InvoiceAt('update', update_dict) 
    return updated_invoice_at
    
def delete_invoice_at(id:str) -> bool:
    invoice_at = get_invoice_at(id)
    invoice_at.delete()
    return invoice_at.get('status')


#### Context Generator ####
class User():
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

    db_collections = ['TaxProfiles','Addresses','Users']
    db_edges = ['ReceivesAt', 'InvoiceAt', 'TaxAddress']


    class usergraph(pyArango.graph.Graph):
        _edgeDefinitions = (pyArango.graph.EdgeDefinition ('ReceivesAt',
                                        fromCollections = ['Users'],
                                        toCollections = ['Addresses']),
                            pyArango.graph.EdgeDefinition ('InvoiceAt',
                                        fromCollections = ['Users'],
                                        toCollections = ['TaxProfiles']),
                            pyArango.graph.EdgeDefinition ('TaxAddress',
                                        fromCollections = ['TaxProfiles'],
                                        toCollections = ['Addresses']),
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
        if not self.db.hasGraph('usergraph'):
            self.db.createGraph('usergraph')



from .Element import Element
from ..Error import *

class TaxAddress(Element):

    @classmethod
    def get_collection(cls):
        return 'TaxAddress'

    def get_class(self):
        return 'Tax_address'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'TaxProfiles', '_to': 'Addresses'}
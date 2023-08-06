from .Element import Element
from ..Error import *

class InvoiceAt(Element):

    @classmethod
    def get_collection(cls):
        return 'InvoiceAt'

    def get_class(self):
        return 'InvoiceAt'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Users', '_to': 'TaxProfiles'}
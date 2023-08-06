from .Element import Element
from ..Error import *

class Holds(Element):

    @classmethod
    def get_collection(cls):
        return 'Holds'

    def get_class(self):
        return 'Holds'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Vendors', '_to': 'Stock'}
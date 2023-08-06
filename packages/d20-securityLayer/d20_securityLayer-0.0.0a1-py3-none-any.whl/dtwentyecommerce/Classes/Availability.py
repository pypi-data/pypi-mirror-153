from .Element import Element
from ..Error import *

class Availability(Element):

    @classmethod
    def get_collection(cls):
        return 'Availability'

    def get_class(self):
        return 'Availability'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Products', '_to': 'Stock'}
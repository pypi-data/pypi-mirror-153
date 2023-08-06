from .Element import Element
from ..Error import *

class ToCart(Element):

    @classmethod
    def get_collection(cls):
        return 'ToCart'

    def get_class(self):
        return 'ToCart'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Queries', '_to': 'Carts'}
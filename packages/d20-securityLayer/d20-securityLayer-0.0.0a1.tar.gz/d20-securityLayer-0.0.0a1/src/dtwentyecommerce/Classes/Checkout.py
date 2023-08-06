from .Element import Element
from ..Error import *

class Checkout(Element):

    @classmethod
    def get_collection(cls):
        return 'Checkout'

    def get_class(self):
        return 'Checkout'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Orders', '_to': 'Payments'}
from .Element import Element
from ..Error import *

class Purchased(Element):

    @classmethod
    def get_collection(cls):
        return 'Purchased'

    def get_class(self):
        return 'Purchased'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Users', '_to': 'Orders'}
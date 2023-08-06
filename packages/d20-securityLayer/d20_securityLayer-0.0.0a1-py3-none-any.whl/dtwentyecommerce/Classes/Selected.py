from .Element import Element
from ..Error import *

class Selected(Element):

    @classmethod
    def get_collection(cls):
        return 'Selected'

    def get_class(self):
        return 'Selected'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Users', '_to': 'Carts'}
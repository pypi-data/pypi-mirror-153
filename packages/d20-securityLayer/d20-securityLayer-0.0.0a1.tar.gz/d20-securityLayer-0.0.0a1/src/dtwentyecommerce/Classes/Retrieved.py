from .Element import Element
from ..Error import *

class Retrieved(Element):

    @classmethod
    def get_collection(cls):
        return 'Retrieved'

    def get_class(self):
        return 'Retrieved'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Queries', '_to': 'Products'}
from .Element import Element
from ..Error import *

class Stock(Element):

    @classmethod
    def get_collection(cls):
        return 'Stock'

    def get_class(self):
        return 'Stock'
    
    def isEdge(self):
        return False
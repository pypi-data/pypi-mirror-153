from .Element import Element
from ..Error import *

class Price(Element):

    @classmethod
    def get_collection(cls):
        return 'Prices'

    def get_class(self):
        return 'Price'
    
    def isEdge(self):
        return False
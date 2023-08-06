from .Element import Element
from ..Error import *

class Vendor(Element):

    @classmethod
    def get_collection(cls):
        return 'Vendors'

    def get_class(self):
        return 'Vendor'
    
    def isEdge(self):
        return False
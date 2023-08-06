from .Element import Element
from ..Error import *

class Delivery(Element):

    @classmethod
    def get_collection(cls):
        return 'Deliveries'

    def get_class(self):
        return 'Delivery'
    
    def isEdge(self):
        return False
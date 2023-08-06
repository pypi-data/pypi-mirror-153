from .Element import Element
from ..Error import *

class DeliveryRule(Element):

    @classmethod
    def get_collection(cls):
        return 'DeliveryRules'

    def get_class(self):
        return 'DeliveryRule'
    
    def isEdge(self):
        return False
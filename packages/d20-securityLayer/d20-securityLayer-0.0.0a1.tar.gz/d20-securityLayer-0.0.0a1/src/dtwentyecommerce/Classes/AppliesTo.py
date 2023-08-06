from .Element import Element
from ..Error import *

class AppliesTo(Element):

    @classmethod
    def get_collection(cls):
        return 'AppliesTo'

    def get_class(self):
        return 'AppliesTo'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'DeliveryRules', '_to': 'Stock'}
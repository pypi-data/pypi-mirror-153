from .Element import Element
from ..Error import *

class Payment(Element):

    @classmethod
    def get_collection(cls):
        return 'Payments'

    def get_class(self):
        return 'Payment'
    
    def isEdge(self):
        return False
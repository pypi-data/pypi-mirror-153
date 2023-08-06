from .Element import Element
from ..Error import *

class PaymentMethod(Element):

    @classmethod
    def get_collection(cls):
        return 'PaymentMethods'

    def get_class(self):
        return 'PaymentMethod'
    
    def isEdge(self):
        return False
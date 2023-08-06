from .Element import Element
from ..Error import *

class PaidBy(Element):

    @classmethod
    def get_collection(cls):
        return 'PaidBy'

    def get_class(self):
        return 'PaidBy'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Charges', '_to': 'PaymentMethods'}
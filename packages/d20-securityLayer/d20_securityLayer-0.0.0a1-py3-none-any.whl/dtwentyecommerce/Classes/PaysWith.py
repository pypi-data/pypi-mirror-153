from .Element import Element
from ..Error import *

class PaysWith(Element):

    @classmethod
    def get_collection(cls):
        return 'PaysWith'

    def get_class(self):
        return 'PaysWith'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Users', '_to': 'PaymentMethods'}
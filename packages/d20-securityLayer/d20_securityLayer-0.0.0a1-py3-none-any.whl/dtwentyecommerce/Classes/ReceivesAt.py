from .Element import Element
from ..Error import *

class ReceivesAt(Element):

    @classmethod
    def get_collection(cls):
        return 'ReceivesAt'

    def get_class(self):
        return 'ReceivesAt'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Users', '_to': 'Addresses'}
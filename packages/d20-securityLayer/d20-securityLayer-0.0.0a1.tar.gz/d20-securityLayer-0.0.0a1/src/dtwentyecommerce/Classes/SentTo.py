from .Element import Element
from ..Error import *

class SentTo(Element):

    @classmethod
    def get_collection(cls):
        return 'SentTo'

    def get_class(self):
        return 'SentTo'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Deliveries', '_to': 'Addresses'}
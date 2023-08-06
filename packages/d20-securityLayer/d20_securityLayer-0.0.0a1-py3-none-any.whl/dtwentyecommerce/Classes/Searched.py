from .Element import Element
from ..Error import *

class Searched(Element):

    @classmethod
    def get_collection(cls):
        return 'Searched'

    def get_class(self):
        return 'Searched'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Users', '_to': 'Queries'}
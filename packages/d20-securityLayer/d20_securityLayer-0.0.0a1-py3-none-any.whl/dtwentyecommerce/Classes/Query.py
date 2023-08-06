from .Element import Element
from ..Error import *

class Query(Element):

    @classmethod
    def get_collection(cls):
        return 'Queries'

    def get_class(self):
        return 'Query'
    
    def isEdge(self):
        return False
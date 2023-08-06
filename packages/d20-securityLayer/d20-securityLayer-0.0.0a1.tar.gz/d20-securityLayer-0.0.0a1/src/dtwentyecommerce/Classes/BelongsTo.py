from .Element import Element
from ..Error import *

class BelongsTo(Element):

    @classmethod
    def get_collection(cls):
        return 'BelongsTo'

    def get_class(self):
        return 'BelongsTo'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Products', '_to': 'Categories'}
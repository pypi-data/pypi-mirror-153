from .Element import Element
from ..Error import *

class Category(Element):

    @classmethod
    def get_collection(cls):
        return 'Categories'

    def get_class(self):
        return 'Category'
    
    def isEdge(self):
        return False
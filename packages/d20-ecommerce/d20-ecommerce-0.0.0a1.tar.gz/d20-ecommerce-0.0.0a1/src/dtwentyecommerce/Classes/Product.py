from .Element import Element
from ..Error import *

class Product(Element):

    @classmethod
    def get_collection(cls):
        return 'Products'

    def get_class(self):
        return 'Product'
    
    def isEdge(self):
        return False
from .Element import Element
from ..Error import *

class Cart(Element):

    @classmethod
    def get_collection(cls):
        return 'Carts'

    def get_class(self):
        return 'Cart'
    
    def isEdge(self):
        return False
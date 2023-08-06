from .Element import Element
from ..Error import *

class CartContains(Element):

    @classmethod
    def get_collection(cls):
        return 'CartContains'

    def get_class(self):
        return 'CartContains'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Carts', '_to': 'Products'}
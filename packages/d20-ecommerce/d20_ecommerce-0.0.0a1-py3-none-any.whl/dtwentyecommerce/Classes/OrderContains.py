from .Element import Element
from ..Error import *

class OrderContains(Element):

    @classmethod
    def get_collection(cls):
        return 'OrderContains'

    def get_class(self):
        return 'OrderContains'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Orders', '_to': 'Products'}
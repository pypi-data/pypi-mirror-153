from .Element import Element
from ..Error import *

class Order(Element):

    @classmethod
    def get_collection(cls):
        return 'Orders'

    def get_class(self):
        return 'Order'
    
    def isEdge(self):
        return False
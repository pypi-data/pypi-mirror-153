from .Element import Element
from ..Error import *

class Address(Element):

    @classmethod
    def get_collection(cls):
        return 'Addresses'

    def get_class(self):
        return 'Address'
    
    def isEdge(self):
        return False
from .Element import Element
from ..Error import *

class Brand(Element):

    @classmethod
    def get_collection(cls):
        return 'Brands'

    def get_class(self):
        return 'Brand'
    
    def isEdge(self):
        return False
from .Element import Element
from ..Error import *

class Makes(Element):

    @classmethod
    def get_collection(cls):
        return 'Makes'

    def get_class(self):
        return 'Makes'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Brands', '_to': 'Products'}
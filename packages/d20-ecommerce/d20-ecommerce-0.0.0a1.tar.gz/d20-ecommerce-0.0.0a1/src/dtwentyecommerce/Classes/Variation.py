from .Element import Element
from ..Error import *

class Variation(Element):

    @classmethod
    def get_collection(cls):
        return 'Variation'

    def get_class(self):
        return 'Variation'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Products', '_to': 'Products'}
from .Element import Element
from ..Error import *

class SellsFor(Element):

    @classmethod
    def get_collection(cls):
        return 'SellsFor'

    def get_class(self):
        return 'SellsFor'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Products', '_to': 'Prices'}
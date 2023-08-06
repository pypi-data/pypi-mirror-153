from .Element import Element
from ..Error import *

class Included(Element):

    @classmethod
    def get_collection(cls):
        return 'Included'

    def get_class(self):
        return 'Included'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Queries', '_to': ['Products', 'Brands', 'Categories', 'Promotions']}
from .Element import Element
from ..Error import *

class IncludesPromo(Element):

    @classmethod
    def get_collection(cls):
        return 'IncludesPromo'

    def get_class(self):
        return 'IncludesPromo'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Products', '_to': 'Promotions'}
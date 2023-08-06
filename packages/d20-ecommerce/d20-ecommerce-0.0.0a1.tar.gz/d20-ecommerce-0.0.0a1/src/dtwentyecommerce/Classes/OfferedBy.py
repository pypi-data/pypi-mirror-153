from .Element import Element
from ..Error import *

class OfferedBy(Element):

    @classmethod
    def get_collection(cls):
        return 'OfferedBy'

    def get_class(self):
        return 'OfferedBy'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Products', '_to': 'Vendors'}
from .Element import Element
from ..Error import *

class LocatedAt(Element):

    @classmethod
    def get_collection(cls):
        return 'LocatedAt'

    def get_class(self):
        return 'LocatedAt'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Vendors', '_to': 'Addresses'}
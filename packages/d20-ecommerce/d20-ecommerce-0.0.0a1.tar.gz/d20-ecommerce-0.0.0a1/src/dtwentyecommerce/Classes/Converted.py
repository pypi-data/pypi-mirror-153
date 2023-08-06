from .Element import Element
from ..Error import *

class Converted(Element):

    @classmethod
    def get_collection(cls):
        return 'Converted'

    def get_class(self):
        return 'Converted'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Carts', '_to': 'Orders'}
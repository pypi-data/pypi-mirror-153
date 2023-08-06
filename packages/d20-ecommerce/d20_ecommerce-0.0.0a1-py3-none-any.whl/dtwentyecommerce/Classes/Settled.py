from .Element import Element
from ..Error import *

class Settled(Element):

    @classmethod
    def get_collection(cls):
        return 'Settled'

    def get_class(self):
        return 'Settled'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Charges', '_to': 'Payments'}
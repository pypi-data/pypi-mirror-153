from .Element import Element
from ..Error import *

class Charge(Element):

    @classmethod
    def get_collection(cls):
        return 'Charges'

    def get_class(self):
        return 'Charge'
    
    def isEdge(self):
        return False
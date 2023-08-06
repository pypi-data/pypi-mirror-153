from .Element import Element
from ..Error import *

class Promotion(Element):

    @classmethod
    def get_collection(cls):
        return 'Promotions'

    def get_class(self):
        return 'Promotion'
    
    def isEdge(self):
        return False
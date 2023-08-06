from .Element import Element
from ..Error import *

class SentBy(Element):

    @classmethod
    def get_collection(cls):
        return 'SentBy'

    def get_class(self):
        return 'SentBy'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Deliveries', '_to': 'Vendors'}
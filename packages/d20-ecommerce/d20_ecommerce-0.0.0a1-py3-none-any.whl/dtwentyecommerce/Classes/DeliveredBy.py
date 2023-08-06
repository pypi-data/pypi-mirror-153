from .Element import Element
from ..Error import *

class DeliveredBy(Element):

    @classmethod
    def get_collection(cls):
        return 'DeliveredBy'

    def get_class(self):
        return 'DeliveredBy'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Orders', '_to': 'Deliveries'}
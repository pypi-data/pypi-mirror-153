from .Element import Element
from ..Error import *

class Invoice(Element):

    @classmethod
    def get_collection(cls):
        return 'Invoices'

    def get_class(self):
        return 'Invoice'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Orders', '_to': 'TaxProfiles'}
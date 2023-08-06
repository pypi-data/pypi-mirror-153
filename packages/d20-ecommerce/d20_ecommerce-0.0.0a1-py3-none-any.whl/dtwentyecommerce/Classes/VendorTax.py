from .Element import Element
from ..Error import *

class VendorTax(Element):

    @classmethod
    def get_collection(cls):
        return 'VendorTax'

    def get_class(self):
        return 'VendorTax'
    
    def isEdge(self):
        return True

    def vertex(self):
        return {'_from': 'Vendors', '_to': 'TaxProfiles'}
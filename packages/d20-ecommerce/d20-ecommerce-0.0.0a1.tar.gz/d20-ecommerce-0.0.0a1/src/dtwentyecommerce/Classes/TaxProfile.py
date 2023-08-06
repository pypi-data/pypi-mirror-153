from .Element import Element
from ..Error import *

class TaxProfile(Element):

    @classmethod
    def get_collection(cls):
        return 'TaxProfiles'

    def get_class(self):
        return 'TaxProfile'
    
    def isEdge(self):
        return False
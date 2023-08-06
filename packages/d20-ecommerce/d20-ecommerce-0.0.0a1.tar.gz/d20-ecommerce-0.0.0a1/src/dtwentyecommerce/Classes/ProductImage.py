from .File import File
from ..Error import *

class ProductImage(File):

    @classmethod
    def get_collection(cls):
        return 'ProductImages'

    def get_class(self):
        return 'ProductImage'
    
    def isEdge(self):
        return False
from dtwentyORM import Element as ORM_Element
from ..Error import *
import os
import json

class Element(ORM_Element):
    def __init__(self, mode = None, data = None, multi = False, conf=None, prefix='D20_EC'):
        if os.environ.get(f'{prefix}_CONF') != None and conf == None:
            conf = json.loads(os.environ.get(f'{prefix}_CONF'))
        else:
            raise MissingConfigurationException
        self.db_name=conf.get('DBNAME')
        super().__init__(self, mode = mode, data = data, multi = multi) 
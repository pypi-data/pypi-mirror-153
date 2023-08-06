from dtwentyORM import Metadata, Element

def check_requirements(requirements:list, object:dict) -> bool:
    return False not in [e in object for e in requirements]

def check_type_requirements(type:str, object:dict) -> bool:
    df = Metadata.DataField('set', {'obj_type':type.lower(), 'active': True, 'deleted': False, 'required': True})
    df.get_all()
    dfa = df.get('datafields')
    requirements = [f.get('name') for f in dfa]
    return check_requirements(requirements, object)
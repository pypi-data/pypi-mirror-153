types = [
    {
        'class_name':'Brand',
        'obj_name':'brand',
        'col_name':'brand'
    },
    {
        'class_name':'Category',
        'obj_name':'category',
        'col_name':'category'
    },
    {
        'class_name':'Price',
        'obj_name':'price',
        'col_name':'price'
    },
    {
        'class_name':'Product',
        'obj_name':'product',
        'col_name':'product'
    },
    {
        'class_name':'Promotion',
        'obj_name':'promotion',
        'col_name':'promotion'
    },
    {
        'class_name':'Vendor',
        'obj_name':'vendor',
        'col_name':'vendor'
    },
    {
        'class_name':'Stock',
        'obj_name':'stock',
        'col_name':'stock'
    },
    {
        'class_name':'IncludesPromo',
        'obj_name':'includes_promo',
        'col_name':'includespromo'
    },
    {
        'class_name':'Availability',
        'obj_name':'availability',
        'col_name':'availability'
    },
    {
        'class_name':'BelongsTo',
        'obj_name':'belongs_to',
        'col_name':'belongsto'
    },
    {
        'class_name':'SellsFor',
        'obj_name':'sells_for',
        'col_name':'sellsfor'
    },
    {
        'class_name':'Makes',
        'obj_name':'makes',
        'col_name':'makes'
    },
    {
        'class_name':'OfferedBy',
        'obj_name':'offered_by',
        'col_name':'offeredby'
    },
    {
        'class_name':'Holds',
        'obj_name':'holds',
        'col_name':'holds'
    },
    {
        'class_name':'LocatedAt',
        'obj_name':'located_at',
        'col_name':'locatedat'
    },
]

for type in types:
    class_name = type['class_name']
    obj_name = type['obj_name']
    col_name = type['col_name']
    print(f"\n\
#### {class_name} #### \n\
def create_{obj_name}(create_dict:dict) -> {class_name}: \n\
    if not check_type_requirements('{col_name}', create_dict): \n\
        raise MissingRequiredParamatersException \n\
    create_dict.pop('_key', None) \n\
    new_{obj_name} = {class_name}('create', create_dict) \n\
    return new_{obj_name} \n\n\
def get_{obj_name}(id:str) -> {class_name}: \n\
    {obj_name} = {class_name}('find', {{'_key':id}}) \n\
    return {obj_name} \n\n\
def update_{obj_name}(id:str, update_dict:dict, user_updated='native') -> {class_name}: \n\
    {obj_name} = get_{obj_name}(id) \n\
    update_dict['_key'] = {obj_name}.get('_key') \n\
    update_dict['user_updated'] = user_updated \n\
    updated_{obj_name} = {class_name}('update', update_dict) \n\
    return updated_{obj_name} \n\n\
def delete_{obj_name}(id:str) -> bool: \n\
    {obj_name} = get_{obj_name}(id) \n\
    {obj_name}.delete() \n\
    return {obj_name}.get('status') \n\n\
")
def check_field(dict_body, key, required=True):
    if key not in dict_body:
        if required:
            raise ValueError('Required field does not exist')
        else:
            return None
    else:
        return dict_body[key]

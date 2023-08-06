def check_field(dict_body, key, required=True):
    if key not in dict_body:
        if required:
            raise ValueError(f'Required field does not exist : {key}')
        else:
            return None
    else:
        return dict_body[key]

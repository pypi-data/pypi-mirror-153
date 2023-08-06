def check_field(dict_body, key, default=None, required=True):
    if key not in dict_body:
        if required:
            raise ValueError(f'Required field does not exist : {key}')
        else:
            return default
    else:
        return dict_body[key]

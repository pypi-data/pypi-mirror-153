def _class_attributes(class_object):

    return [attr for attr in class_object.__dir__() if not attr.startswith("_")]
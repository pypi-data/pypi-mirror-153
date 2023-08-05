'''
All custom exceptions raised in the project.
'''


class InvalidWidgetDefinition(ValueError):
    pass


class InvalidLayoutError(Exception):
    pass


class InvalidCallbackDefinition(Exception):
    def __init__(self, msg: str):
        self.msg = msg


class InvalidImageKey(Exception):
    def __init__(self, key: str):
        self.key = key


class InvalidImageType(Exception):
    def __init__(self, dtype: str):
        self.dtype = dtype

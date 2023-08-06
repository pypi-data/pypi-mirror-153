__author__ = 'Andrey Komissarov'
__date__ = '2022'


class ServiceLookupError(BaseException):
    def __init__(self, name: str = None):
        self.name = name or 'name is not specified by user'

    def __str__(self):
        return f'Service ({self.name}) not found!'

__author__ = 'Andrey Komissarov'
__date__ = '2022'


class PackageNotFoundError(BaseException):
    def __init__(self, package: str = None):
        self.package = package or 'name is not specified by user'

    def __str__(self):
        return f'Package ({self.package}) not found!'

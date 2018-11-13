import abc

class AutoStorage(abc.ABC):
    
    __counter = 0

    def __init__(self):
        cls = self.__class__
        prefix = cls.__name__
        index = cls.__counter
        self.storage_name = '_{}#{}'.format(prefix, index)
        cls.__counter += 1

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)
    '''
    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)

    '''

    def __set__(self, instance , value):
        #value = self.validated(instance, value)
        value = self.validated(value)
        setattr(instance, self.storage_name, value)
        #super().__set__(instance, value)

    @abc.abstractmethod
    #def validated(self, instance, value):
    def validated(self, value):
        '''return validated value or raise ValueError'''


class Quantity(AutoStorage):

    #def validated(self, instance, value):
    def validated(self, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value

class NonBlank(AutoStorage):
    #def validated(self, instance, value):
    def validated(self, value):
        if len(value.strip()) == 0:
            raise ValueError('value cannot be empty or blank')
        return value

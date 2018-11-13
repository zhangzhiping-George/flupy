import abc
import collections

class AutoStorage:
    
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

    def __set__(self, instance, value):
        setattr(instance, self.storage_name, value)

class Validated(abc.ABC, AutoStorage):

    def __set__(self, instance , value):
        value = self.validated(instance, value)
        super().__set__(instance, value)

    @abc.abstractmethod
    def validated(self, instance, value):
        '''return validated value or raise ValueError'''


class Quantity(Validated):

    def validated(self, instance, value):
        if value <= 0:
            raise ValueError('value must be > 0')
        return value

class NonBlank(Validated):
    def validated(self, instance, value):
        if len(value.strip()) == 0:
            raise ValueError('value cannot be empty or blank')
        return value
'''
class LineItem(Entity):
    desc = model.NonBlank()
    weight = model.Quantity()
    price = model.Quantity()
    def __init__(self, desc, weight, price):
         
'''

class EntityMeta(type):
    def __prepare__(cls, name, bases):
        return collections.OrderedDict()
    def __init__(cls, name, bases, attr_dict):
        super().__init__(name, bases, attr_dict)
        cls._field_names = []
        for key, attrs in cls.__dict__.items():
            if isinstance(attrs, Validated):
                attrs.storage_name = '_{}#{}'.format(
                            type(attrs).__name__, key)
                cls._field_names.append(key)
class Entity(metaclass=EntityMeta):
    @classmethod
    def fields_name(cls):
        for name in cls._field_names:
            yield name


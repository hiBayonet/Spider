# -*- coding: utf-8 -*-
import numbers


class Field:
    pass


class ModelMetaBase(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        fields = {}
        for key, value in attrs.items():
            if isinstance(value, Field):
                fields[key] = value

        attrs_meta = attrs.get("Meta", None)
        _meta = {}
        db_table = name.lower()
        if attrs_meta is not None:
            table = getattr(attrs_meta, "db_table", None)
            del attrs['Meta']
            if table is not None:
                db_table = table

        _meta['db_table'] = db_table
        attrs['_meta'] = _meta
        attrs['fields'] = fields
        return super().__new__(cls, name, bases, attrs, **kwargs)


class IntField(Field):
    def __init__(self, db_column=None, min_value=None, max_value=None):
        self._value = None
        self.db_column = db_column
        self.min_value = min_value
        self.max_value = max_value

        if min_value is not None:
            if not isinstance(self.min_value, numbers.Integral):
                raise ValueError('min_value must be int')
            elif min_value < 0:
                raise ValueError('min_value must be positive int')

        if max_value is not None:
            if not isinstance(self.max_value, numbers.Integral):
                raise ValueError('max_value must be int')
            elif max_value < 0:
                raise ValueError('max_value must be positive int')

        if min_value is not None and max_value is not None:
            if min_value > max_value:
                raise ValueError('min_value must be smaller than max_value')

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if not isinstance(value, numbers.Integral):
            raise ValueError('int value need')

        if value < 0:
            raise ValueError('positive value need')

        if self.min_value is not None or self.max_value is not None:
            if self.min_value < value or self.max_value > value:
                raise ValueError('value must between min_value and max_value')
        self._value = value


class CharField(Field):
    def __init__(self, db_column=None, max_length=None):
        self.db_column = db_column
        self._value = None
        if max_length is None:
            raise ValueError('you must spcify max_length for CharField')
        self.max_length = max_length

    def __get__(self, instance, owner):
        return self._value

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError('string value need')

        if len(value) > self.max_length:
            raise ValueError('value len excess len of max_length')

        self._value = value


class BaseModel(metaclass=ModelMetaBase):
    def __init__(self, *args, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        super().__init__()

    def save(self):
        fields = []
        values = []
        for key, value in self.fields.items():
            db_column = value.db_column
            if db_column is None:
                db_column = key.lower()

            fields.append(db_column)
            value = getattr(self, key)
            values.append(str(value))

        sql = 'insert {db_table}({fields}) values(\'{values}\')'.format(db_table=self._meta['db_table'],
                                                                        fields=','.join(fields),
                                                                        values='\',\''.join(values))

        print(sql)

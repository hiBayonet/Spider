# -*- coding: utf-8 -*-
from db.orm import IntField, CharField, BaseModel


class User(BaseModel):
    name = CharField(max_length=20)
    age = IntField()

    class Meta:
        db_table = "user"


def test_orm():
    # user = User(name='bayonet', age=10)
    user = User()
    user.age = 10
    user.name = 'bayonet'
    user.save()


if __name__ == '__main__':
    test_orm()

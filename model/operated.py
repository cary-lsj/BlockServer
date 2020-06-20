# -*-coding:utf-8-*-
from orm.orm import Model, IntegerField, StringField


class User(Model):
    __table__ = 'operated'
    __primary_key__ = 'id'

    id = IntegerField('id', True)  # 操作id
    uid = IntegerField('uid', True)  # 谁操作的
    type = StringField('type', True)  # 操作类型
    time = StringField('time', True)  # 时间

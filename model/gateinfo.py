# -*-coding:utf-8-*-
from orm.orm import Model, IntegerField, StringField, FloatField


class Gateinfo(Model):
    __table__ = 'gateinfo'
    __primary_key__ = 'id'

    id = IntegerField('id', False)
    gid = IntegerField('gid', True)
    uid = StringField('uid', True)
    gatestar = IntegerField('gatestar', True)
    state = IntegerField('state', True)

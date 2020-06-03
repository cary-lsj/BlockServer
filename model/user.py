# -*-coding:utf-8-*-
from orm.orm import Model, IntegerField, StringField


class User(Model):
    __table__ = 'userinfo'
    __primary_key__ = 'id'

    id = StringField('id', True)
    nickname = StringField('nickname', True)
    headimgurl = StringField('headimgurl', True)
    sex = IntegerField('sex', True)
    city = StringField('city', True)
    country = StringField('country', True)
    province = StringField('province', True)
    unionid = StringField('unionid', True)
    tips = IntegerField('tips', True)
    gates = StringField('gates', True)
    dtips = IntegerField('dtips', True)
    ranklevel = IntegerField('ranklevel', True)
    gold = IntegerField('gold', True)
    money = IntegerField('money', True)
    goods = StringField('goods', True)

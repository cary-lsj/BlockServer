# -*-coding:utf-8-*-
from orm.orm import Model, IntegerField, StringField


class User(Model):
    __table__ = 'userinfo'
    __primary_key__ = 'id'

    id = IntegerField('id', False)
    username = StringField('username', True)
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
    tipstime = StringField('tipstime', True)  # 提示的时间
    ads = IntegerField('ads', True)  # 看视频广告次数
    adtime = StringField('adtime', True)  # 看视频广告时间
    shares = IntegerField('shares', True)  # 分享的次数
    sharetime = StringField('sharetime', True)  # 分享的时间
    popadds = IntegerField('popadds', True)  # 看弹出式广告次数
    popaddtime = StringField('popaddtime', True)  # 弹出式广告时间

    def getCanSeeVideoAD(self):
        if adtime == None:
            return True

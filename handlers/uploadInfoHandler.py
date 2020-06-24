# coding:utf-8

import json
import tornado.web
import time
import os

from configs.config_default import configs_default
from configs.config_game import config_game
from dal.dal_gateinfo import Dal_Gateinfo
from model.gateinfo import Gateinfo
from model.user import User
from dal.dal_user import Dal_User
from configs.config_error import config_error
from protobuf.errorcode_pb2 import ErrorCode
from tools.utils import Utils
from handlers.BaseHandler import BaseHandler
from protobuf import msg_pb2

import sys

reload(sys)
sys.setdefaultencoding("utf8")


class UploadInfoHandler(BaseHandler):
    def post(self):
        msgReq = msg_pb2.Msg()
        msgReq.ParseFromString(self.request.body)

        msgResp = msg_pb2.Msg()
        msgResp.type = msg_pb2.EnumMsg.Value('uploadinforequest')

        request = msgReq.request.uploadinforequest

        username = request.sID
        nickname = request.sNick
        headimgurl = request.sHeadimg
        sex = request.nGender
        country = request.sCountry
        province = request.sProvince
        city = request.sCity

        user = Dal_User().getLoginUser(username)
        if user:
            if nickname != "" and nickname != user.nickname:
                user.nickname = nickname
                kwargs = {"nickname": user.nickname}
                Dal_User().uqdateUser(user.id, **kwargs)
            if headimgurl != "" and headimgurl != user.headimgurl:
                user.headimgurl = headimgurl
                kwargs = {"headimgurl": user.headimgurl}
                Dal_User().uqdateUser(user.id, **kwargs)
            if sex != "" and sex != user.sex:
                user.sex = sex
                kwargs = {"sex": user.sex}
                Dal_User().uqdateUser(user.id, **kwargs)
            if city != "" and city != user.city:
                user.city = city
                kwargs = {"city": user.city}
                Dal_User().uqdateUser(user.id, **kwargs)
            if country != "" and country != user.country:
                user.country = country
                kwargs = {"country": user.country}
                Dal_User().uqdateUser(user.id, **kwargs)
            if province != "" and province != user.province:
                user.province = province
                kwargs = {"province": user.province}
                Dal_User().uqdateUser(user.id, **kwargs)




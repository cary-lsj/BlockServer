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


class LoginHandler(BaseHandler):
    def post(self):
        msgReq = msg_pb2.Msg()
        msgReq.ParseFromString(self.request.body)

        msgResp = msg_pb2.Msg()
        msgResp.type = msg_pb2.EnumMsg.Value('loginresponse')

        request = msgReq.request.loginRequest
        resp = msgResp.response.loginResponse
        username = request.sID
        nick = request.sNick
        headimg = request.sHeadimg
        gender = request.nGender
        country = request.sCountry
        province = request.sProvince
        city = request.sCity

        user = Dal_User().getLoginUser(username)
        if user == None:
            Utils().logDebug("创建新用户:" + str(nick) + " ; openid:" + str(username))
            # 新用户默认第一关解锁
            newgate = Gateinfo(gid=1, uid=username, gatestar=0, state=1)
            gid = Dal_Gateinfo().addGateinfo(newgate)
            nowtime = Utils().dbTimeCreate()
            user = User(id=None, username=username, nickname=nick, headimgurl=headimg, \
                        tips=0, gates=str(gid), sex=gender, city=city, country=country, province=province, \
                        unionid="", dtips=0, ranklevel=0, gold=0, money=0, goods="", tipstime=nowtime, ads=0, \
                        adtime=nowtime, shares=0, sharetime=nowtime, popadds=0, popaddtime=nowtime)
            Dal_User().addUser(user)

        if nick != "" and nick != user.nickname:
            user.nickname = nick
            kwargs = {"nickname": user.nickname}
            Dal_User().uqdateUser(user.id, **kwargs)

        if headimg != "" and headimg != user.headimgurl:
            user.headimgurl = headimg
            kwargs = {"headimgurl": headimg}
            Dal_User().uqdateUser(user.id, **kwargs)

        gates = Dal_User().getUserGates(user.id)
        for index, id in enumerate(gates):
            gate = resp.gates.add()
            gateinfo = Dal_Gateinfo().getGateinfo(id)
            gate.id = gateinfo.gid
            gate.starNum = gateinfo.gatestar

        resp.nServerTime = int(time.time())
        resp.requester.nUserID = user.id
        resp.requester.nSeeAdTimes = config_game['seeVideoAdTimes'] - user.ads
        resp.requester.nShareTimes = config_game['shareTimes'] - user.shares
        resp.requester.nGetTipsTimes = user.tips
        resp.requester.nPopaddsTimes = config_game['seePopAdTimes'] - user.popadds
        resp.requester.nGold = user.gold

        msgResp.response.nErrorCode = config_error['success']
        data = msgResp.SerializeToString()
        self.write(data)

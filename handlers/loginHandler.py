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
        uid = request.sID
        nick = request.sNick
        headimg = request.sHeadimg

        user = Dal_User().getUser(uid)
        if user == None:
            Utils().logDebug("创建新用户:"+str(nick)+" ; openid:"+str(uid))
            #新用户默认第一关解锁
            newgate = Gateinfo(gid=1, uid=uid, gatestar=0, state=1)
            gid = Dal_Gateinfo().addGateinfo(newgate)

            user = User(id=uid, nickname=nick, headimgurl=headimg, \
                    tips =0,gates = str(gid),sex=0,city="",country="",province="", \
                        unionid="",dtips=0,ranklevel=0,gold=0,money=0,goods="")
            Dal_User().addUser(user)

        if nick != "" and nick != user.nickname:
            user.nickname = nick
            kwargs = {"nick": user.nickname}
            Dal_User().uqdateUser(user.id, **kwargs)

        if headimg != "" and headimg != user.headimgurl:
            user.headimgurl = headimg
            kwargs = {"headimg": headimg}
            Dal_User().uqdateUser(user.id, **kwargs)

        gates = Dal_User().getUserGates(user.id)
        for index,id in enumerate(gates):
            gate = resp.gates.add()
            gateinfo = Dal_Gateinfo().getGateinfo(id)
            gate.id = gateinfo.gid
            gate.starNum = gateinfo.gatestar

        resp.nTotalStar = Dal_User().getUserTopGateStar(user.id)
        resp.nTotalGate = config_game['maxGate']

        msgResp.response.nErrorCode = config_error['success']
        data = msgResp.SerializeToString()
        self.write(data)

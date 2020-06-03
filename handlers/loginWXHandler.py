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

class LoginWXHandler(BaseHandler):
    def post(self):
        # msgReq = msg_pb2.Msg()
        # msgReq.ParseFromString(self.request.body)
        # 
        # msgResp = msg_pb2.Msg()
        # msgResp.type = msg_pb2.EnumMsg.Value('loginresponse')

        # request = msgReq.request.loginRequest
        # response = msgResp.response.loginResponse
        req = json.loads(self.request.body)

        resp = {}
        uid = req["request"]["sID"]
        nick = req["request"]["sNick"]
        headimg = req["request"]["sHeadimg"]

        user = Dal_User().getUser(uid)
        if user == None:
            resp['nErrorCode'] = config_error['success']
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

        resp['nErrorCode'] = config_error['success']
        resp['nUserID'] = user.id
        if user.nickname:
            resp['sNick'] = user.nickname
        if user.headimgurl:
            resp['sHeadimg'] = user.headimgurl
        if user.gold:
            resp['gold'] = user.gold
        if user.money:
            resp['money'] = user.money
        if user.goods:
            resp['goods'] = user.goods

        resp['gates'] = []
        gates = Dal_User().getUserGates(user.id)
        for index,id in enumerate(gates):
            gateinfo = Dal_Gateinfo().getGateinfo(id)
            resp['gates'].append(gateinfo)

        resp['nTotalStar'] = Dal_User().getUserTopGateStar(user.id)
        resp['nTotalGate'] = config_game['maxGate']

        msg={}
        msg["type"] = config_game['msgType']['loginresponse']
        msg["response"] = resp
        resp = json.dumps(msg)

        self.write(resp)

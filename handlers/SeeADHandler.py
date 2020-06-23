# -*- coding:utf-8 -*-
import json

from configs.config_default import configs_default
from configs.config_game import config_game
from dal.dal_user import Dal_User
from model.user import User
from dal.dal_gateinfo import Dal_Gateinfo
from configs.config_error import config_error
from protobuf.errorcode_pb2 import ErrorCode
from tools.utils import Utils
from handlers.BaseHandler import BaseHandler
from protobuf import play_begin_pb2, msg_pb2


class Adtype():
    seeAdGetGlod = 1  # 看视频广告得金币
    endseeAd = 2  # 结算看视频
    popadd = 3  # 弹窗广告
    share = 4  # 分享


class SeeADHandler(BaseHandler):
    def post(self):
        msgReq = msg_pb2.Msg()
        msgReq.ParseFromString(self.request.body)

        msgResp = msg_pb2.Msg()
        msgResp.type = msg_pb2.EnumMsg.Value('seeadresponse')

        request = msgReq.request.seeAdRequest
        response = msgResp.response.seeAdResponse
        response.nType = request.nType

        uid = request.nID
        user = Dal_User().getUser(uid)
        if user == None:
            msgResp.response.nErrorCode = config_error['userinvaild']
        else:
            msgResp.response.nErrorCode = config_error['success']
            if request.nType == Adtype.seeAdGetGlod:
                self.seeAdGetGlod(user, msgResp)
            elif request.nType == Adtype.endseeAd:
                self.endseeAd(user, msgResp, request.nGlod)
            elif request.nType == Adtype.popadd:
                self.popadd(user, msgResp)
            elif request.nType == Adtype.share:
                self.share(user, msgResp)
        response.nGlod = user.gold
        data = msgResp.SerializeToString()
        self.write(data)

    def seeAdGetGlod(self, user, msgResp):
        response = msgResp.response.seeAdResponse
        if user.adtime and Utils().dbTime2Number(user.adtime) < Utils().LastDayEndTime():
            user.ads = 1
        else:
            if user.ads >= config_game['seeVideoAdTimes']:
                msgResp.response.nErrorCode = config_error['timesnone']
                return
            user.ads += 1
        newGlod = config_game['goldSeeAd']
        user.gold += newGlod
        user.adtime = Utils().dbTimeCreate()
        kwargs = {"ads": user.ads, "adtime": user.adtime, "gold": user.gold}
        Dal_User().uqdateUser(user.id, **kwargs)
        response.nTimes = config_game['seeVideoAdTimes'] - user.ads

    def endseeAd(self, user, msgResp, nGlod):
        response = msgResp.response.seeAdResponse
        if user.adtime and Utils().dbTime2Number(user.adtime) < Utils().LastDayEndTime():
            user.ads = 1
        else:
            if user.ads >= config_game['seeVideoAdTimes']:
                msgResp.response.nErrorCode = config_error['timesnone']
                return
            user.ads += 1
        multiple = config_game['goldEndSeeAd'] - 1
        newGlod = multiple * nGlod
        user.gold += newGlod
        user.adtime = Utils().dbTimeCreate()
        kwargs = {"ads": user.ads, "adtime": user.adtime, "gold": user.gold}
        Dal_User().uqdateUser(user.id, **kwargs)
        response.nTimes = config_game['seeVideoAdTimes'] - user.ads

    def popadd(self, user, msgResp):
        response = msgResp.response.seeAdResponse
        if user.popaddtime and Utils().dbTime2Number(user.popaddtime) < Utils().LastDayEndTime():
            user.popadds = 1
        else:
            if user.popadds >= config_game['seePopAdTimes']:
                msgResp.response.nErrorCode = config_error['timesnone']
                return
            user.popadds += 1
        newGlod = config_game['goldPopAd']
        user.gold += newGlod
        user.popaddtime = Utils().dbTimeCreate()
        kwargs = {"popadds": user.popadds, "popaddtime": user.popaddtime, "gold": user.gold}
        Dal_User().uqdateUser(user.id, **kwargs)
        response.nTimes = config_game['seePopAdTimes'] - user.popadds

    def share(self, user, msgResp):
        response = msgResp.response.seeAdResponse
        if user.sharetime and Utils().dbTime2Number(user.sharetime) < Utils().LastDayEndTime():
            user.shares = 1
        else:
            if user.shares >= config_game['shareTimes']:
                msgResp.response.nErrorCode = config_error['timesnone']
                return
            user.shares += 1
        newGlod = config_game['goldShare']
        user.gold += newGlod
        user.sharetime = Utils().dbTimeCreate()
        kwargs = {"shares": user.shares, "sharetime": user.sharetime, "gold": user.gold}
        Dal_User().uqdateUser(user.id, **kwargs)
        response.nTimes = config_game['shareTimes'] - user.shares

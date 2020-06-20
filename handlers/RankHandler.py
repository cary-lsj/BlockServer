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


class RankHandler(BaseHandler):
    def post(self):
        msgReq = msg_pb2.Msg()
        msgReq.ParseFromString(self.request.body)

        msgResp = msg_pb2.Msg()
        msgResp.type = msg_pb2.EnumMsg.Value('rankresponse')

        request = msgReq.request.rankRequest
        response = msgResp.response.rankResponse

        msgResp.response.nErrorCode = config_error['success']

        uid = request.sID

        user = Dal_User().getUser(uid)
        if user == None:
            msgResp.response.nErrorCode = config_error['userinvaild']
        else:
            rankDatas = Dal_User().getRankCache()
            for index, uid in enumerate(rankDatas):
                user = Dal_User().getUser(uid)
                if user:
                    respData = response.rankDatas.add()
                    respData.id = uid
                    respData.sNick = user.nickname
                    respData.nRank = index
                    respData.starNum = Dal_User().getUserTopGateStar(uid)
                    respData.sHeadimg = user.headimgurl

        data = msgResp.SerializeToString()
        self.write(data)

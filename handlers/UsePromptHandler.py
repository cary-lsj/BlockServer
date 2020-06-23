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


class UsePromptHandler(BaseHandler):
    def post(self):
        msgReq = msg_pb2.Msg()
        msgReq.ParseFromString(self.request.body)

        msgResp = msg_pb2.Msg()
        msgResp.type = msg_pb2.EnumMsg.Value('usepromptresponse')

        request = msgReq.request.usePromptRequest
        response = msgResp.response.usePromptResponse
        uid = request.sID

        user = Dal_User().getUser(uid)
        costGold = config_game['buyTipPrice']
        if user == None:
            msgResp.response.nErrorCode = config_error['userinvaild']
        elif user.gold < costGold:
            msgResp.response.nErrorCode = config_error['moneyerror']
        else:
            msgResp.response.nErrorCode = config_error['success']
            user.gold = user.gold - costGold
            kwargs = {"gold": user.gold}
            Dal_User().uqdateUser(user.id, **kwargs)
            response.nGold = user.gold

        data = msgResp.SerializeToString()
        self.write(data)

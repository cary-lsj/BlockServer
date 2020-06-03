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


class SeeADHandler(BaseHandler):
    def post(self):
        # msgReq = msg_pb2.Msg()
        # msgReq.ParseFromString(self.request.body)
        #
        # msgResp = msg_pb2.Msg()
        # msgResp.type = msg_pb2.EnumMsg.Value('seeadresponse')
        #
        # request = msgReq.request.seeAdRequest
        # response = msgResp.response.seeAdResponse

        resp = {}
        resp['nErrorCode'] = config_error['success']

        req = json.loads(self.request.body)
        uid = req["request"]["sID"]

        user = Dal_User().getUser(uid)
        if user == None:
            resp['nErrorCode'] = config_error['userinvaild']
        else:
            user.tips = user.tips + 1
            kwargs = {"tips": user.tips}
            Dal_User().uqdateUser(user.id, **kwargs)
            resp['nPrompt'] =  user.tips

        msg={}
        msg["type"] = config_game['msgType']['seeadresponse']
        msg["response"] = resp
        resp = json.dumps(msg)

        self.write(resp)

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
        # msgReq = msg_pb2.Msg()
        # msgReq.ParseFromString(self.request.body)
        #
        # msgResp = msg_pb2.Msg()
        # msgResp.type = msg_pb2.EnumMsg.Value('usepromptresponse')
        #
        # request = msgReq.request.usePromptRequest
        # response = msgResp.response.usePromptResponse

        resp = {}
        resp['nErrorCode'] = config_error['success']

        req = json.loads(self.request.body)
        uid = req["request"]["sID"]

        user = Dal_User().getUser(uid)
        if user == None:
            resp['nErrorCode'] = config_error['userinvaild']
        elif user.tips == 0:
            resp['nErrorCode'] = config_error['ptomptnone']
        else:
            user.dtips = user.dtips + 1  # 每次开始，临时的提示数据清空，结束的时候写入数据库

        msg = {}
        msg["type"] = config_game['msgType']['usepromptresponse']
        msg["response"] = resp
        resp = json.dumps(msg)

        self.write(resp)

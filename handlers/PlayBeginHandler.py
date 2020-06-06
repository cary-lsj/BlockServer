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


class PlayBeginHandler(BaseHandler):
    def post(self):

        return

        msgReq = msg_pb2.Msg()
        msgReq.ParseFromString(self.request.body)

        msgResp = msg_pb2.Msg()
        msgResp.type = msg_pb2.EnumMsg.Value('playbeginresponse')

        request = msgReq.request.playBeginRequest
        response = msgResp.response.playBeginResponse


        msgResp.nErrorCode = config_error['success']

        req = json.loads(self.request.body)
        uid = request.sID
        gateID = request.gateID

        user = Dal_User().getUser(uid)
        if user == None:
            resp['nErrorCode'] = config_error['userinvaild']
        else:
            user.dtips = 0#每次开始，临时的提示数据清空，结束的时候写入数据库
            #检查当前关卡是否解锁
            bUnLock = Dal_User().isUnLockGate(user.id,gateID)
            if bUnLock== False:
                resp['nErrorCode'] = config_error['gateunlock']
            else:
                gateinfo = Dal_User().getGateInfoByGateID(user.id,gateID)
                resp['gateId'] = gateinfo.gid
                resp['nTopStar'] = gateinfo.gatestar
                resp['nPrompt'] =  user.tips


        msg={}
        msg["type"] = config_game['msgType']['playbeginresponse']
        msg["response"] = resp
        resp = json.dumps(msg)

        self.write(resp)

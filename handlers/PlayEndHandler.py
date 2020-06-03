# -*- coding:utf-8 -*-
import json

from configs.config_default import configs_default
from configs.config_game import config_game
from dal.dal_user import Dal_User
from model.gateinfo import Gateinfo
from model.user import User
from dal.dal_gateinfo import Dal_Gateinfo
from configs.config_error import config_error
from protobuf.errorcode_pb2 import ErrorCode
from tools.utils import Utils
from handlers.BaseHandler import BaseHandler
from protobuf import play_begin_pb2, msg_pb2


class PlayEndHandler(BaseHandler):
    def post(self):
        # msgReq = msg_pb2.Msg()
        # msgReq.ParseFromString(self.request.body)
        #
        # msgResp = msg_pb2.Msg()
        # msgResp.type = msg_pb2.EnumMsg.Value('playendresponse')
        #
        # request = msgReq.request.playEndRequest
        # response = msgResp.response.playEndResponse

        resp = {}
        resp['nErrorCode'] = config_error['success']

        req = json.loads(self.request.body)
        uid = req["request"]["sID"]
        gateID = req["request"]["gateID"]


        user = Dal_User().getUser(uid)
        if user == None:
            resp['nErrorCode'] = config_error['userinvaild']
        else:
            #检查当前关卡是否解锁
            bUnLock = Dal_User().isUnLockGate(user.id,gateID)
            if bUnLock== False:
                resp['nErrorCode'] = config_error['gateunlock']
            else:
                if  user.dtips>0:#扣除提示机会
                    user.tips = user.tips - user.dtips
                    kwargs = {"tips": user.tips }
                    Dal_User().uqdateUser(user.id, **kwargs)

                gateinfo = Dal_User().getGateInfoByGateID(user.id,gateID)
                gateinfo.gatestar = config_game['maxGateStar']
                if user.dtips > 0:#计算星级
                   gateinfo.gatestar = gateinfo.gatestar -  user.dtips
                kwargs = {"gatestar": gateinfo.gatestar}
                Dal_Gateinfo().uqdateGateinfo(gateinfo.id, **kwargs)

                #刷新排行
                Dal_User().updateRankCache(uid)

                resp['gateID'] = gateID
                resp['nTopStar'] = gateinfo.gatestar
                resp['nTotalStar'] = Dal_User().getUserTopGateStar(user.id)

                #如果当前玩的是玩家最大关卡，则解锁下一关卡
                newGateID = int(gateID) + 1
                bUnLock = Dal_User().isUnLockGate(user.id, newGateID)
                if bUnLock == False:
                    if newGateID <= config_game['maxGate'] :
                        newgate = Gateinfo(gid=newGateID, uid=user.id, gatestar=0, state=1)
                        newid = Dal_Gateinfo().addGateinfo(newgate)

                        #更新用户解锁关卡信息
                        gates = Utils().decodeIDFormat(user.gates)
                        gates.append(newid)
                        user.gates = Utils().encodeIDFormat(gates)
                        kwargs = {"gates": user.gates }
                        Dal_User().uqdateUser(user.id, **kwargs)
                    else:
                        resp['nErrorCode'] = config_error['maxgates']#大满贯

        msg={}
        msg["type"] = config_game['msgType']['playendresponse']
        msg["response"] = resp
        resp = json.dumps(msg)

        self.write(resp)

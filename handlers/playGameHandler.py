# -*- coding:utf-8 -*-
import json
import time

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
from model.gateinfo import Gateinfo


class PlayGameHandler(BaseHandler):
    begin_time_cache = dict()  ##玩家开始游玩时间集合

    def post(self):
        msgReq = msg_pb2.Msg()
        msgReq.ParseFromString(self.request.body)

        if msgReq.type == msg_pb2.EnumMsg.Value('playbeginrequest'):
            self.playBeginRequest(msgReq.request.playBeginRequest)
        elif msgReq.type == msg_pb2.EnumMsg.Value('playendrequest'):
            self.playEndRequest(msgReq.request.playEndRequest)

    def playBeginRequest(self, request):
        msgResp = msg_pb2.Msg()
        msgResp.type = msg_pb2.EnumMsg.Value('playbeginresponse')

        response = msgResp.response.playBeginResponse

        msgResp.response.nErrorCode = config_error['success']

        uid = request.sID
        gateID = request.gateID

        user = Dal_User().getUser(uid)
        if user == None:
            msgResp.response.nErrorCode = config_error['userinvaild']
        else:
            user.dtips = 0  # 每次开始，临时的提示数据清空，结束的时候写入数据库
            # 检查当前关卡是否解锁
            bUnLock = Dal_User().isUnLockGate(user.id, gateID)
            if bUnLock == False:
                msgResp.response.nErrorCode = config_error['gateunlock']
            else:
                gateinfo = Dal_User().getGateInfoByGateID(user.id, gateID)
                response.gateId = gateinfo.gid
                beginTime = int(time.time())
                endTime = beginTime
                response.nBeginTime = endTime
                self.add_begin_time(user.id, beginTime)

        data = msgResp.SerializeToString()
        self.write(data)

    def playEndRequest(self, request):
        msgResp = msg_pb2.Msg()
        msgResp.type = msg_pb2.EnumMsg.Value('playendresponse')

        response = msgResp.response.playEndResponse

        msgResp.response.nErrorCode = config_error['success']

        uid = request.sID
        gateID = request.gateID

        user = Dal_User().getUser(uid)
        if user == None:
            msgResp.response.nErrorCode = config_error['userinvaild']
        else:
            # 检查当前关卡是否解锁
            bUnLock = Dal_User().isUnLockGate(user.id, gateID)
            if bUnLock == False:
                msgResp.response.nErrorCode = config_error['gateunlock']
            else:
                gateinfo = Dal_User().getGateInfoByGateID(user.id, gateID)
                gatestar = 0
                beginTime = self.get_begin_time(user.id)
                useTime = 0
                if beginTime != None:  # 没有记录开始时间按0星计算
                    useTime = int(time.time()) - beginTime

                    if useTime < config_game['timeShreeStar']:
                        gatestar = 3
                    elif useTime < config_game['timeTwoStar']:
                        gatestar = 2
                    elif useTime < config_game['timeOneStar']:
                        gatestar = 1
                new_get_gold = 0
                if gateinfo.gatestar < gatestar:
                    ## 获得新的星星 需要给他发奖励
                    for i in range(gateinfo.gatestar, gatestar):
                        if config_game['goldStar'][i] != None:
                            new_get_gold += config_game['goldStar'][i]

                    kwargs = {"gatestar": gatestar}
                    Dal_Gateinfo().uqdateGateinfo(gateinfo.id, **kwargs)
                else:
                    new_get_gold = config_game['goldPlayEnd']

                user.gold = user.gold + new_get_gold
                kwargs = {"gold": user.gold}
                Dal_User().uqdateUser(user.id, **kwargs)

                # 刷新排行
                Dal_User().updateRankCache(uid)

                response.gateID = gateID
                response.nTopStar = gatestar
                response.nGetGold = new_get_gold
                response.nGold = user.gold
                response.nUseTime = useTime

                # 如果当前玩的是玩家最大关卡，则解锁下一关卡
                newGateID = int(gateID) + 1
                bUnLock = Dal_User().isUnLockGate(user.id, newGateID)
                if bUnLock == False:
                    newgate = Gateinfo(gid=newGateID, uid=user.id, gatestar=0, state=1)
                    newid = Dal_Gateinfo().addGateinfo(newgate)

                    # 更新用户解锁关卡信息
                    Dal_User().openNewGates(user.id, [newid])

        gates = Dal_User().getUserGates(user.id)
        for index, id in enumerate(gates):
            gate = response.gates.add()
            gateinfo = Dal_Gateinfo().getGateinfo(id)
            gate.id = gateinfo.gid
            gate.starNum = gateinfo.gatestar

        data = msgResp.SerializeToString()
        self.write(data)

    def add_begin_time(self, id, time):
        self.begin_time_cache[id] = time

    def get_begin_time(self, id):
        return self.begin_time_cache.get(id)

    def del_begin_time(self, id):
        self.begin_time_cache.pop(id)

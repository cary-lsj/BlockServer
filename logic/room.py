#-*-coding:utf-8-*-
import math
import random

from configs.config_default import configs_default
from configs.config_game import config_game, config_gate
from logic.gamer import Gamer

from dal.dal_user import Dal_User
from protobuf import msg_pb2
from tools.mainTimerManager import MainTimerManager
from tools.utils import Utils
from configs.config_error import config_error
import uuid
## 定义一个房间基类
class Room:
    def __init__(self,id,conn):##房主链接，房主id
        self.m_owner = id  # 房主id
        self.m_type =  'quadra'  # 是否空闲
        self.m_bMatch =  False  # 是否匹配
        self.m_nRankIndex =  1  # 是否匹配
        self.m_id = (str)(uuid.uuid1())  # 生成房间id
        self.m_gamerCache=dict()  ##玩家集合，id:gamer
        self.m_timerMgr= MainTimerManager()  ##超时处理队列
        self.m_state = config_game['roomState']['ready']
        self.m_gateID = 0
        self.onCreate(id,conn)

    def sendMessage(self,id,msg):##向玩家发送消息
        data = msg.SerializeToString()
        gamer = self.m_gamerCache[id]
        if gamer.conn:
           self.m_gamerCache[id].conn.write_message(data,True)

    def sendOtherMessage(self,id,msg):##向玩家发送消息
        data = msg.SerializeToString()
        for k,v in self.m_gamerCache.iteritems():
            if k != id:
              if v.conn:
                 v.conn.write_message(data,True)

    def sendAllMessage(self,msg):##向玩家发送消息
        data = msg.SerializeToString()
        for k,v in self.m_gamerCache.iteritems():
            if v.conn:
                 v.conn.write_message(data,True)

    def reset(self):  ##重置房间
        self.m_nRankIndex =  1  # 是否匹配
        self.m_gateID = 0
        for k, v in self.m_gamerCache.iteritems():
             v.reset()

##网络协议相关

    def onCreate(self,id,conn):  ##玩家创建房间,id
        newGamer = Gamer(id,conn,self)
        self.m_gamerCache[id] = newGamer

        msg = msg_pb2.Msg()
        msg.type = msg_pb2.EnumMsg.Value('createroomresponse')
        msg.response.nErrorCode = config_error['success']
        msg.response.createRoomResponse.sRoomID = self.m_id
        self.sendMessage(id,msg)


    def onJoin(self,id,conn):##玩家加入房间,id
        id = str(id)
        msg = msg_pb2.Msg()
        msg.type = msg_pb2.EnumMsg.Value('joinroomresponse')

        if self.m_state == config_game['roomState']['playing']:
            msg.response.nErrorCode = config_error['roomplaying']
            self.sendMessage(id, msg)
            return

        newGamer = self.m_gamerCache.get(id)
        if newGamer == None:
            if self.isFull():
                msg.response.nErrorCode = config_error['roomfull']
                self.sendMessage(id, msg)
                return
            newGamer = Gamer(id,conn,self)
            newGamer.m_bAI = (conn == None)
            self.m_gamerCache[id] = newGamer
        else:
            newGamer.conn = conn

        #网络协议,响应
        msg = msg_pb2.Msg()
        msg.type = msg_pb2.EnumMsg.Value('joinroomresponse')
        msg.response.nErrorCode = config_error['success']
        msg.response.joinRoomResponse.joinRoom.sRoomID = self.m_id
        msg.response.joinRoomResponse.joinRoom.sBossID = self.m_owner
        for k,v in self.m_gamerCache.iteritems():
             gamer = msg.response.joinRoomResponse.joinRoom.gamers.add()
             gamer.sID = k
             user = Dal_User().getUser(k)
             if user:
                 gamer.sNick = user.nickname
                 gamer.sHeadImg = user.headimgurl
                 gamer.nRankLevel = user.ranklevel

        self.sendMessage(id,msg)
        #网络协议,通知其他人加入了新人

        msg = msg_pb2.Msg()
        msg.type = msg_pb2.EnumMsg.Value('joinroomnotify')
        msg.notify.joinRoomNotify.joinGamer.sID = newGamer.id
        user = Dal_User().getUser(newGamer.id)
        if user:
            msg.notify.joinRoomNotify.joinGamer.sNick = user.nickname
            msg.notify.joinRoomNotify.joinGamer.sHeadImg = user.headimgurl
            msg.notify.joinRoomNotify.joinGamer.nRankLevel = user.ranklevel
        self.sendOtherMessage(id,msg)

      #人满开始
        #self.gameStart()


    def onLeave(self, id):  ##玩家离开房间,id
        #网络协议
        msg = msg_pb2.Msg()
        msg.type = msg_pb2.EnumMsg.Value('leaveroomresponse')
        msg.response.nErrorCode = config_error['success']
        self.sendMessage(id,msg)

        msg = msg_pb2.Msg()
        msg.type = msg_pb2.EnumMsg.Value('leaveroomnotify')
        msg.notify.leaveRoomNotify.sID = id
        msg.notify.leaveRoomNotify.sRoomID = self.m_id
        self.sendOtherMessage(id, msg)

        self.m_gamerCache.pop(id)
        # 房间解散
        if len(self.m_gamerCache) == 0 or self.self.m_owner == id:
            return  True

    def onStartGame(self,uid):  ##房间内开始游戏请求
        msg = msg_pb2.Msg()
        msg.type = msg_pb2.EnumMsg.Value('startgameresponse')
        if len(self.m_gamerCache) <= 1:
            msg.response.nErrorCode = config_error['roomnotfull']#人数不够，暂定
            self.sendMessage(uid, msg)
            return

        msg.response.nErrorCode = config_error['success']
        self.sendMessage(uid, msg)

        self.gameStart()


    def onMatchGame(self,uid):  ##房间内匹配游戏请求
        self.m_bMatch = True

        msg = msg_pb2.Msg()
        msg.type = msg_pb2.EnumMsg.Value('matchgameresponse')
        msg.response.nErrorCode = config_error['success']
        self.sendMessage(uid, msg)

        self.gameMatch()

    def onEndRoomGame(self,uid):  ##房间内每个玩家的结束请求
        gamer = self.m_gamerCache.get(uid)
        #记录每个玩家的结束时间
        gamer.m_finishTime = self.m_nTickCount
        gamer.m_nRank =  self.m_nRankIndex
        self.m_nRankIndex =  self.m_nRankIndex +1

        msg = msg_pb2.Msg()
        msg.type = msg_pb2.EnumMsg.Value('endgameresponse')
        msg.response.nErrorCode = config_error['success']
        msg.response.endGameResponse.nRank= gamer.m_nRank
        msg.response.endGameResponse.sGamerID=uid
        self.sendMessage(uid,msg)

        if self.isAllGamerEnd():
            self.gameEnd()


    def onUseTool(self,uid,goodid,did):  ##玩家使用道具请求
        goodid = str(goodid)
        msg = msg_pb2.Msg()
        msg.type = msg_pb2.EnumMsg.Value('usetoolresponse')
        if goodid not in config_game['goods']:
            msg.response.nErrorCode = config_error['nogoods']
            self.sendMessage(uid, msg)
            return
        if Dal_User().userTool(uid,goodid) == False:
            msg.response.nErrorCode = config_error['toolnone']
            self.sendMessage(uid, msg)
            return

        gConfig = config_game['goods'][goodid]
        gTime = gConfig['extra']
        gamer = self.m_gamerCache.get(did)

        gamer.m_overTime = gamer.m_overTime + gTime

        msg.response.nErrorCode = config_error['success']
        self.sendMessage(uid, msg)

        msg = msg_pb2.Msg()
        msg.type = msg_pb2.EnumMsg.Value('usetoolnotify')
        msg.notify.useToolNotify.sID = uid
        msg.notify.useToolNotify.goodID = goodid
        msg.notify.useToolNotify.sDID = did
        self.sendOtherMessage(uid, msg)

        Dal_User().updateGoods(uid, goodid, -1)


    def onPlayBlock(self,uid,isadd):  ##玩家放置木块请求
        msg = msg_pb2.Msg()
        msg.response.nErrorCode = config_error['success']
        if isadd == True:
            msg.type = msg_pb2.EnumMsg.Value('playblockaddresponse')
            self.sendMessage(uid, msg)
        else:
            msg.type = msg_pb2.EnumMsg.Value('playblockdeleteresponse')
            self.sendMessage(uid, msg)

        msg = msg_pb2.Msg()
        msg.type = msg_pb2.EnumMsg.Value('playblocknotify')
        msg.notify.playBlockNotify.sID = uid
        msg.notify.playBlockNotify.sRoomID = self.m_id
        msg.notify.playBlockNotify.gateID = self.m_gateID
        msg.notify.playBlockNotify.isAdd = isadd
        self.sendOtherMessage(uid, msg)


    def isFull(self):  ##房间是否空闲
        return  len(self.m_gamerCache) >= config_game['roomType'][self.m_type]

    def gameStart(self):  ##人满开始游戏
        if len(self.m_gamerCache) <= 1:
            return

        self.reset()#开始之前重置房间数据

        self.m_gateID = random.randint(1,config_game['maxVSGate'])

        msg = msg_pb2.Msg()
        msg.type = msg_pb2.EnumMsg.Value('startgamenotify')
        msg.notify.startGameNotify.sRoomID = self.m_id
        msg.notify.startGameNotify.nGID = self.m_gateID
        self.sendAllMessage(msg)

        self.startTimeOut()

        self.m_state = config_game['roomState']['playing']

        self.cancelAITimeOut()
        self.beginAI()

    def gameEnd(self):  ##开始总结算
        self.cancelTimeOut()

        msg = msg_pb2.Msg()
        msg.type = msg_pb2.EnumMsg.Value('endgamenotify')
        msg.notify.endGameNotify.sRoomID = self.m_id
        self.genRankData(msg)
        self.sendAllMessage(msg)

        self.m_state = config_game['roomState']['ready']

    def gameMatch(self):  ##匹配游戏，机器人
        self.addAI()

    def addAI(self):#ai 定时器
        self.m_timerMgr.addTimer('addai',self.onAddAITimeOut,config_game['aitimeout'], {})

    def beginAI(self):#ai 定时器
        for k, v in self.m_gamerCache.iteritems():
            v.aiPlayBlock()

    def startTimeOut(self):  ##超时处理
        self.m_nTickCount = 0
        self.m_timerMgr.addTimer(self.m_id,self.onTimeTick,config_game['timetick'], {})

    def onTimeTick(self,args):  ##同步客户端超时
        self.m_nTickCount = self.m_nTickCount + 1
        for k, v in self.m_gamerCache.iteritems():
            deltaTime = v.m_overTime - self.m_nTickCount
            if deltaTime <= 0:
                self.onGamerTimeOut(v.id)
                continue

            ##网络协议,通知玩家倒计时
            msg = msg_pb2.Msg()
            msg.type = msg_pb2.EnumMsg.Value('gametimeticknotify')
            msg.notify.gameTimeTickNotify.nLeft = deltaTime
            self.sendMessage(k,msg)

    def onGamerTimeOut(self,gid):  ##操作超时回调，
        ##网络协议,通知玩家超时
        gamer = self.m_gamerCache.get(gid)
        if gamer.isGameEnd():return
        gamer.m_nRank = len(self.m_gamerCache)

        msg = msg_pb2.Msg()
        msg.type = msg_pb2.EnumMsg.Value('overtimenotify')
        msg.notify.overTimeNotify.sGamerID = gid
        msg.notify.overTimeNotify.nRank = gamer.m_nRank#超时默认是最后一名
        self.sendMessage(gid,msg)
        if self.isAllGamerEnd():
            self.gameEnd()
            self.cancelTimeOut()

    def cancelTimeOut(self):  ##取消超时处理
        self.m_timerMgr.delTimer(self.m_id)

    def cancelAITimeOut(self):  ##取消超时处理
        self.m_timerMgr.delTimer('addai')

    def onAddAITimeOut(self, args):  ##AI超时
        maxAICount = config_game['roomType'][self.m_type] - 1
        aiID = len(self.m_gamerCache)
        self.onJoin(aiID, None)
        if aiID >= maxAICount:
           self.cancelAITimeOut()


    def isAllGamerEnd(self):  ##判断是否所有玩家结束
        for k, v in self.m_gamerCache.iteritems():
            if v.isGameEnd() == False:
                return False

        return True

    def genRankData(self,msg):  ##根据玩家结束时间生成假的排名数据
        for k, v in self.m_gamerCache.iteritems():
            rankData = msg.notify.endGameNotify.rankEndGameDatas.add()
            rankData.sGamerID = k
            rankData.nTime = v.m_finishTime
            rankData.nRank = v.m_nRank

            endGold = config_game['endCalc']['baseGold'] * (len(self.m_gamerCache) - v.m_nRank + 1)
            user = Dal_User().getUser(k)
            if user:
                user.gold = user.gold + endGold
                kwargs = {"gold": user.gold}
                Dal_User().uqdateUser(user.id, **kwargs)

            rankData.nGold = endGold

            rankData.nLevel = 1  # 具体等级规则另外协商


    def getGateBlockCount(self):
        gateInfo = config_gate['port'][self.m_gateID]
        blockCount = len(gateInfo['map'])
        return blockCount
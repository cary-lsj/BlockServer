#-*-coding:utf-8-*-
'''
逻辑玩家类
'''
## 定义一个游戏内逻辑玩家类
import math

from configs.config_game import config_game
from tools.mainTimerManager import MainTimerManager
import random

class Gamer:
    def __init__(self,id,conn,room):##房主链接，房主id
       self.id = id#玩家userid
       self.conn = conn
       self.m_finishTime = config_game['timeout']
       self.m_overTime = config_game['timeout']
       self.m_nRank = -1
       self.m_bAI = False
       self.m_timerMgr = MainTimerManager()  ##定时器
       self.m_room = room
       self.m_aiPlayIndex = 0

    def reset(self):
        self.m_finishTime = config_game['timeout']
        self.m_overTime = config_game['timeout']
        self.m_nRank = -1
        self.m_aiPlayIndex = 0

    def isGameEnd(self):
        return (self.m_nRank != -1)

#机器人玩
    def aiPlayBlock(self):
        if self.m_bAI == False:return
        gatePlayCount = self.m_room.getGateBlockCount()
        maxTime =  int(math.ceil(config_game['timeout'] / gatePlayCount))
        playTime = random.randint(1,maxTime) * 1000
        self.m_timerMgr.addTimer('aiplay', self.onAIPlayBlock, playTime, {})

    def onAIPlayBlock(self, args):  ##AI超时
        self.m_room.onPlayBlock(self.id,True)
        self.m_aiPlayIndex = self.m_aiPlayIndex + 1
        gatePlayCount = self.m_room.getGateBlockCount()
        if self.m_aiPlayIndex >= gatePlayCount:
            self.m_room.onEndRoomGame(self.id)#模拟玩家结束请求
            self.cancelAIPlayTimeOut()


    def cancelAIPlayTimeOut(self):  ##取消超时处理
        self.m_timerMgr.delTimer('aiplay')
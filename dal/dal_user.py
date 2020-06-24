# -*-coding:utf-8-*-
'''
dal 层user继承了dal_base的所有的方法 增删改查 缓存
'''
from configs.config_game import config_game
from dal.dal_gateinfo import Dal_Gateinfo
from db.mysqlapp import MySQLApp
from model.user import User
from dal.dal_base import Dal_base
from tools.singleton import Singleton
from tools.utils import Utils


class Dal_User(Dal_base):
    def __init__(self):
        Dal_base.__init__(self)
        self.m_rankCache = []
        self.m_GameTimeCache = dict()

    ##增
    def addUser(self, newUser):
        newUser.id = newUser.save()
        self._m_cache[newUser.id] = newUser
        ## 返回一个新增user的id
        return newUser.id

    ## 查
    def getUser(self, pk):
        pk = int(pk)
        return self.get(pk, User)

    def getLoginUser(self, username):
        username = str(username)
        for k, v in self._m_cache.iteritems():
            if v.username == username:
                return v
        return None

    ## 改
    def uqdateUser(self, pk, **kwargs):
        pk = str(pk)
        return self.update(pk, User, **kwargs)

    ## 删
    def delateUser(self, pk):
        pk = str(pk)
        self.delete(pk, User)

        ## 初始化数据库

    ## 缓存
    def initCache(self):
        self.initDB('userinfo', User)
        self.initRankCache()

    ## 排序缓存
    def initRankCache(self):
        tempCache = dict()
        for k, v in self._m_cache.iteritems():
            totalStar = self.getUserTopGateStar(k)
            tempCache[k] = totalStar

        tempCache = sorted(tempCache.items(), key=lambda x: x[1], reverse=True)
        tempCache = tempCache[0:config_game['maxRank']]
        for index, v in enumerate(tempCache):
            uid = v[0]
            self.m_rankCache.append(uid)  # 仅存id
            continue

    ## 每次游戏结束刷新排序缓存,这里仅有20个数据了
    def updateRankCache(self, uid):
        tempCache = dict()
        if uid not in self.m_rankCache:
            self.m_rankCache.append(uid)
        for index, uid in enumerate(self.m_rankCache):
            totalStar = self.getUserTopGateStar(uid)
            tempCache[uid] = totalStar
        tempCache = sorted(tempCache.items(), key=lambda x: x[1], reverse=True)
        tempCache = tempCache[0:config_game['maxRank']]
        self.m_rankCache = []
        for index, v in enumerate(tempCache):
            self.m_rankCache.append(v[0])  # 仅存id

    ## 每次游戏结束刷新排序缓存
    def getRankCache(self):
        return self.m_rankCache

    ## 获取用户对应的所有关卡id集合
    def getUserGates(self, uid):
        uid = str(uid)
        user = self.getUser(uid)
        if user:
            gates = Utils().decodeIDFormat(user.gates)
            return gates
        return None

    ## 用户解锁新关卡
    def openNewGates(self, uid, gids):
        uid = str(uid)
        user = self.getUser(uid)
        gates = Utils().decodeIDFormat(user.gates)
        gates = gates + gids
        user.gates = Utils().encodeIDFormat(gates)
        kwargs = {"gates": user.gates}
        Dal_User().uqdateUser(user.id, **kwargs)

    ## 获取用户对应的当前累积通关星级
    def getUserTopGateStar(self, uid):
        uid = str(uid)
        topGates = self.getUserGates(uid)
        if topGates == None:
            return None

        topStar = 0
        for index, id in enumerate(topGates):
            gi = Dal_Gateinfo().getGateinfo(id)
            if gi == None: continue
            topStar = topStar + gi.gatestar
        return topStar

    ## 检查当前关卡是否是解锁状态
    def isUnLockGate(self, uid, gid):
        uid = str(uid)
        gi = self.getGateInfoByGateID(uid, gid)
        bUnLock = (gi != None)
        return bUnLock

    ## 通过关卡id获取用户的关卡信息
    def getGateInfoByGateID(self, uid, gid):
        uid = str(uid)
        user = self.getUser(uid)
        if user:
            gates = Utils().decodeIDFormat(user.gates)
            for index, id in enumerate(gates):
                gateinfo = Dal_Gateinfo().getGateinfo(id)
                if gateinfo.gid == gid:
                    return gateinfo
        return None

    ## 更新商品，特殊处理下
    def updateGoods(self, uid, goodid, count):
        gid = unicode(goodid)
        user = self.getUser(uid)
        dictGoods = Utils().decodeMutilFormat(user.goods, ';', ':')
        if dictGoods.has_key(gid):
            dictGoods[gid] = int(dictGoods[gid]) + count
        else:
            dictGoods[gid] = count

        if dictGoods[gid] < 0: dictGoods[gid] = 0

        user.goods = Utils().encodeMutilFormat(dictGoods, ';', ':')
        kwargs = {"goods": user.goods}
        Dal_User().uqdateUser(user.id, **kwargs)

    def userTool(self, uid, goodid):
        gid = unicode(goodid)
        user = self.getUser(uid)
        dictGoods = Utils().decodeMutilFormat(user.goods, ';', ':')
        if dictGoods.has_key(gid):
            count = int(dictGoods[gid])
            if (count > 1):
                dictGoods[gid] = count - 1
                user.goods = Utils().encodeMutilFormat(dictGoods, ';', ':')
                kwargs = {"goods": user.goods}
                Dal_User().uqdateUser(user.id, **kwargs)
                return True
        return False

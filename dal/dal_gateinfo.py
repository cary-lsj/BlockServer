# -*-coding:utf-8-*-
from dal.dal_base import Dal_base
from model.gateinfo import Gateinfo
from tools.singleton import Singleton


class Dal_Gateinfo(Dal_base):
    def __init__(self):
        Dal_base.__init__(self)

    ##增
    def addGateinfo(self, newGateinfo):
        newGateinfo.id = newGateinfo.save()
        self._m_cache[newGateinfo.id] = newGateinfo
        return newGateinfo.id

    ## 查
    def getGateinfo(self, pk):
        pk = int(pk)
        return self.get(pk, Gateinfo)

    ## 改
    def uqdateGateinfo(self, pk, **kwargs):
        pk = int(pk)
        return self.update(pk, Gateinfo, **kwargs)

    ## 删
    def delateGateinfo(self, pk):
        pk = int(pk)
        self.delete(pk, Gateinfo)

    ## 缓存
    def initCache(self):
        self.initDB('gateinfo', Gateinfo)

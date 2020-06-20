# coding:utf-8

import json
import tornado.web
import time
import os

from configs.config_game import config_game
from model.user import User
from dal.dal_user import Dal_User
from configs.config_error import config_error
from configs.config_default import configs_default
from tools.utils import Utils
from handlers.BaseHandler import BaseHandler


class BuyHandler(BaseHandler):
    def post(self):
        resp = {}
        resp['nErrorCode'] = config_error['success']

        req = json.loads(self.request.body)
        uid = req["request"]["nUserID"]
        goods = req["request"]["goods"]

        user = Dal_User().getUser(uid)
        if user == None:
            resp['nErrorCode'] = config_error['userinvaild']
        else:
            totalG = 0
            totalM = 0
            for i, v in enumerate(goods):
                gID = v["nID"]
                gCount = v["nCount"]
                gConfig = config_game['goods'][str(gID)]
                totalM = totalM + gConfig['money'] * gCount  # 需要花费的钻石数量
                totalG = totalG + gConfig['gold'] * gCount  # 需要花费的游戏币数量

            if user.money < totalM or user.gold < totalG:
                resp['nErrorCode'] = config_error['moneyerror']
            else:
                user.gold = user.gold - totalG
                user.money = user.money - totalM
                resp['newAssets'] = {}
                resp['newAssets']['UserID'] = user.id
                resp['newAssets']['nGold'] = user.gold
                resp['newAssets']['nMoney'] = user.money
                resp['newAssets']['sAssets'] = user.goods
                kwargs = {"gold": user.gold, "money": user.money, }
                Dal_User().uqdateUser(user.id, **kwargs)

                for i, v in enumerate(goods):
                    gID = v["nID"]
                    gCount = v["nCount"]
                    Dal_User().updateGoods(user.id, gID, gCount)

        msg = {}
        msg["type"] = config_game['msgType']['buyresponse']
        msg["response"] = resp
        resp = json.dumps(msg)
        self.write(resp)

#-*-coding:utf-8-*-
'''
逻辑玩家类
'''
## 单元测试
import json
import math

from configs.config_game import config_game
from tools.mainTimerManager import MainTimerManager
import random

class UTest:
    def __init__(self):
          pass

    def UT_Json(self):
        with open("configs/pkmapinfo.json", 'r') as load_f:
            load_dict = json.load(load_f)
            return load_dict


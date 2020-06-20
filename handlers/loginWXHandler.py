# coding:utf-8

import json
import tornado.web
import time
import os
import urllib

from configs.config_default import configs_default
from configs.config_game import config_game
from dal.dal_gateinfo import Dal_Gateinfo
from model.gateinfo import Gateinfo
from model.user import User
from dal.dal_user import Dal_User
from configs.config_error import config_error
from protobuf.errorcode_pb2 import ErrorCode
from tools.utils import Utils
from handlers.BaseHandler import BaseHandler
from protobuf import msg_pb2


class LoginWXHandler(BaseHandler):
    def post(self):
        req = self.request.arguments
        code = req['code'][0]
        appid = "wx97a0264b06970cb6"
        secret = "e76e02cbae40277733835b1b009fdd08"
        url = "https://api.weixin.qq.com/sns/jscode2session?appid=" + appid + "&secret=" + secret + "&js_code=" + code + "&grant_type=authorization_code"

        res = urllib.urlopen(url)
        read = res.read()
        data = json.loads(read)
        self.write(read)

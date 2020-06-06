#coding:utf-8

import json
import tornado.web
import time
import os
import logging

from model.user import User
from dal.dal_user import Dal_User
from configs.config_error import config_error
from tools.utils import Utils
from handlers.BaseHandler import BaseHandler
from protobuf import msg_pb2

class ClientLogHandler(BaseHandler):
    def post(self):
        log = self.request.body
        Utils().logMainDebug(log)
        return
    def get(self):
        loger = logging.getLogger("ingenia")
        self.write("test")




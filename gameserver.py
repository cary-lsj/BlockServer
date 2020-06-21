#-*-coding:utf-8
import os
import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop
import tornado.log
import yaml
import logging
import logging.config
import time
import datetime

from configs.config_game import config_gate
from db.mysqlapp import MySQLApp
from application import webapplication
from protobuf import msg_pb2
from tornado.options import define, options

from dal.dal_base import Dal_base
from dal.dal_user import Dal_User


from tools.utils import Utils
from utest.utest import UTest

define("port", default=8080, help="run on the given port", type=int)

def initLog():
    #logging.config.fileConfig('configs/logging.conf')
    logging.config.dictConfig(yaml.load(open('configs/python_logging.yaml', 'r')))

def logTest():
    initLog()

def initCache():
    Dal_User().initCache()

def UnitTest():
    return
    ut = UTest()
    ut.UT_Json()
    return


def main():
    print (options.help)
    # print "Quit the server with CONTROL-C "
    tornado.options.parse_command_line()
    # http_server=tornado.httpserver.HTTPServer(webapplication)
    http_server = tornado.httpserver.HTTPServer(webapplication, ssl_options={
       "certfile": os.path.join(os.path.abspath("."), "www.cxagile.cn.crt"),
       "keyfile": os.path.join(os.path.abspath("."), "www.cxagile.cn.key"),
    })

    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    UnitTest()
    initLog()
    initCache()
    main()


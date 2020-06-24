# -*-coding:utf-8-*-
from handlers.gameHandler import GameHandler
from handlers.loginWXHandler import LoginWXHandler
from handlers.UsePromptHandler import UsePromptHandler
from handlers.SeeADHandler import SeeADHandler
from handlers.RankHandler import RankHandler
from handlers.buyHandler import BuyHandler
from handlers.loginHandler import LoginHandler
from handlers.clientLogHandler import ClientLogHandler
from handlers.playGameHandler import PlayGameHandler
from handlers.uploadInfoHandler import UploadInfoHandler

urls = [
    (r"/login", LoginHandler),
    (r"/loginwx", LoginWXHandler),
    (r"/useprompt", UsePromptHandler),
    (r"/seead", SeeADHandler),
    (r"/rank", RankHandler),
    (r"/game", GameHandler),
    (r"/buy", BuyHandler),
    (r"/log", ClientLogHandler),
    (r"/palygame", PlayGameHandler),
    (r"/uploadInfo", UploadInfoHandler),
]

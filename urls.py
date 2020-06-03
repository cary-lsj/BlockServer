# -*-coding:utf-8-*-
from handlers.gameHandler import GameHandler
from handlers.loginWXHandler import LoginWXHandler
from handlers.PlayBeginHandler import PlayBeginHandler
from handlers.PlayEndHandler import PlayEndHandler
from handlers.UsePromptHandler import UsePromptHandler
from handlers.SeeADHandler import SeeADHandler
from handlers.RankHandler import RankHandler
from handlers.buyHandler import BuyHandler

urls = [
    (r"/loginwx", LoginWXHandler),
    (r"/palybegin", PlayBeginHandler),
    (r"/palyend", PlayEndHandler),
    (r"/useprompt", UsePromptHandler),
    (r"/seead", SeeADHandler),
    (r"/rank", RankHandler),
    (r"/game",GameHandler),
    (r"/buy",BuyHandler)
]

# -*-coding:utf-8-*-
'''
用户点击开始游戏  用户传入的数据是 用户名和歌曲id  返回值是错误码  和的当前的体力值
'''
import json
import tornado.web
import tornado.websocket
import time
import logging

from logic.room import Room
from protobuf import msg_pb2


# 基本思想是vip和普通房间都是先在后台创建房间，
# vip房间需要消耗房卡道具，可邀请微信好友加入
# 普通房间是当用户开始游戏时，先检查房间队列中有没有空闲的，如果有就直接加入，没有则创建新的普通房间加入
# 一旦创建房间，默认进入长链接模式
class GameHandler(tornado.websocket.WebSocketHandler):
    waiters = dict()  # 用户链接集合
    room_cache = dict()  ##玩家分组集合，房间id=》房间

    def check_origin(self, origin):
        return True

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        uID = (self.get_argument('id'))
        GameHandler.waiters[uID] = self

    def on_close(self):
        uID = (self.get_argument('id'))
        GameHandler.waiters.pop(uID)

    @classmethod
    def get_connect(cls, uid):
        return cls.waiters[uid]

    def add_room(self, room):
        self.room_cache[room.id] = room

    def get_room(self, id):
        return self.room_cache.get(id)

    def del_room(self, id):
        self.room_cache.pop(id)

    def on_message(self, message):
        # logging.info("got message %r", message)
        msgRequest = msg_pb2.Msg()
        msgRequest.ParseFromString(message)
        if msgRequest.type == msg_pb2.EnumMsg.Value('createroomrequest'):
            self.on_create_room(msgRequest.request.createRoomRequest)
        elif msgRequest.type == msg_pb2.EnumMsg.Value('joinroomrequest'):
            self.on_join_room(msgRequest.request.joinRoomRequest)
        elif msgRequest.type == msg_pb2.EnumMsg.Value('leaveroomrequest'):
            self.on_leave_room(msgRequest.request.leaveRoomRequest)
        elif msgRequest.type == msg_pb2.EnumMsg.Value('endgamerequest'):
            self.on_end_room_game(msgRequest.request.endGameRequest)
        elif msgRequest.type == msg_pb2.EnumMsg.Value('startgamerequest'):
            self.on_start_game(msgRequest.request.startGameRequest)
        elif msgRequest.type == msg_pb2.EnumMsg.Value('matchgamerequest'):
            self.on_match_game(msgRequest.request.matchGameRequest)
        elif msgRequest.type == msg_pb2.EnumMsg.Value('usetoolrequest'):
            self.on_use_tool(msgRequest.request.useToolRequest)
        elif msgRequest.type == msg_pb2.EnumMsg.Value('playblockaddrequest'):
            self.on_playblock_add(msgRequest.request.playBlockAddRequest)
        elif msgRequest.type == msg_pb2.EnumMsg.Value('playblockdeleterequest'):
            self.on_playblock_delete(msgRequest.request.playBlockDeleteRequest)

    # 创建房间
    def on_create_room(self, message):
        uid = message.sID
        newRoom = Room(uid, GameHandler.waiters[uid])
        self.room_cache[newRoom.m_id] = newRoom

    def on_join_room(self, message):
        uid = message.sID
        rid = message.sRoomID
        room = self.get_room(rid)
        room.onJoin(uid, GameHandler.waiters[uid])

    def on_leave_room(self, message):
        uid = message.sID
        rid = message.sRoomID
        room = self.get_room(rid)
        bEmpty = room.onLeave(uid)
        if bEmpty:
            self.del_room(rid)

    def on_end_room_game(self, message):
        uid = message.sID
        rid = message.sRoomID
        room = self.get_room(rid)
        room.onEndRoomGame(uid)

    def on_start_game(self, message):
        uid = message.sID
        rid = message.sRoomID
        room = self.get_room(rid)
        room.onStartGame(uid)

    def on_match_game(self, message):
        uid = message.sID
        rid = message.sRoomID
        room = self.get_room(rid)
        room.onMatchGame(uid)

    def on_use_tool(self, message):
        uid = message.sID
        rid = message.sRoomID
        goodid = message.goodID
        did = message.sDID
        room = self.get_room(rid)
        room.onUseTool(uid, goodid, did)

    def on_playblock_add(self, message):
        uid = message.sID
        rid = message.sRoomID
        gid = message.gateID
        room = self.get_room(rid)
        room.onPlayBlock(uid, True)

    def on_playblock_delete(self, message):
        uid = message.sID
        rid = message.sRoomID
        gid = message.gateID
        room = self.get_room(rid)
        room.onPlayBlock(uid, False)

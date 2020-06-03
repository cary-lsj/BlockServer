#-*-coding:utf-8-*-
'''
统计所有错误的可能性
'''
config_error={
    'success' : 1,
    'userinvaild' : 2, #无效的用户
    'pwderror'  : 3, #密码错误
    'moneyerror' : 4, #金币不足
    'gateunlock' : 5, #关卡未解锁
    'ptomptnone' : 6, #提示机会不足
    'maxgates' : 7, #全部通关，大满贯
    'roomfull': 8,  # 房间已满
    'roomnotfull': 9, # 房间未满
    'nogoods': 10,  # 没有该物品
    'toolnone': 11 # 道具不足
}
# -*-coding:utf-8-*-
'''
统计所有错误的可能性
'''
import json

with open("configs/pkmapinfo.json", 'r') as load_f:
    config_gate = json.load(load_f)
config_game = {
    'minGate': 1,
    'maxGate': 50,
    'maxGateStar': 3,
    'maxVSGate': 30,
    'maxRank': 20,
    'msgType': {
        'loginresponse': 2,
        'playbeginresponse': 4,
        'playendresponse': 6,
        'seeadresponse': 8,
        'usepromptresponse': 10,
        'rankresponse': 12,
        'buyresponse': 35,
    },
    'roomType':
        {
            'single': 1,
            'solo': 2,
            'triple': 3,
            'quadra': 4
        },
    'roomState':
        {
            'ready': 1,
            'playing': 2,
        },
    "timeout": 50,  # 倒计时间
    "timetick": 1000,
    "aitimeout": 3000,
    'goods': {
        "0": {"desc": "加时卡", "type": 0, "gold": 500, "money": 0, "rmb": 0, "extra": 5},
        "1": {"desc": "减时卡", "type": 0, "gold": 0, "money": 2, "rmb": 0, "extra": -5},
    },
    'endCalc': {
        'baseGold': 10  # 基础结算金币
    },
    "timeShreeStar": 45,  # 三星倒计时间 秒
    "timeTwoStar": 135,  # 二星倒计时间 秒
    "timeOneStar": 225,  # 一星倒计时间 秒
    "seeVideoAdTimes": 5,  # 每天看视频广告的次数
    "shareTimes": 5,  # 每天看分享得提示次数
    "seePopAdTimes": 5,  # 每天自动弹出广告的次数
    "goldStar": {
        0: 0,
        1: 25,  # 第一颗星奖励
        2: 50,  # 第二颗星奖励
        3: 75,  # 第三颗星奖励
    },
    "goldPlayEnd": 10,  # 重复刷关卡给的奖励
    "buyTipPrice": 100,  # 购买一次提示消耗的金币
    "goldShare": 100,  # 分享一次 获得奖励
    "goldSeeAd": 100,  # 看一次视频广告 获得奖励
    "goldPopAd": 100,  # 点击弹出广告 获得奖励
    "goldEndSeeAd": 3,  # 结算看广告获得金币倍数
}

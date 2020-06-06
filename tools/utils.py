#coding:utf-8
import hashlib
import httplib
import os
import threading

import math

from configs.config_game import config_game
from tools.singleton import Singleton
import logging
import random
import string

import time
import datetime
from datetime import timedelta
from protobuf import msg_pb2
import json
#工具类
class Utils:
    __metaclass__ = Singleton

    # def __init__(self):
    #     self.m_nAIInfoRand = -1
    #     self.m_nAIHeadRand = -1

    ##工具中包含有 截取字符串的    编码的 解码的  是否为空的  获取文件路径的
#prama: ,,,;,,, return dict
    def decodeMutilFormat(self,inputstring,char1,char2):## 输入的字符串"1:30;2:20;3:90;4;90"
        outResult = {}
        outlist = inputstring.split(char1);
        for k,substr in enumerate(outlist):
            arrStr = substr.split(char2)
            if len(arrStr) <= 1:continue
            outResult[arrStr[0]] = arrStr[1]
        return outResult

    def encodeMutilFormat(self,inputDict,char1,char2):
        outResult = '' ##{‘name’:"blx","age":20,"sex":"nan"}
        i = 0
        dlen = len(inputDict)
        for k, v in inputDict.iteritems():
            outResult = outResult + str(k) + char2 + str(v)
            i = i + 1
            if i < dlen:
                outResult = outResult + char1

        return outResult

#prama: ;;;; [] return str
    def encodeIDFormat(self,inputList,char = ';'):  ## 列表转化为字符串
        outResult = ''
        index = 0
        listlen = len(inputList)
        for substr in inputList:
            substr = str(substr)
            index = index + 1
            if index < listlen:
                outResult = outResult +substr+ char
            else:
                outResult = outResult +substr
        return outResult
    ## decodeIDFromat() 解码 就是分割字符串 分隔符 传入一个字符串和分隔符 输出一个列表
    def decodeIDFormat(self,inputstring,char = ';'):  ## 字符串转化为列表"1;2;3;4;5" ==> [1,2,3,4]
        outResult = []
        if inputstring == '':return outResult
        outlist = inputstring.split(char)
        for substr in outlist:
            outResult.append(substr)
        return outResult
    ## 判断某个元素是否在一个字符串（可以分割成列表）中
    def isValueInIDFormat(self,v,inputstring):
        if self.isNull(inputstring):
            return False
        outlist = self.decodeIDFormat(inputstring)
        return (str(v) in outlist)   ##返回的值是False  和 True
    ## 判断是否为空
    def isNull(self,v):
        return (v == None or v == '');

    def getFileCountInPath(self,path):
        count = 0
        for root, dirs, files in os.walk(path):
        #print files
            fileLength = len(files)
            if fileLength != 0:
               count = count + fileLength
        return count

    def logDebug(self,msg):
       # return False
       loger= logging.getLogger("newuser")
       loger.info(msg)

    def logMainDebug(self, msg):
        #return False
        loger = logging.getLogger("ingenia")
        loger.info(msg)

    def logPaiString(self,type,value):
        if type == 0:
            if value == 1:return "红中"
            elif value == 2:return "发财"
            elif value == 3:return "白板"
        elif type == 1:
            if value == 1:return "东风"
            elif value == 2:return "南风"
            elif value == 3:return "西风"
            elif value == 4:return "北风"
        elif type == 2:return str(value) + "万"
        elif type == 3:return str(value) + "条"
        elif type == 4:return str(value) + "饼"

#根据id生成邀请码
    def encodeRandomCode(self,id,length=7):
        '''
        id + L + 随机码
        string模块中的3个函数：string.letters，string.printable，string.printable
        '''
        prefix = oct(int(id))+ '9'
        length = length - len(prefix)
        chars=string.digits
        return prefix + ''.join([random.choice(chars) for i in range(length)])

    # 根据id生成账号
    def encodeRandomAccount(self, id, length=11):
        '''
        id + L + 随机码
        string模块中的3个函数：string.letters，string.printable，string.printable
        '''
        prefix ='1'+ oct(int(id)) + '15648'
        length = length - len(prefix)
        chars = string.digits
        return prefix + ''.join([random.choice(chars) for i in range(length)])

    def decodeRandomCode(self,code):
        ''' Hex to Dec '''
        return str(int(code.upper(), 8))

##生成手机验证码
    def createPhoneCode(self,session):
        chars = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        x = random.choice(chars), random.choice(chars), random.choice(chars), random.choice(chars)
        verifyCode = "".join(x)
        return verifyCode

    def sendTelMsg(self,msg, phoneID):
        appid = 1254114772
        appkey = "1234567890abcdef1234567890abcdef"
        # phone_number1 = "12345678901"
        # phone_number2 = "18037665695"
        # phone_number3 = "12345678903"
        # phone_numbers = [phone_number1, phone_number2, phone_number3]
        # templ_id = 7839

        single_sender = SmsSender.SmsSingleSender(appid, appkey)

        # 普通单发
        result = single_sender.send(0, "86", phoneID,"您的添胡游戏验证码为:"+msg, "", "")
        rsp = json.loads(result)
        print result

    def dbTime2Client(self,timeDB):
        timeArre = time.strptime(timeDB, "%Y-%m-%d %H:%M:%S")
        timestrap = int(time.mktime(timeArre))
        v1 = datetime.datetime.utcfromtimestamp(timestrap)
        return v1

    def dateTime2String(self,dt):
        return dt.strftime("%Y-%m-%d-%H")

    def dateTime3String(self,dt):
        return dt.strftime("%Y-%m-%d %H:%M:%S")

    def String2dateTime(self,str):
        return datetime.datetime.strptime(str,"%Y-%m-%d %H:%M:%S")

    def dbTimeCreate(self):
        return time.strftime('%Y-%m-%d %H:%M:%S')

    def dbTime2Number(self,timeDB):
        if isinstance(timeDB,str):
            timeDB = datetime.datetime.strptime(timeDB,"%Y-%m-%d %H:%M:%S")
        timestrap = int(time.mktime(timeDB.timetuple()))
        return timestrap

    def random_range(self,min,max):
        return   random.randint(min, max)

    def random_index(self,rate):
        """随机变量的概率函数"""
        #
        # 参数rate为list<int>
        #
        start = 0
        randnum = random.randint(1, sum(rate))

        for index, item in enumerate(rate):
            start += item
            if randnum <= start:
                break
        return index

    def DateTime2Float(self,dt):
        return time.mktime(dt.timetuple())

#获取某天0点的时间戳
    def DayBeginTime(self,timeD):
        #t = time.localtime(time.time()) 当天
        t = time.localtime(timeD)
        time1 = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t), '%Y-%m-%d %H:%M:%S'))
        return float(time1)

    # 获取某天24点的时间戳
    def DayEndTime(self,timeD):
        z_time = self.DayBeginTime(timeD)
        return z_time + 86400

    # 获取现在到当天24点的时间戳
    def TodayDeltaTime(self):
        cur_time = time.time()
        end_time = self.DayEndTime(cur_time)
        return end_time - cur_time

    # 获取昨天0点的时间戳
    def LastDayBeginTime(self):
        z_time = self.DayBeginTime(time.time())
        return z_time - 86400

    # 获取昨天24点的时间戳
    def LastDayEndTime(self):
        return  self.DayBeginTime(time.time())

    # 获取上周第一天的时间戳
    def LastWeekBeginTime(self):
        now = datetime.datetime.now()
        last_week_start = now - timedelta(days=now.weekday() + 7)
        last_week_start = self.DateTime2Float(last_week_start)
        last_week_start = self.DayBeginTime(last_week_start)
        return last_week_start

    # 获取上周最后一天的时间戳
    def LastWeekEndTime(self):
        now = datetime.datetime.now()
        last_week_end = now - timedelta(days=now.weekday() + 1)
        last_week_end = self.DateTime2Float(last_week_end)
        last_week_end = self.DayEndTime(last_week_end)
        return last_week_end

    # 获取本周最后一天的时间戳
    def WeekEndTime(self):
        now = datetime.datetime.now()
        this_week_end = now + timedelta(days=6 - now.weekday())
        this_week_end =  self.DateTime2Float(this_week_end)
        this_week_end = self.DayEndTime(this_week_end)
        return this_week_end

    # 获取现在到周末24点的时间戳
    def WeekDeltaTime(self):
        cur_time = time.time()
        end_time = self.WeekEndTime()
        return end_time - cur_time

        # 获取上月第一天的时间戳
    def LastMonthBeginTime(self):
        now = datetime.datetime.now()
        this_month_start = datetime.datetime(now.year, now.month, 1)
        last_month_end = this_month_start - timedelta(days=1)
        last_month_start = datetime.datetime(last_month_end.year, last_month_end.month, 1)
        last_month_start = self.DateTime2Float(last_month_start)
        last_month_start = self.DayBeginTime(last_month_start)
        return last_month_start

    # 获取上月最后一天的时间戳
    def LastMonthEndTime(self):
        now = datetime.datetime.now()
        this_month_start = datetime.datetime(now.year, now.month, 1)
        last_month_end = this_month_start - timedelta(days=1)
        last_month_end = self.DateTime2Float(last_month_end)
        last_month_end = self.DayEndTime(last_month_end)
        return last_month_end

    # 获取本月最后一天的时间戳
    def MonthEndTime(self):
        now = datetime.datetime.now()
        nextYear = now.year
        nextMonth = now.month + 1
        if (now.month + 1) > 12:
            nextYear = now.year +1
            nextMonth =  0
        this_month_end = datetime.datetime(nextYear,nextMonth + 1, 1) - timedelta(days=1)
        this_month_end = self.DateTime2Float(this_month_end)
        this_month_end = self.DayEndTime(this_month_end)
        return this_month_end

    # 获取现在到月末24点的时间戳
    def MonthDeltaTime(self):
        cur_time = time.time()
        end_time = self.MonthEndTime()
        return end_time - cur_time

        # 获取去年第一天的时间戳
    def LastYearBeginTime(self):
        now = datetime.datetime.now()
        this_year_start = datetime.datetime(now.year, 1, 1)
        last_year_end = this_year_start - timedelta(days=1)
        last_year_start = datetime.datetime(last_year_end.year, 1, 1)
        last_year_start = self.DateTime2Float(last_year_start)
        last_year_start = self.DayBeginTime(last_year_start)
        return last_year_start

    # 获取去年最后一天的时间戳
    def LastYearEndTime(self):
        now = datetime.datetime.now()
        this_year_start = datetime.datetime(now.year, 1, 1)
        last_year_end = this_year_start - timedelta(days=1)
        last_year_end = self.DateTime2Float(last_year_end)
        last_year_end = self.DayEndTime(last_year_end)
        return last_year_end

    # 获取本年最后一天的时间戳
    def YearEndTime(self):
        now = datetime.datetime.now()
        this_year_end = datetime.datetime(now.year + 1, 1, 1) - timedelta(days=1)
        this_year_end = self.DateTime2Float(this_year_end)
        this_year_end = self.DayEndTime(this_year_end)
        return this_year_end

    # 获取现在到年末24点的时间戳
    def YearDeltaTime(self):
        cur_time = time.time()
        end_time = self.YearEndTime()
        return end_time - cur_time


    # 发送post请求
    def send_post_request(self, host, port, url, data, callback):
        con = None
        try:
            headers = {"Content-type": "application/x-www-form-urlencoded",
                       "Accept": "text/plain"}
            conn = httplib.HTTPConnection(host, port)
            conn.request('POST', url, json.dumps(data), headers)
            httpres = conn.getresponse()
            if '200' != str(httpres.status):
                obj = {}
                obj["result"] = -1
                obj["errmsg"] = str(httpres.status) + " " + httpres.reason
                result = json.dumps(obj)
            else:
                result = httpres.read()
                callback(result)

        except Exception, e:
            import traceback
            obj = {}
            obj["result"] = -2
            obj["errmsg"] = traceback.format_exc()
            result = json.dumps(obj)
        finally:
            if con:
                con.close()
        return result

    def gen_ai_info_rand(self):
        self.m_nAIInfoRand = (self.m_nAIInfoRand  + 1) % config_game['aiInfoCount']
        return self.m_nAIInfoRand

    def gen_ai_head_rand(self):
        self.m_nAIHeadRand = (self.m_nAIHeadRand + 1) % config_game['aiHeadCount']
        return self.m_nAIHeadRand

    def createToken(self):
        token = hashlib.md5(bytes(str(time.time()))).hexdigest()
        return token
    # 分页
    def GetPaging(self,page,num,pageList):
        page_start = ((page - 1) * num)
        page_end = page_start + num
        r_list = pageList[page_start:page_end]
        return r_list
    # 求交集
    def GetIntersection(self,list1,list2):
        return list(set(list2).intersection(set(list1)))


    def any2unicode(self, s, encoding=None):
        if isinstance(s, unicode):
            return s
        else:
            return unicode(s)
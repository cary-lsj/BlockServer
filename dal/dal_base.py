#-*-coding:utf-8-*-
'''
是所有dal层的基类  定义缓存中的数据  程序启动的时候 加入缓存
主要的方法有 增加add  查询get   修改 update  删除delete
根据k=v 判断属性  缓存处理
'''
from db.mysqlapp import MySQLApp  ## 数据库的连接通道
from tools.singleton import Singleton  ## 单立模式
from tools.utils import Utils


class Dal_base:
    __metaclass__ = Singleton
    def __init__(self):
        self._m_cache=dict()  ##说明当前的缓存是一个字典
    def add(self,mInstance):
        ##把这个对象加入到数据库
        mInstance.id=mInstance.save()
        ## 放到数据库 中 在放入缓存
        self._m_cache[mInstance.id]=mInstance
        return mInstance.id  ## 返回当前用户的id
    '''
    主要区别从客户端到数据库是通过  对象(mInstance)  的形式传输的参数
    从数据中取数据 主要是通过 模型类（modelclss）的形式把数据取出来
    '''
    def get(self,pk,modelclass):
        ## 判断PK 是否在缓存中
        if (pk in self._m_cache) == False:
            md=modelclass.get(pk)
            if md == None:
                return None
            # 如果在数据库中 就把它加入到缓存的当中
            self._m_cache[pk]=md
        return self._m_cache[pk]

    ## 修改属性
    def update(self,pk,modelclass,**kwargs):
        #pk=int(pk)
        md =None
        if(pk in self._m_cache) == False:
            md = self.get(pk, modelclass)
            self._m_cache[pk]=md  ## 如果不在缓存中 在数据库中查找后介入缓存  如果在缓存中 介入缓存
        else:
            md = self._m_cache[pk]
        for k,v in kwargs.iteritems():
            if md.__mappings__[k].innertype == 'int':
                v = (int)(v)
            elif md.__mappings__[k].innertype == 'str':
                v = Utils().any2unicode(v)

            self._m_cache[pk][k]=v
        return self._m_cache[pk].update(pk,**kwargs)
    ## 删除某条记录
    def delete(self,pk,modelclass):
        if (pk in self._m_cache) == False:
            md = self.get(pk, modelclass)
            self._m_cache[pk] = md

        self._m_cache[pk].delete(pk)
        del self._m_cache[pk]
    ## 初始化数据库
    def initDB(self,tablename,cls):
        db=MySQLApp().getInstance()
        sql="select * from "+tablename
        db.query(sql)
        result=db.fetchAllRows()
        for row in result:
            md=cls(**row)
            self._m_cache[md.id]=md

        print self._m_cache

        db.close()

    def getAllID(self):
        result=[]
        for k,v in self._m_cache.iteritems():
            result.append(k)
        return result
    ## 这个方法只局限一歌曲表中 md.songid
    def getAttrsByAllId(self,AllID,modelclass):
        attrlist=[]
        for pk in AllID:
            ## 永远是Ture
            if (pk in self._m_cache) == False:
                md=self.get(pk,modelclass)
                self._m_cache[pk]=md
            resultsongid=self._m_cache[pk].songid
            resultsongid=int(resultsongid)
            attrlist.append(resultsongid)
        for pk in AllID:
            ## 永远是Ture
            if (pk in self._m_cache) == False:
                md=self.get(pk,modelclass)
                self._m_cache[pk]=md
            resultmax=self._m_cache[pk].max
            resultmax=int(resultmax)
            attrlist.append(resultmax)

        return attrlist  ##列表前面是歌曲配置中的id　后面是每首歌的最高分


#根据某种属性返回满足条件的记录
    def getValueByAttr(self,attr,value):##主要用于判断是否该记录存在  id=1和getuserByattr相比返回一个主键
        result = []  # 返回一个    列表
        bfit = True  #self._m_cache里面装的是什么 da:User[id]={"name":"blx","age":"11","class":"clasd"}
        for k, v in self._m_cache.iteritems():##
                if isinstance(value, dict):#对象属于某个类别 value 的属性是否属于dict字典
                    for k1, v1 in value.iteritems():  ##p={a=1,b=2,c=3} id=p
                        if v[attr][k1] != v1:  ##p[id][a] != 1
                            bfit = False
                            break
                    if bfit:  ##u如果bfit 是一个true
                        result.append(k)
                else:
                    if v[attr] == value:  ##  参考第十二行：self._m_cache[newUser.id] = newUser，内存的储存形式
                        result.append(k)   ##k的值是是主键id  保存到内存里面
        return result





















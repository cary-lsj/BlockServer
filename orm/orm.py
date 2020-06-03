#!/usr/bin/env python
# -*- coding: utf-8 -*-

' Simple ORM using metaclass '

from db.mysqlapp import MySQLApp

class Field(object):
    def __init__(self, name, innertype,canset):
        self.name = name
        self.canset = canset
        self.innertype = innertype
    def __str__(self):
        return '<%s:%s>' % (self.__class__.__name__, self.name)

class StringField(Field):
    def __init__(self, name, canset):
        super(StringField, self).__init__(name,'str',canset)

class IntegerField(Field):
    def __init__(self, name,canset):
        super(IntegerField, self).__init__(name,'int',canset)

## 这个FloatField是临时添加的
class FloatField(Field):
    def __init__(self, name,canset):
        super(FloatField, self).__init__(name,'float',canset)

class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        print('Found model: %s' % name)
        mappings = dict()
        for k, v in attrs.iteritems():
            if isinstance(v, Field):
                print('Found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
        for k in mappings.iterkeys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
      #  attrs['__table__'] = name # 假设表名和类名一致
        return type.__new__(cls, name, bases, attrs)
##继承的类是 dict  字典
class Model(dict):
    __metaclass__ = ModelMetaclass

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]  ##可以理解为这个属性是否存在这 个  类中 即：表中是否有这个字段
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

#根据主键查找内容,类方法,这里必然是取单条记录
    @classmethod
    def get(cls, pk):##   根据 关键字 查询这条记录
        sql = 'select * from %s where %s=%s' % (cls.__table__, cls.__primary_key__,pk)
        db = MySQLApp().getInstance()
        db.query(sql)
        result = db.fetchOneRow()
        db.close()
        return cls(**result) if result else None  ## 他的返回值是个什么？？？？  返回的是一个类带有及个参数

#把本类所有对象全部存入db,实例方法
    def save(self):
        fields = []
        params = []  ##参考 注册 处理 程序 newUser

        for k, v in self.__mappings__.iteritems():
            if v.canset == False or getattr(self, k,None) == None :##如果不能被赋值，或则在表中没有这个字段，类中没有这个属性
                continue
            fields.append(v.name) ##意思是：为属性集合增加元素，增加的元素是v.name,v=values值
            vu = getattr(self, k, None)
            if isinstance(vu,unicode):
                vu = vu.encode('utf-8')
            if isinstance(vu,str) == False:
                vu = str(vu)
            params.append("'"+vu+"'")##  意思是：为参数集合添加元素，  增加的元素是 vu
        sql = 'insert into %s (%s) values (%s)' % (self.__table__, ','.join(fields), ','.join(params))
        print('SQL: %s' % sql)
        print('ARGS: %s' % str(params))
        db = MySQLApp().getInstance()
        pk = db.insert(sql)
        db.close()

        print(pk)

        return pk ##返回一个主键，也就是一个数字

#把部分属性更新入db,实例方法
    def update(self,pk,**kwargs):
        params = []
        for k, v in self.__mappings__.iteritems():
            #做一次属性校验，将不可更改的剔除
            if v.canset == False:
                if v.name in kwargs:
                   del kwargs[v.name]

        for k, v in kwargs.iteritems():
            if isinstance(v,unicode): ##判断是否已经编码，如果没有就utf-8编码
                v = v.encode('utf-8')
            if isinstance(v,str) == False:## value的值是否是 ‘字符串’ 如果不是，变成字符串
                v = str(v)
            params.append(k + '=' + "'" + v + "'")##;paramers是一个列表

        sql = 'update  %s set %s where %s=%s' % (self.__table__, ','.join(params),self.__primary_key__,pk)
        print('SQL: %s' % sql)
        db = MySQLApp().getInstance()
        result = db.update(sql)
        db.close()
        print(result)
        return result

    def delete(self,pk):
        sql = 'delete from %s where %s=%s' % (self.__table__, self.__primary_key__,pk)
        db = MySQLApp().getInstance()
        result = db.update(sql)  ##删除操作也是更新 主要是游标 _cur
        db.close()
        print(result)
        return  result
# testing code:
if __name__ == '__main__':
    class User(Model):
        __table__ = 'user'
        # id = IntegerField('id')
        username = StringField('username',True)
        #email = StringField('email')
        #password = StringField('password')Preferences

    u = User(username='blx3')
    u.save()

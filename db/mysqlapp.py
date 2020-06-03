#-*-coding:utf-8-*-
'''
是对 mysqlwapper 的进一步封装
'''
from tools.mysqlwapper import MySQL
from tools.singleton import Singleton
from configs.config_default import configs_default


class MySQLApp():
      u'''派生自己的app数据库类'''
      __metaclass__ = Singleton
      ## 声明一个静态的方法
      @classmethod
      def getInstance(self):
          return MySQL(configs_default['db'])
      ## 属于配置文件 在文件夹configs中 相当于 连接通道，连接数据库，并且有所有的数据表



if __name__ == '__main__':
    u'使用样式举例'
    Instance=MySQLApp().getInstance()
    sql='select * from user'
    Instance.query(sql)
    print Instance.fetchAllRows()



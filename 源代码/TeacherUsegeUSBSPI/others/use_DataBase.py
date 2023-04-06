import pymysql
from UiLibs.MyLOG import *
class Database():
    def __init__(self,username,password,dbname,port=3306,host='localhost'):
        self.user=username
        self.password=password
        self.dbname=dbname
        self.port=port
        self.host=host
        self.id=0
        #创建相关对象
        # self.createConn()

    #创建连接
    def createConn(self):
        try:
            self.conn = pymysql.connect(host='localhost', user='root', password=self.password, database=self.dbname)
            #print("数据库连接成功")
            try:
                self.cursor = self.conn.cursor()
                print("数据库连接成功")
            except:
                self.cursor = None
                logger.error("数据库连接成功，但是curse操作对象创建失败！")
        except:
            self.conn=None
            logger.error("数据库连接失败！")
    #提交
    def commit(self):
        self.conn.commit()
    #增加数据
    def ExcuteSql(self,sql):
        try:
            self.cursor.execute(sql)
            return True
        except:
            logger.error(sql+"Mysql语句执行失败！")
            return False
    #查询数据并返回tuple,每行为一个元素
    def GetData(self,sql):
        try:
            self.cursor.execute(sql)
            return self.cursor.fetchall()
        except:
            return None
    #查询最新一行数据
    def GetTheLasteData(self,tablename):
        sql=" select * FROM "+tablename+" ORDER BY id DESC LIMIT 0,1 ;"
        return self.GetData(sql)
    #清空数据表
    def ClearTable(self,tablename):
        sql="delect from "+tablename+";"
        try:
            self.cursor.execute(sql)
        except:
            pass

    def CloseConn(self,conn):
        self.conn.close()

    def CloseCursor(self,cursor):
        self.cursor.close()
    #关闭相关数据库对象
    def CloseAll(self):
        if self.cursor!=None:
            self.cursor.close()
        if self.conn!=None:
            self.conn.close()



#如何对同一张表同时进行读写*********************
# dbR = Database('root', 'a123456', 'data_ui')
# dbW = Database('root', 'a123456', 'data_ui')
#
# import threading
# import time
#
#
# class myThreadR(threading.Thread):  # 继承父类threading.Thread
#     def __init__(self,db):
#         threading.Thread.__init__(self)
#         self.db=db
#
#     def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
#        times=0
#        while times<10:
#            times+=1
#            self.db.createConn()#创建连接
#            print("读取：",self.db.GetTheLasteData('mspdata'))
#            time.sleep(0.5)
#            self.db.CloseAll()
# class myThreadW(threading.Thread):  # 继承父类threading.Thread
#     def __init__(self,db):
#         threading.Thread.__init__(self)
#         self.db=db
#
#     def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
#         index=10086
#         while index<10096:
#             self.db.createConn()#创建连接
#             print("write:"+str(index))
#             sql = r'insert into' + ' mspdata values(' + str(index) + ',1,1,1,1);'
#             self.db.ExcuteSql(sql)
#             self.db.commit()
#             self.db.CloseAll()
#             index += 1
#             time.sleep(0.5)
#
# # 创建新线程
# threadR = myThreadR(dbR)
# threadW = myThreadW(dbW)
# # 开启线程
# threadR.start()
# threadW.start()
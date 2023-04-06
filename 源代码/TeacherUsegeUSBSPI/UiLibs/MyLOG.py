#--coding:utf-8--
"""
日志注意事项：
   1- 日志文件不能太大 ---指定文件大小
   2- 日志不能太多 ---压缩文件
   3- 日志定期清空
"""
from loguru import logger
import os
import time

class ME_LOG():
    def __init__(self):
        # 生成日志路径
        self.DIR_=os.path.expanduser('logs')
        if not os.path.exists(self.DIR_):
            os.mkdir(self.DIR_)
        # 生成日期路径日志保存路径
        time_tuple = time.localtime(time.time())
        self.DIR_Day=os.path.join(self.DIR_,"{}_{}_{}".format(time_tuple[0],time_tuple[1],time_tuple[2]))
        if not os.path.exists(self.DIR_Day):
            os.mkdir(self.DIR_Day)
        #日志配置
        #日志文件存储大小配置
        self.rotation='200kb'
        #日志压缩格式
        self.compression='zip'
        #日志清理周期
        self.retention='1 days'

    #日志配置函数
    def ConfigLogger(self,rotation,compression,retention):
        self.rotation=rotation
        self.compression=compression
        self.retention=retention
    #开启日志记录
    def StartLoging(self):
        #关闭控制台输出
        logger.remove(handler_id=None)
        logFile = os.path.join(self.DIR_Day,'_{time}_.log')
        logger.add(logFile,rotation=self.rotation,compression=self.compression,retention=self.retention)
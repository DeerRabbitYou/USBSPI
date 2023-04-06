#--coding:utf-8--
from UiLibs.WriteOrReadHDF import SaveDatasToHDF,ReadDatasFromHDF
import os
import datetime
import time
import numpy as np
class OperateDatas():
    def __init__(self,SaveDir):
        self.SaveDir=SaveDir

    # 将传入参数数据保存为HDF文件
    #  将数据按SaveDir/日期/时间.h5的形式存储
    def SaveDatas(self,Datas,Index,Key):
        # 判断路径是否存在
        if not os.path.exists(self.SaveDir):
            os.makedirs(self.SaveDir)
        # 获取今天的日期
        today=datetime.date.today()
        toyear=today.strftime('%y')
        tomonth=today.strftime('%m')
        today=today.strftime('%d')
        todayPath=self.SaveDir+'/'+toyear+'/'+tomonth+'/'+today
        # 判断当前日期目录是否存在
        if not os.path.exists(todayPath):
            os.makedirs(todayPath)
        # # 判断当前日期下今天
        # # 获取当前时间
        # nowTime=time.time()
        # nowTime=time.strftime('%H_%M_%S.h5',time.gmtime(nowTime+480*60))
        # nowTimePath=todayPath+'/'+nowTime
        nowTimePath=todayPath+'/'+Index+'.h5'
        # 存储数据
        SaveDatasToHDF(Datas,nowTimePath,Key)
    # 读取指定HDF文件数据
    def ReadDats(self,filename,Key):
        # # 判断路径是否存在
        # if not os.path.exists(filename):
        #     # 文件路径不存在
        #     return [],False
        # 读取文件数据
        try:
           shape,datas=ReadDatasFromHDF(filename,Key)
           return datas, True
        except:
            return [],False
    # 存储指定关键字的数据集
    def SaveDatas_Keys(self,datas,Index,Keys):
        # 判断路径是否存在
        if not os.path.exists(self.SaveDir):
            os.makedirs(self.SaveDir)
        # 获取今天的日期
        today = datetime.date.today()
        toyear = today.strftime('%y')
        tomonth = today.strftime('%m')
        today = today.strftime('%d')
        todayPath = self.SaveDir + '/' + toyear + '/' + tomonth + '/' + today
        # 判断当前日期目录是否存在
        if not os.path.exists(todayPath):
            os.makedirs(todayPath)
        # # 判断当前日期下今天
        # # 获取当前时间
        # nowTime=time.time()
        # nowTime=time.strftime('%H_%M_%S.h5',time.gmtime(nowTime+480*60))
        # nowTimePath=todayPath+'/'+nowTime
        nowTimePath = todayPath + '/' + Index + '.h5'
        # 存储数据
        for i in range(len(Keys)):
            SaveDatasToHDF(datas[i], nowTimePath, Keys[i])
    # 读取指定HDF文件的指定关键字下的所有数据
    def ReadDatas_Keys(self,filename,Keys):
        try:
            datas=[]
            for i in Keys:
                shapes,D=ReadDatasFromHDF(filename,i)
                # print(shapes)
                datas.append(D)
            return np.array(datas).T,True
        except:
            return [],False

#     # 将数据处理为指定格式
# OD=OperateDatas('../datasDir')
# filesDay=OD.SaveDir+'/23/04/03/22_38_08.h5'
# filesDay=OD.SaveDir+'/23/04/04/13_17_15.h5'
# filesDay=OD.SaveDir+'/23/04/04/14_25_49.h5'
# print(filesDay)
# Keys = ['帧序号', '电池电压', '电路板电压', '钻压', '扭矩', '压强', '温度', '振动加速度x', '振动加速度y', '振动加速度z', '钻速']
# Keys = ['原始数据']
# import matplotlib.pyplot as plt
# datas,flag=OD.ReadDatas_Keys(filesDay,Keys)
# if flag:
#     # Datas=[]
#     # for index in range(len(datas[:,0])):
#     #
#     #     #for i in range(len(Keys)):
#     #         # print(datas[:, i])
#     #     Datas.extend(datas[index])
#     # plt.plot(Datas)
#     # plt.show()
#     pass
#     # for i in range(1,len(datas[:,0])):
#     #     if (datas[i][0]-datas[i-1][0])!=1:
#     #         Datas=datas[i-1:,0]
#     #         break
#     # print(Datas[0],Datas[1],Datas[-1])
#     # plt.plot(Datas)
#     # plt.show()
#     pass
#     print(len(datas[:,0]))
#     N=len(datas[:,0])
#     data=datas[:,0]
#     i=4
#     FrameData=[]
#     CUOWU=[]
#     while i<N:
#         if data[i]==0xaa and data[i+1]==0x55 and data[i+2]==0xaa:
#             FrameData.append([data[i+3:i+3+29]])
#             i+=32
#         else:
#             # CUOWU.extend(data[i-32:])
#             print("错误帧头：",data[i],'错误开始下标：',i)
#             print(data[i:i+100])
#             break
#     # plt.plot(CUOWU)
#     # plt.show()
#     # plt.plot(data[4:])
#     # plt.show()
# else:
#     print('读取失败！')

#encoding:utf-8
from usb2spi import *
from UiLibs.MyLOG import *
import time
import queue
import warnings
warnings.filterwarnings("ignore")
import threading
# 导出线程
class ExportThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self,MyUi,EndAddr):
        threading.Thread.__init__(self)
        self.MyUi=MyUi
        self.EndAddr=EndAddr

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        # 通信准备
        size = self.EndAddr+5
        self.MyUi.reciveLen = 0
        self.MyUi.ReciveDatas = (c_ubyte * size)()  # 申请空间大小
        everyTimeReciveLen = 20480  # 每次接收20kbyte
        reciveBuffer = (c_ubyte * everyTimeReciveLen)()
        startTime = time.time()
        # 回应判断
        self.callback=False
        # 发送命令
        sendBuffer = (c_ubyte * 5)()
        sendBuffer[0] = 0xAA
        # 地址
        sendBuffer[4] = self.EndAddr & 0xff
        sendBuffer[3] = (self.EndAddr >> 8) & 0xff
        sendBuffer[2] = (self.EndAddr >> 16) & 0xff
        sendBuffer[1] = (self.EndAddr >> 24) & 0xff
        ret = SPI_SlaveWriteBytes(self.MyUi.DevHandles[self.MyUi.DevIndex], self.MyUi.SlaveIndex, byref(sendBuffer), 5, 1000)
        if ret <= 0:
            self.MyUi.FlagEnd=0 # 命令发送失败
            return 0
        else:
            # 接收数据
            while size > self.MyUi.reciveLen:
                ret = SPI_SlaveReadBytes(self.MyUi.DevHandles[self.MyUi.DevIndex], self.MyUi.SlaveIndex, byref(reciveBuffer),
                                         everyTimeReciveLen, 1000000)
                if ret <= 0:
                    self.MyUi.FlagEnd=1 # 接收数据出现错误
                    return
                else:
                    for i in range(ret):
                        self.MyUi.ReciveDatas[self.MyUi.reciveLen] = reciveBuffer[i]
                        self.MyUi.reciveLen += 1
                        if self.MyUi.reciveLen==size:
                            return
                        if self.callback==False and self.MyUi.reciveLen==5:
                            self.callback=True
                            if self.MyUi.ReciveDatas[0]==self.MyUi.CommandExport and (self.MyUi.ReciveDatas[1] + self.MyUi.ReciveDatas[2] * 256 + self.MyUi.ReciveDatas[3] * 256 * 256 + self.MyUi.ReciveDatas[4] * 256 * 256 * 256) == self.EndAddr:
                                continue
                            else:
                                self.MyUi.FlagEnd = 2  # 地址回应错误
                                return
            self.MyUi.FlagEnd = 5  # 正确结束

#获取配置文件参数
from others.GetConfigParas import GetConfigsToDict
Configs=GetConfigsToDict() # 读取配置信息

class UsbRecive():
    def __init__(self):
        self.ExportReturnTips = {-1: "连续模式启动失败！(转接板问题)", 0: "未收到反弹命令，且连续模式关闭失败！！", 1: "未收到反弹命令",
                            2: "未收到导出模式结束符，且连续模式关闭失败！", 3: "未收到导出模式结束符",
                            4: "导出模式运行结束，但是连续模式关闭失败！", 5: "导出模式运行成功！",
                            6: "地址回应错误，且连续模式关闭失败！", 7: "地址回应错误！"}
        self.FormatReturnTips = {-1: "连续模式启动失败！(转接板问题)", 0: "未收到反弹命令，且连续模式关闭失败！！", 1: "未收到反弹命令",
                            2: "未收到格式化模式结束符，且连续模式关闭失败！", 3: "未收到格式化模式结束符，模式运行失败！",
                            4: "格式化模式运行成功！但连续模式关闭失败！", 5: "格式化模式运行成功！"}
        self.CheckFlashReturnTips = {-1: "连续模式启动失败！(转接板问题)", 0: "未收到反弹命令，且连续模式关闭失败！！", 1: "未收到反弹命令",
                                2: "未收到检查Flash模式结束符，且连续模式关闭失败！", 3: "未收到检查Flash模式结束符",
                                4: "检查Flash模式运行结束，但是连续模式关闭失败！", 5: "检查Flash模式运行成功！",
                                6: "地址回应错误，且连续模式关闭失败！", 7: "地址回应错误！"}
        self.ConfigParasReturnTips = {-1: "连续模式启动失败！(转接板问题)", 0: "未收到反弹命令，且连续模式关闭失败！！",
                                 1: "未收到反弹命令", 2: "未收到配参模式结束符，且连续模式关闭失败！", 3: "未收到配参模式结束符，模式运行失败！",
                                 4: "配参模式运行成功！但连续模式关闭失败！", 5: "配参模式运行成功"}
        self.SelfTestReturnTips = {-1: "连续模式启动失败！(转接板问题)", 0: "未收到反弹命令，且连续模式关闭失败！！", 1: "未收到反弹命令",
                              2: "未收到自测模式结束符，且连续模式关闭失败！", 3: "未收到自测模式结束符，模式运行失败！",
                              4: "自测模式运行成功！但连续模式关闭失败！", 5: "自测模式运行成功！"}
        self.ReadParasReturnTips = {-1: "连续模式启动失败！(转接板问题)", 0: "未收到反弹命令，且连续模式关闭失败！！", 1: "未收到反弹命令",
                               2: "未收到读参模式结束符，且连续模式关闭失败！", 3: "未收到读参模式结束符，模式运行失败！",
                               4: "读参模式运行成功！但连续模式关闭失败！", 5: "读参模式运行成功！"}
        self.Countnums=[]
        self.SlaveIndex = Configs['转接板初始化spi组']
        self.DevIndex = 0
        self.DevHandles = (c_uint * 20)()
        #全局变量
        self.FlagCallBack = False # 命令回应字符
        self.FlagEnd = 0 # 模式结束字符
        self.FlagDataTimeOver=False #数据超时变量
        self.CountTime_Start = 0.0
        self.DataFrameSize = 0
        self.ReciveDatas = []

        # 格式化命令
        self.CommandFormat=Configs['格式化命令'] #0x55
        # 检查Flash命令
        self.CommandCheckFlash=Configs['检查Flash命令'] #0x54
        # 检查Flash的起始地址
        self.StartAddr=[]
        # 导出模式命令
        self.CommandExport=Configs['导出命令'] #0xaa
        # 导出数据结束地址
        self.EndAddr=[]
        # 导出模式地址检查标志
        self.FlagAddrRight=False
        # 自检模式
        self.CommandSelftest=Configs['自检命令'] #0x51
        # 检查Flash模式接收长度
        self.CheackFlash_FrameLen = Configs['检查Flash接收数据长度'] #132 ： 4个地址数据+1个开始标志0x55+128个读取数据=132个数据，最后的模式结束符不算在内
        # 自检模式
        self.reciveLen=0
        self.Selftest_FrameLen = Configs['自检接收数据长度'] # 10自测数据长度：10个字节
        # 读参模式接收
        self.ReadParas_FrameLen = 4

    # 初始化设备按钮
    def initDevice(self):
        # 扫描连接设备
        if self.ScanDevice() == False:
            logger.error("设备连接失败")
            return False,1
        # 打开设备
        else:
            if self.OpenDevice() == False:
                logger.error("设备打开失败")
                return False,2
            else:
                # 配置spi
                if self.CofigSPI() == False:
                    logger.error("配置SPI失败")
                    return False,3
                else:
                    logger.info("设备以及SPI初始化成功")
                    return True,0

    # 扫描设备
    # 扫描当前连接的usb转接板设备
    def ScanDevice(self):
        ret = USB_ScanDevice(byref(self.DevHandles))
        if (ret == 0):
            logger.error("No device connected!")
            return False
        else:
            return True

    # 打开设备
    # 功能：打开指定的扫描设备
    def OpenDevice(self):
        ret = USB_OpenDevice(self.DevHandles[self.DevIndex])
        if (bool(ret)):
            return True
        else:
            return False

    # 配置spi设置
    # 功能：配置打开的转接板设备的spi信息
    def CofigSPI(self):
        self.SPIConfig = SPI_CONFIG()
        self.SPIConfig.Mode = Configs['转接板工作模式配置'] # SPI_MODE_HARD_FDX  # 硬件全双工模式
        self.SPIConfig.Master = Configs['转接板spi主从机配置'] #SPI_SLAVE  # 从机模式
        self.SPIConfig.CPOL = Configs['转接板spiCPOL配置']# 1
        self.SPIConfig.CPHA = Configs['转接板spiCPHA配置']#1
        self.SPIConfig.LSBFirst = Configs['转接板spi接收数据模式配置'] #SPI_MSB
        self.SPIConfig.SelPolarity = Configs['转接板spi片选电平配置'] # SPI_SEL_LOW #低电平从机选中
        # self.SPIConfig.ClockSpeedHz = 8000000 #10M频率
        ret = SPI_Init(self.DevHandles[self.DevIndex], self.SlaveIndex, byref(self.SPIConfig))
        if (ret != SPI_SUCCESS):
            return False
        else:
            return True

    # 关闭设备
    # 功能：关闭连接使用的usb转接板设备
    def CloseDevice(self):
        # Close device
        ret = USB_CloseDevice(self.DevHandles[self.DevIndex])
        if (bool(ret)):
            return True
        else:
            return False

    # 加速度与温度数据转换
    # 功能：转换adxl357数据
    def TransFromOneData(self,dataR,flag):
        if flag:#加速度数据转化
            SCALE = 12800  # +-40g的scale
            X = (dataR[0] & 0x0ff) + ((dataR[1] << 8) & 0x0ff00) + ((dataR[2] << 16) & 0x0ff0000) + (
                    (dataR[3] << 24) & 0x0ff000000)
            if (X & 0x800000):  # 负数
                X = ~X
                X = (X & 0x7ffff) + 1
                X = -(X / SCALE)  # 转为g单位
            else:  # 正数
                X = (X / SCALE)  # 转为g单位
            return X/16
        else:
            # 温度数据:16位
            # 无需判断，直接保存前两个字节
            T = ((dataR[1] & 0xff) << 8) + (dataR[0] & 0x0ff)
            # DAC转化:+-40g模式的精度
            T = (T & 0xffff)  # 只保留16位的温度数据
            T = 25 + (T - 1885) / (-9.05)
            return T

    # 24位符号数值转换
    def Transfrom24BtoValue(self,data):
        if data & 0x800000:# 负数
            data=~data+1
            data=data & 0x07fffff
            return -data
        else:# 正数
            return data
    # 24位特殊转换
    def Transfrom24BtoValue_S(self,data):
        if data & 0x800000:# 负数
            data= data & 0x7fffff
            return -data
        else:# 正数
            return data

    # 近钻头工程参数数据帧集合转换
    # 功能：提取接收的flash数据，解析出所有参数信息
    def TransfromParasSets(self,Datas,FrameLen,offsetIndex,offset):
        # 帧序号，电池电压，电路板电压，钻压，扭矩，压强，温度，加速度x,y,z，钻速
        result=[[],[],[],[],[],[],[],[],[],[],[]]
        datas=[]
        datas.extend(Datas[offsetIndex][0][offset:])
        for index in range(offsetIndex+1,FrameLen):
            datas.extend(Datas[index][0])
        # 0xaa,0x55,0xaa为帧头
        # 每帧数据产犊为32个字节；3+5+24
        NumLJ = 4
        # 解析数据
        i = NumLJ
        size=len(datas)
        self.reciveLen = size-4 # 实际接收数据字节数
        while i<size:
            if (i+3)<size and datas[i]==0xaa and datas[i+1]==0x55 and datas[i+2]==0xaa:
                i+=3
                if (i+29)==size or ((i + 29 +3) < size and datas[i + 29] == 0xaa and datas[i + 29 + 1] == 0x55 and datas[
                        i + 29 + 2] == 0xaa):
                    # 接收这一帧数据
                    # 1.提取数据帧序号24位，低、中、高
                    start = i
                    result[0].append(datas[start] + datas[start + 1] * 256 + datas[start + 2] * 256 * 256)  # 帧序号
                    start += 3
                    result[1].append(datas[start] / 5)  # 电池电压
                    start += 1
                    result[2].append(datas[start] / 10)  # 电路板电压
                    start += 1
                    DrP = datas[start + 2] * 256 * 256 + datas[start + 1] * 256 + datas[start]
                    result[3].append(self.Transfrom24BtoValue(DrP))  # 钻压
                    start += 3
                    Torque = datas[start + 2] * 256 * 256 + datas[start + 1] * 256 + datas[start]
                    result[4].append(self.Transfrom24BtoValue(Torque))  # 扭矩
                    start += 3
                    P = datas[start + 2] * 256 * 256 + datas[start + 1] * 256 + datas[start]
                    result[5].append(self.Transfrom24BtoValue(P))  # 压强
                    start += 3
                    Tem = datas[start + 2] * 256 * 256 + datas[start + 1] * 256 + datas[start]
                    result[6].append(self.Transfrom24BtoValue(Tem))  # 温度
                    start += 3
                    AX = datas[start + 2] * 256 * 256 + datas[start + 1] * 256 + datas[start]
                    result[7].append(self.Transfrom24BtoValue(AX))  # 加速度X
                    start += 3
                    AY = datas[start + 2] * 256 * 256 + datas[start + 1] * 256 + datas[start]
                    result[8].append(self.Transfrom24BtoValue(AY))  # 加速度Y
                    start += 3
                    AZ = datas[start + 2] * 256 * 256 + datas[start + 1] * 256 + datas[start]
                    result[9].append(self.Transfrom24BtoValue(AZ))  # 加速度Z
                    start += 3
                    DrS = datas[start + 2] * 256 * 256 + datas[start + 1] * 256 + datas[start]
                    result[10].append(self.Transfrom24BtoValue(DrS))  # 钻速
                    i+=29
            else:
                i+=1
        return result

    # 格式化模式接收数据
    # 功能：传入等待命令回应秒数和等待结束回应秒数
    # 返回：标识，模式通信结果
    # 为了让主程序不因等待通信过程卡顿，用户点击按钮后，产生线程运行此函数！！！
    def Format(self,waitCallTime,waitEndTime):#通信有确切的终止条件时
        #1.初始化全局变量标志
        self.FlagCallBack = False
        self.FlagEnd=False
        self.ReciveDatas=[]
        #2. 启动从机连续接收数据模式************************************
        pSlaveGetDataHandle = SPI_GET_DATA_HANDLE(self.SlaveGetData_Format)
        ret = SPI_SlaveContinueRead(self.DevHandles[self.DevIndex], self.SlaveIndex, pSlaveGetDataHandle)
        if (ret != SPI_SUCCESS):
            logger.error("连续模式启动失败！")
            return -1
        else:
            # 连续模式启动成功
            #2.1 发送命令
            SendBuffer = (c_ubyte * 1)()
            SendBuffer[0] = self.CommandFormat
            SPI_SlaveContinueWrite(self.DevHandles[self.DevIndex], self.SlaveIndex, SendBuffer, 1)
            #2.2 清空缓冲
            SendBuffer[0] = 0x00
            SPI_SlaveContinueWrite(self.DevHandles[self.DevIndex], self.SlaveIndex, SendBuffer, 1)
            #2.3 等待回应
            self.CountTime_Start = time.time()
            while self.FlagCallBack == False:
                if (time.time()-self.CountTime_Start)>waitCallTime:#回应超时！！！
                    break
            #2.4 回应成功？
            if self.FlagCallBack == False:#回应超时
                #结束连续接收模式
                ret = SPI_SlaveContinueWriteReadStop(self.DevHandles[self.DevIndex], self.SlaveIndex)
                if (ret != SPI_SUCCESS):
                    return 0 # 回应超时且连续模式关闭失败！！
                return 1  # 回应超时但连续模式关闭成功！！
            #2.5 等待模式结束
            self.CountTime_Start  = time.time()
            while self.FlagEnd == False:
                if (time.time()-self.CountTime_Start )>waitEndTime:#模式结束等待超时！！！
                    break
            # 结束连续接收模式
            #2.6 结束启动从机连续接收数据模式
            ret = SPI_SlaveContinueWriteReadStop(self.DevHandles[self.DevIndex], self.SlaveIndex)
            if (ret != SPI_SUCCESS):
                #2.7 根据返回信息返回提示结果
                if self.FlagEnd == False:
                    return 2
                else:
                    return 4
            else:
                if self.FlagEnd == False:
                    return 3
                else:
                    return 5

    # 格式化连续模式读数据接收回调函数
    def SlaveGetData_Format(self,DevHandle, SPIIndex, pData, DataNum):
        SPIData = (c_ubyte * DataNum)()  # 声明本地内存存储空间
        memmove(byref(SPIData), c_char_p(pData), DataNum)  # 拷贝数据到本地，DataNum为ADC数量，每个ADC有2字节，所以得拷贝DataNum*2
        if self.FlagEnd == False:  # 模式未结束
            for i in SPIData:
                if self.FlagCallBack == False:  # 未收到命令回应
                    if i == self.CommandFormat:
                        self.FlagCallBack = True  # 收到命令回应
                        continue
                else:  # 收到回应，等待模式结束
                    if i == 0x0e:
                        self.FlagEnd = True  # 收到模式成功结束回应
                        break

    # 检查Flash模式接收数据
    # 功能：传入等待命令回应秒数和等待结束回应秒数,以及读取数据的起始地址（32位数据）
    # 返回：标识，模式通信结果
    # 为了让主程序不因等待通信过程卡顿，用户点击按钮后，产生线程运行此函数！！！
    def CheckFlash(self,waitCallTime,waitEndTime,startAddr):#通信有确切的终止条件时
        #初始化标志
        self.FlagCallBack = False
        self.ReciveDatas = []
        self.reciveLen=0
        self.DataFrameSize = 0
        self.FlagEnd = False
        self.FlagAddrRight=False
        # 启动从机连续接收数据模式************************************
        pSlaveGetDataHandle = SPI_GET_DATA_HANDLE(self.SlaveGetData_CheckFlash)
        ret = SPI_SlaveContinueRead(self.DevHandles[self.DevIndex], self.SlaveIndex, pSlaveGetDataHandle)
        if (ret != SPI_SUCCESS):
            logger.error("连续模式启动失败！")
            return -1
        else:
            # 连续模式启动成功
            # 1.0发送命令：1+4=5
            SendBuffer = (c_ubyte * 5)()
            # 命令
            SendBuffer[0] = self.CommandCheckFlash
            # 地址
            SendBuffer[4] = startAddr & 0xff
            SendBuffer[3] = (startAddr >> 8) & 0xff
            SendBuffer[2] = (startAddr >> 16) & 0xff
            SendBuffer[1] = (startAddr >> 24) & 0xff
            # 保存起始地址
            self.StartAddr=SendBuffer[1:].copy()
            # 发送：命令+地址
            SPI_SlaveContinueWrite(self.DevHandles[self.DevIndex], self.SlaveIndex, SendBuffer, 5)
            # 2.0清空缓冲
            SendBuffer[0] = 0x00
            SPI_SlaveContinueWrite(self.DevHandles[self.DevIndex], self.SlaveIndex, SendBuffer, 1)
            self.CountTime_Start = time.time()
            while self.FlagCallBack == False:
                if (time.time() - self.CountTime_Start) > waitCallTime:  # 回应超时！！！
                    break
            if self.FlagCallBack == False:
                # 结束连续接收模式
                ret = SPI_SlaveContinueWriteReadStop(self.DevHandles[self.DevIndex], self.SlaveIndex)
                if (ret != SPI_SUCCESS):
                    return 0
                else:
                    return 1
            self.CountTime_Start = time.time()
            while self.FlagEnd == False:
                if (time.time() - self.CountTime_Start) > waitEndTime:  # 模式结束等待超时！！！
                    break
            # 数据通信太快了，来不及判断,直接在外面判断
            # 判断反弹地址是否正确？
            if self.FlagAddrRight == False and self.reciveLen >= 4:
                if (self.ReciveDatas[0] + self.ReciveDatas[1] * 256 + self.ReciveDatas[2] * 256 * 256 +
                    self.ReciveDatas[3] * 256 * 256 * 256) == startAddr:
                    self.FlagAddrRight = True
            # 结束连续接收模式
            ret = SPI_SlaveContinueWriteReadStop(self.DevHandles[self.DevIndex], self.SlaveIndex)
            if (ret != SPI_SUCCESS):# 连续模式关闭失败
                if self.FlagAddrRight==False:# 地址回应错误
                    return 6
                else:# 地址回应
                    if self.FlagEnd == False:
                        return 2
                    else:
                        return 4
            else:# 连续模式关闭成功
                if self.FlagAddrRight==False:# 地址回应错误
                    return 7
                else:# 地址回应
                    if self.FlagEnd == False:
                        return 3
                    else:
                        return 5

    # 检查Flash模式连续接受回调函数:其中按照通信约束，会返回1个反弹命令+4个字节地址+1个数据帧头+128个数据+1个命令结束符；注意只在受到反弹命令且结束地址正确时才进行通信。
    # 若地址数据对应不上，则通信失败！出现传递地址出现错误
    def SlaveGetData_CheckFlash(self,DevHandle, SPIIndex, pData, DataNum):
        SPIData = (c_ubyte * DataNum)()  # 声明本地内存存储空间
        memmove(byref(SPIData), c_char_p(pData), DataNum)  # 拷贝数据到本地，DataNum为ADC数量，每个ADC有2字节，所以得拷贝DataNum*2
        if self.FlagEnd == False:  # 模式未结束
            i = 0
            while i < DataNum:
                # 首先判断有没有收到命令回应
                if self.FlagCallBack == False:
                    if SPIData[i] == self.CommandCheckFlash:  # 回应
                        self.FlagCallBack = True
                        i += 1
                        continue
                    else:
                        i += 1
                elif self.DataFrameSize > 0:
                    if (DataNum - i) >= self.DataFrameSize:
                        self.ReciveDatas.extend(SPIData[i:i + self.DataFrameSize])
                        i += self.DataFrameSize
                        self.reciveLen += self.DataFrameSize # 接收数据长度
                        self.DataFrameSize = 0
                        continue
                    else:
                        self.ReciveDatas.extend(SPIData[i:DataNum])
                        self.reciveLen += (DataNum - i)  # 接收数据长度
                        self.DataFrameSize -= (DataNum - i)
                        break
                # 判断是何种帧
                else:
                    if SPIData[i] == 0x55:
                        self.DataFrameSize = self.CheackFlash_FrameLen
                        i += 1
                        continue
                    if SPIData[i] == 0xff:  # 结束命令
                        self.FlagEnd = True
                        break

    # 配置参数模式接收数据
    # 功能：传入等待命令回应秒数和等待结束回应秒数
    # 返回：标识，模式通信结果
    # 为了让主程序不因等待通信过程卡顿，用户点击按钮后，产生线程运行此函数！！！
    def ConfigParas(self,waitCallTime,waitEndTime,ConfigParas):#通信有确切的终止条件时
        #初始化标志
        self.FlagCallBack = False
        self.FlagEnd = False
        # 启动从机连续接收数据模式************************************
        pSlaveGetDataHandle = SPI_GET_DATA_HANDLE(self.SlaveGetData_ConfigParas)
        ret = SPI_SlaveContinueRead(self.DevHandles[self.DevIndex], self.SlaveIndex, pSlaveGetDataHandle)
        if (ret != SPI_SUCCESS):
            logger.error("连续模式启动失败！")
            return -1
        else:
            # 连续模式启动成功
            # 1.0发送命令
            SendBuffer = (c_ubyte * 1000)()
            SendBuffer[0] = 0x05
            #配置参数
            for i in range(len(ConfigParas)):
                SendBuffer[i+1]=ConfigParas[i]
            #发送帧长
            SendSize=len(ConfigParas)+1
            SPI_SlaveContinueWrite(self.DevHandles[self.DevIndex], self.SlaveIndex, SendBuffer, SendSize)
            # 2.0清空缓冲
            SendBuffer[0] = 0x00
            SPI_SlaveContinueWrite(self.DevHandles[self.DevIndex], self.SlaveIndex, SendBuffer, 1)
            self.CountTime_Start = time.time()
            while self.FlagCallBack == False:
                if (time.time()-self.CountTime_Start) > waitCallTime:  # 回应超时！！！
                    break
            if self.FlagCallBack==False:
                # 结束连续接收模式
                ret = SPI_SlaveContinueWriteReadStop(self.DevHandles[self.DevIndex], self.SlaveIndex)
                if (ret != SPI_SUCCESS):
                    return 0
                else:
                    return 1
            self.CountTime_Start = time.time()
            while self.FlagEnd == False:
                if (time.time()-self.CountTime_Start) > waitEndTime:  # 回应超时！！！
                    break
            # 结束连续接收模式
            ret = SPI_SlaveContinueWriteReadStop(self.DevHandles[self.DevIndex], self.SlaveIndex)
            if (ret != SPI_SUCCESS):
                if self.FlagEnd == False:
                    return 2
                else:
                    return 4
            else:
                if self.FlagEnd == False:
                    return 3
                else:
                    return 5

    # 配参模式连续接收回调函数
    def SlaveGetData_ConfigParas(self,DevHandle, SPIIndex, pData, DataNum):
        SPIData = (c_ubyte * DataNum)()  # 声明本地内存存储空间
        memmove(byref(SPIData), c_char_p(pData), DataNum)  # 拷贝数据到本地，DataNum为ADC数量，每个ADC有2字节，所以得拷贝DataNum*2
        if self.FlagEnd ==False:
            for i in SPIData:
                if i == 0x05:
                    self.FlagCallBack = True  # 收到命令回应
                    break
                if i == 0x0e:
                    self.FlagEnd = True  # 收到模式结束回应
                    break

    # 导出模式接收数据
    # 功能：传入等待命令回应秒数和等待结束回应秒数，以及导出终止地址EndAddr
    # 返回：标识，模式通信结果
    # 为了让主程序不因等待通信过程卡顿，用户点击按钮后，产生线程运行此函数！！！
    def Export(self, waitCallTime, waitEndTime,waitOkTime,EndAddr):  # 通信有确切的终止条件时
        #1.0 初始化标志
        self.FlagCallBack = False
        self.ReciveDatas=(c_ubyte * (260*1024*1024))()
        self.FlagEnd=False
        self.FlagAddrRight=False
        self.FlagDataTimeOver=False
        self.reciveLen=0
        self.MaxSize=EndAddr
        self.EndAddr=[]

        self.Times=[]
        self.sizes=[]
        self.Lock = threading.Lock()

        #2.0 启动从机连续接收数据模式************************************
        pSlaveGetDataHandle = SPI_GET_DATA_HANDLE(self.SlaveGetData_Export)
        ret = SPI_SlaveContinueRead(self.DevHandles[self.DevIndex], self.SlaveIndex, pSlaveGetDataHandle)
        if (ret != SPI_SUCCESS):
            logger.error("连续模式启动失败！")
            return -1
        else:
            # 连续模式启动成功
            #2.1 发送命令：1+4=5
            SendBuffer = (c_ubyte * 5)()
            # 命令
            SendBuffer[0] = self.CommandExport
            # 地址
            SendBuffer[4] = EndAddr & 0xff
            SendBuffer[3] = (EndAddr >> 8) & 0xff
            SendBuffer[2] = (EndAddr >> 16) & 0xff
            SendBuffer[1] = (EndAddr >> 24) & 0xff
            # 保存结束地址
            self.EndAddr=SendBuffer[1:].copy()
            # 发送命令+地址
            SPI_SlaveContinueWrite(self.DevHandles[self.DevIndex], self.SlaveIndex, SendBuffer, 5)
            #2.2 清空缓冲
            SendBuffer[0] = 0x00
            SendBuffer[1] = 0x00
            SendBuffer[2] = 0x00
            SendBuffer[3] = 0x00
            SendBuffer[4] = 0x00
            SPI_SlaveContinueWrite(self.DevHandles[self.DevIndex], self.SlaveIndex, SendBuffer, 1)
            #2.3 等待命令回应
            self.CountTime_Start = time.time()
            while self.FlagCallBack==False:
                if (time.time() - self.CountTime_Start) > waitCallTime:  # 超时判定
                    break
                else:
                    time.sleep(0.5)
                    pass
            #2.4 判断回应情况
            if self.FlagCallBack == False:
                # 结束连续接收模式
                ret = SPI_SlaveContinueWriteReadStop(self.DevHandles[self.DevIndex], self.SlaveIndex)
                if (ret != SPI_SUCCESS):
                    return 0
                else:
                    return 1
            #2.5 等待模式结束
            self.CountTime_Start=time.time()#更新开始时间
            while self.FlagDataTimeOver==False:
                if (time.time()-self.CountTime_Start)>waitEndTime:#超时判定
                    self.FlagDataTimeOver=True
                    break
                # 检查返回地址是否正确!!!
                elif self.FlagAddrRight==False and self.reciveLen>=4:
                    if (self.ReciveDatas[0]+ self.ReciveDatas[1]*256+self.ReciveDatas[2]*256*256+ self.ReciveDatas[3]*256*256*256)==EndAddr:
                        self.FlagAddrRight=True
                    else:# 地址不正确
                        break
                else:
                    time.sleep(0.5)
                    pass

            #2.6 结束连续接收模式
            ret = SPI_SlaveContinueWriteReadStop(self.DevHandles[self.DevIndex], self.SlaveIndex)
            if (ret != SPI_SUCCESS):
                #2.7 根据情况返回
                if self.FlagAddrRight==False:
                    return 6
                else:
                    # 注意：导出模式正常运行结束时，得到的接收数据的前四个字节数据是返回地址
                    if self.FlagEnd == False: # 连续模式结束失败、返回地址正确、但是结束未收到0xff
                        return 2
                    else:
                        return 4
            else:
                if self.FlagAddrRight==False:
                    return 7
                else:
                    # 注意：导出模式正常运行结束时，得到的接收数据前4个字节数据是返回地址
                    if self.FlagEnd == False: # 连续模式结束、返回地址正确、但未收到0xff
                        return 3
                    else:
                        return 5

    # 地址不正确，则将表面那个数据错误
    def SlaveGetData_Export(self,DevHandle, SPIIndex, pData, DataNum):
        self.Lock.acquire()
        times=time.time()
        SPIData = (c_ubyte * DataNum)()  # 声明本地内存存储空间
        memmove(byref(SPIData), c_char_p(pData), DataNum)  # 拷贝数据到本地，DataNum为ADC数量，每个ADC有2字节，所以得拷贝DataNum*2
        # 来数据就收
        if self.FlagEnd==False:
            if self.FlagDataTimeOver == False:  # 默认
                if self.FlagCallBack == False:  # 没有收到回应
                    i = 0
                    while i < DataNum:
                        # 首先判断有没有收到命令回应
                        if SPIData[i] == self.CommandExport:  # 回应
                            i += 1
                            if i < DataNum:  # 保存数据
                                for i in range(i,DataNum):
                                    self.ReciveDatas[self.reciveLen]=SPIData[i]
                                    self.reciveLen += 1
                            self.FlagCallBack = True
                            break
                        else:
                            i += 1
                else:  # 不断接收数据
                    self.CountTime_Start = time.time()  # 更新开始时间
                    for i in range(DataNum):
                        self.ReciveDatas[self.reciveLen] = SPIData[i]
                        self.reciveLen+=1
                        if self.reciveLen==self.MaxSize:
                            break
                # 保存时间和数据量
                self.Times.append(time.time()-times)
                self.sizes.append(DataNum)
            else:
                pass
        self.Lock.release()

    def ExportNew(self, waitCallTime, waitEndTime,EndAddr):  # 通信有确切的终止条件时
        #1.0 初始化标志
        self.FlagCallBack = False
        self.ReciveDatas=[]
        self.Message=queue.Queue()
        self.FrameLen=0
        self.startFrameindex=0
        self.startFrameOffset=0
        # 创建线程锁
        self.Lock=threading.Lock()
        self.Times=[]
        self.Lens=[]

        self.FlagEnd=False
        self.FlagAddrRight=False
        self.FlagDataTimeOver=False
        self.reciveLen=0
        self.MaxSize=EndAddr
        self.EndAddr=[]
        starts=time.time()
        #2.0 启动从机连续接收数据模式************************************
        pSlaveGetDataHandle = SPI_GET_DATA_HANDLE(self.ExportNew_Slave)
        ret = SPI_SlaveContinueRead(self.DevHandles[self.DevIndex], self.SlaveIndex, pSlaveGetDataHandle)
        if (ret != SPI_SUCCESS):
            logger.error("连续模式启动失败！")
            return -1
        else:
            # 连续模式启动成功
            #2.1 发送命令：1+4=5
            SendBuffer = (c_ubyte * 5)()
            # 命令
            SendBuffer[0] = self.CommandExport
            # 地址
            SendBuffer[4] = EndAddr & 0xff
            SendBuffer[3] = (EndAddr >> 8) & 0xff
            SendBuffer[2] = (EndAddr >> 16) & 0xff
            SendBuffer[1] = (EndAddr >> 24) & 0xff
            # 保存结束地址
            self.EndAddr=SendBuffer[1:].copy()
            # 发送命令+地址
            SPI_SlaveContinueWrite(self.DevHandles[self.DevIndex], self.SlaveIndex, SendBuffer, 5)
            #2.2 清空缓冲
            SendBuffer[0] = 0x00
            SPI_SlaveContinueWrite(self.DevHandles[self.DevIndex], self.SlaveIndex, SendBuffer, 1)
            #2.3 等待命令回应
            self.CountTime_Start = time.time()
            readindex=0
            time.sleep(0.5)
            # 检查回应
            while self.FlagCallBack==False: # 等待回应
                now=self.Message.qsize()
                if now>readindex:# 当接收数据帧数大于当前已读数据帧数时
                    for i in range(readindex,now):# 遍历新接收的数据帧
                        datas=self.ReciveDatas[i]# 获取数据帧
                        data=datas[0]
                        size=datas[1]
                        for j in range(size):# 遍历判断回应和地址
                            if data[j]==self.CommandExport:
                                self.FlagCallBack=True
                                if j==(size-1):# 确定接收数据的偏移下标
                                    self.startFrameindex=i+1
                                    self.startFrameOffset=0
                                else:# 确定接收数据的偏移下标
                                    self.startFrameindex = i
                                    self.startFrameOffset = j + 1
                                break
                        if self.FlagCallBack:
                            break
                    if self.FlagCallBack:
                        break
                    readindex=now # 修改已读的帧数
                time.sleep(0.5)  # 判断延时
                if (time.time()-self.CountTime_Start)>=waitCallTime:
                    break
            # 延时等待一段时间
            if self.FlagCallBack==False:
                ret = SPI_SlaveContinueWriteReadStop(self.DevHandles[self.DevIndex], self.SlaveIndex)
                if (ret != SPI_SUCCESS):
                    return 0
                else:
                    return 1
            else:# 回应
                # 接收数据
                self.CountTime_Start = time.time()
                re=0
                while self.FlagEnd==False:
                    Now=self.Message.qsize()
                    if re<Now:
                        self.CountTime_Start=time.time()
                        re=Now
                    elif (time.time()-self.CountTime_Start)>=waitEndTime:
                        self.FlagEnd=True
                    else:
                        pass
                    time.sleep(1)
                ret = SPI_SlaveContinueWriteReadStop(self.DevHandles[self.DevIndex], self.SlaveIndex)
                if (ret != SPI_SUCCESS):
                    return 2
                else:
                    return 3

    def ExportNew_Slave(self,DevHandle, SPIIndex, pData, DataNum):
        # times=time.time()
        SPIData = (c_ubyte * DataNum)()  # 声明本地内存存储空间
        memmove(byref(SPIData), c_char_p(pData), DataNum)  # 拷贝数据到本地，DataNum为ADC数量，每个ADC有2字节，所以得拷贝DataNum*2
        self.Lock.acquire()
        self.ReciveDatas.append([SPIData,DataNum])
        self.FrameLen+=1
        self.Message.put(1)
        # self.Times.append(time.time()-times)
        # self.Lens.append(DataNum)
        self.reciveLen+=DataNum
        self.Lock.release()

    # 自测模式接收数据
    # 功能：传入等待命令回应秒数和等待结束回应秒数
    # 返回：标识，模式通信结果
    # 为了让主程序不因等待通信过程卡顿，用户点击按钮后，产生线程运行此函数！！！
    def SelfTest(self, waitCallTime, waitEndTime):  # 通信有确切的终止条件时
        # 初始化标志
        self.DataFrameSize=0
        self.ReciveDatas = []
        self.reciveLen=0
        self.FlagCallBack = False
        self.FlagEnd = False
        # 启动从机连续接收数据模式************************************
        pSlaveGetDataHandle = SPI_GET_DATA_HANDLE(self.SlaveGetData_SelfTest)
        ret = SPI_SlaveContinueRead(self.DevHandles[self.DevIndex], self.SlaveIndex, pSlaveGetDataHandle)
        if (ret != SPI_SUCCESS):
            logger.error("连续模式启动失败！")
            return -1
        else:
            # 连续模式启动成功
            # 1.0发送命令
            SendBuffer = (c_ubyte * 1)()
            SendBuffer[0] = self.CommandSelftest
            SPI_SlaveContinueWrite(self.DevHandles[self.DevIndex], self.SlaveIndex, SendBuffer, 1)
            # 2.0清空缓冲
            SendBuffer[0] = 0x00
            SPI_SlaveContinueWrite(self.DevHandles[self.DevIndex], self.SlaveIndex, SendBuffer, 1)
            self.CountTime_Start = time.time()
            while self.FlagCallBack == False:
                if (time.time()-self.CountTime_Start) > waitCallTime:  # 回应超时！！！
                    break
            if self.FlagCallBack == False:
                # 结束连续接收模式
                ret = SPI_SlaveContinueWriteReadStop(self.DevHandles[self.DevIndex], self.SlaveIndex)
                if (ret != SPI_SUCCESS):
                    return 0
                else:
                    return 1
            self.CountTime_Start = time.time()  # 更新开始时间
            while self.FlagEnd==False:
                if (time.time() - self.CountTime_Start) > waitEndTime:  # 超时判定
                    break
            # 结束连续接收模式
            ret = SPI_SlaveContinueWriteReadStop(self.DevHandles[self.DevIndex], self.SlaveIndex)
            if (ret != SPI_SUCCESS):
                if self.FlagEnd==False:
                    return 2
                else:
                    return 4
            else:
                if self.FlagEnd==False:
                    return 3
                else:
                    return 5

    # 导出模式连续接收回调函数
    def SlaveGetData_SelfTest(self,DevHandle, SPIIndex, pData, DataNum):
        SPIData = (c_ubyte * DataNum)()  # 声明本地内存存储空间
        memmove(byref(SPIData), c_char_p(pData), DataNum)  # 拷贝数据到本地，DataNum为ADC数量，每个ADC有2字节，所以得拷贝DataNum*2
        if self.FlagEnd == False:  # 模式未结束
            i = 0
            while i < DataNum:
                # 首先判断有没有收到命令回应
                if self.FlagCallBack == False:
                    if SPIData[i] == self.CommandSelftest:  # 回应
                        self.FlagCallBack = True
                        i += 1
                        continue
                    else:
                        i += 1
                # 是否正在接收帧数据
                elif self.DataFrameSize > 0:
                    if (DataNum - i) >= self.DataFrameSize:
                        self.ReciveDatas.extend(SPIData[i:i + self.DataFrameSize])
                        i += self.DataFrameSize
                        self.reciveLen+=self.DataFrameSize
                        self.DataFrameSize= 0
                        continue
                    else:
                        self.ReciveDatas.extend(SPIData[i:DataNum])
                        self.DataFrameSize -= (DataNum - i)
                        self.reciveLen+=(DataNum - i)
                        break
                # 判断是何种帧
                else:
                    if SPIData[i] == 0x55:  # 收到数据帧
                        # 刷新等待时间
                        # self.CountTime_Start = time.time()
                        self.DataFrameSize = self.Selftest_FrameLen
                        i += 1
                        continue
                    if SPIData[i] == 0xff:  # 结束命令
                        self.FlagEnd = True
                        break

    # 读参模式接收数据
    # 功能：传入等待命令回应秒数和等待结束回应秒数
    # 返回：标识，模式通信结果
    # 为了让主程序不因等待通信过程卡顿，用户点击按钮后，产生线程运行此函数！！！
    def ReadParas(self, waitCallTime, waitEndTime):  # 通信有确切的终止条件时
        # 初始化标志
        self.ReciveDatas = []
        self.FlagCallBack = False
        self.FlagEnd = False
        self.reciveLen=0
        # 启动从机连续接收数据模式************************************
        pSlaveGetDataHandle = SPI_GET_DATA_HANDLE(self.SlaveGetData_ReadParas)
        ret = SPI_SlaveContinueRead(self.DevHandles[self.DevIndex], self.SlaveIndex, pSlaveGetDataHandle)
        if (ret != SPI_SUCCESS):
            logger.error("连续模式启动失败！")
            return -1
        else:
            # 连续模式启动成功
            # 1.0发送命令
            SendBuffer = (c_ubyte * 1)()
            SendBuffer[0] = 0x06
            SPI_SlaveContinueWrite(self.DevHandles[self.DevIndex], self.SlaveIndex, SendBuffer, 1)
            # 2.0清空缓冲
            SendBuffer[0] = 0x00
            SPI_SlaveContinueWrite(self.DevHandles[self.DevIndex], self.SlaveIndex, SendBuffer, 1)
            self.CountTime_Start = time.time()
            while self.FlagCallBack == False:
                if (time.time()-self.CountTime_Start) > waitCallTime:  # 回应超时！！！
                    break
            if self.FlagCallBack == False:
                # 结束连续接收模式
                ret = SPI_SlaveContinueWriteReadStop(self.DevHandles[self.DevIndex], self.SlaveIndex)
                if (ret != SPI_SUCCESS):
                    return 0
                else:
                    return 1
            self.CountTime_Start = time.time()  # 更新开始时间
            while self.FlagEnd==False:
                if (time.time() - self.CountTime_Start) > waitEndTime:  # 超时判定
                    break
            # 结束连续接收模式
            ret = SPI_SlaveContinueWriteReadStop(self.DevHandles[self.DevIndex], self.SlaveIndex)
            if (ret != SPI_SUCCESS):
                if self.FlagEnd==False:
                    return 2
                else:
                    return 4
            else:
                if self.FlagEnd==False:
                   return 3
                else:
                   return 5

    # 读参模式连续接收回调函数
    def SlaveGetData_ReadParas(self,DevHandle, SPIIndex, pData, DataNum):
        SPIData = (c_ubyte * DataNum)()  # 声明本地内存存储空间
        memmove(byref(SPIData), c_char_p(pData), DataNum)  # 拷贝数据到本地，DataNum为ADC数量，每个ADC有2字节，所以得拷贝DataNum*2
        if self.FlagEnd == False:  # 模式未结束
            i = 0
            while i < DataNum:
                # 首先判断有没有收到命令回应
                if self.FlagCallBack == False:
                    if SPIData[i] == 0x06:  # 回应
                        self.FlagCallBack = True
                        i += 1
                        continue
                    else:
                        i += 1
                # 是否正在接收帧数据
                elif self.DataFrameSize > 0:
                    if (DataNum - i) >= self.DataFrameSize:
                        self.ReciveDatas.extend(SPIData[i:i + self.DataFrameSize])
                        self.reciveLen+=(self.DataFrameSize)
                        i += self.DataFrameSize
                        self.DataFrameSize = 0
                        continue
                    else:
                        self.ReciveDatas.extend(SPIData[i:DataNum])
                        self.reciveLen += (DataNum-i)
                        self.DataFrameSize -= (DataNum - i)
                        break
                # 判断是何种帧
                else:
                    if SPIData[i] == 0x55:
                        self.DataFrameSize = self.ReadParas_FrameLen  # 假设接收4个字节
                        i += 1
                        continue
                    if SPIData[i] == 0xff:  # 结束命令
                        self.FlagEnd = True
                        break

#encoding:utf-8
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
import pyqtgraph as pg
from UiLibs.MyUi import Ui_MainWindow
from UsbReciveData import UsbRecive
from UiLibs.MyLOG import *
from ctypes import *
from UiLibs.save_get_Datas import OperateDatas
from UiLibs.TransfromFile import TF

#数据库操作
#symbol类型
symbols={0:'o',1:'t',2:'t1',3:'t2',4:'t3',5:'s',6:'p',7:'h',8:'star',9:'+',10:'d',11:'arrow_down',12:'arrow_left',13:'arrow_up',14:'arrow_right'}
#spi传输配置标识
spi_msb=0
spi_lsb=1
spi_mode1=0
spi_mode2=1
spi_mode3=2
spi_mode4=3
#当前界面为那个单片机工作：标签标识
FLAG_Chip_DSP=0x00
FLAG_Chip_MSP=0x01

#获取配置文件参数
from others.GetConfigParas import GetConfigsToDict
Configs=GetConfigsToDict() # 读取配置信息
import threading
import time
class myThread(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, MyUi,flag):
        threading.Thread.__init__(self)
        self.MyUi=MyUi
        self.flag=flag

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        logger.info("模式进入")
        if self.flag==1:
            self.ret=self.MyUi.USBR.Format(1,Configs['格式化模式等待结束的最大等待时间'])
        if self.flag==2:
            logger.info("启动检查Flash模式，检查开始地址为："+str(self.MyUi.CheckFlashStartAddr))
            self.ret = self.MyUi.USBR.CheckFlash(1, 20,self.MyUi.CheckFlashStartAddr)
        if self.flag==3:
            logger.info("启动导出模式，导出结束地址为：" + str(self.MyUi.ExportEndAddr))
            self.ret = self.MyUi.USBR.ExportNew(2, 4,self.MyUi.ExportEndAddr)
            # self.ret=self.MyUi.USBR.ExportNew(self.MyUi.ExportEndAddr)
        if self.flag==4:
            self.ret = self.MyUi.USBR.SelfTest(1, 3)
        if self.flag==5:
            self.ret = self.MyUi.USBR.ReadParas(1, 3)
        if self.flag==6:
            SendBuffer = (c_ubyte * 4)()
            for i in range(4):
                SendBuffer[i] = 0x55
            self.ret = self.MyUi.USBR.ConfigParas(1, 2, SendBuffer)
        # 修改模式完成标志
        self.MyUi.ModeFinish = self.ret
        logger.info("模式退出！")

class myThread_SaveExportDatas(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, MyUi):
        threading.Thread.__init__(self)
        self.MyUi=MyUi
    def run(self):
        # 将数据进行分帧处理
        datas = self.MyUi.USBR.TransfromParasSets(self.MyUi.USBR.ReciveDatas, self.MyUi.USBR.FrameLen, self.MyUi.USBR.startFrameindex,
                                             self.MyUi.USBR.startFrameOffset)
        # 帧序号，电池电压，电路板电压，钻压，扭矩，压强，温度，加速度x,y,z，钻速
        # 保存数据
        Keys = ['帧序号', '电池电压', '电路板电压', '钻压', '扭矩', '压强', '温度', '振动加速度x', '振动加速度y', '振动加速度z', '钻速']
        filename = time.strftime('%H_%M_%S', time.localtime())
        self.MyUi.DataOP.SaveDatas_Keys(datas, filename, Keys)
        self.MyUi.SaveDatasFinish=True

class UI(QMainWindow,Ui_MainWindow):
    def __init__(self,flag_chip,parent=None):
        super(UI, self).__init__(parent)
        self.setupUi(self)
        self.setWindowIcon(QIcon(Configs['软件icon路径']))
        #****************************软件启动首先要配置日志对象，以方便其他文件使用
        # 创建日志对象
        self.ME_LOG = ME_LOG()
        # 启动日志记录
        self.ME_LOG.StartLoging()
        # 启动记录
        times = time.localtime(time.time())
        logger.info("软件在时间点{}时{}分{}秒启动！", times[3], times[4], times[5])

        # 初始化不使能
        self.DisEnaDrawSys()
        self.win=pg.GraphicsLayoutWidget(show=True,title='绘图区域')
        self.win.setBackground(Configs['绘图控件的背景颜色'])
        self.setWindowTitle(Configs['软件名称'])
        self.DrawLayout.addWidget(self.win)

        # 子图字典创建
        self.subplots={}
        # 启动数据库读取计时器
        self.DrawFlag = False
        # 算法执行标志
        self.AlFlag={'Kalman':False,'Mean':False}
        # 绘图
        self.DrawData_Now=[]
        self.DrawFrameIndexs=[]
        self.DrawDataIndex=-1
        self.DrawDataMaxsize=0
        self.DrawTimer = QTimer()
        self.DrawTimer.timeout.connect(self.RefreshDataFromMSPDatabase)
        self.DrawF=Configs['初始绘图速度'] #绘图速度
        # 转换文件存储路径
        self.TFSaveDir=Configs['转换文件存储目录']
        AbsPath=os.path.abspath(self.TFSaveDir)
        self.SaveRoadEdit.setText(AbsPath)
        self.SaveRoadEdit.setEnabled(False)
        # 创建文件转换对象
        self.FilesTransfrom=TF(self.TFSaveDir,'')
        # 文件区间记录
        self.FileBoundDict={}


        # 数据通信参量定义*********************
        # 创建转接板对象
        self.USBR = UsbRecive()

        # self.DisEnaUndContralSys() # 只有初始化成功后才会使能模式按钮
        # 模式按钮绑定函数
        self.ModeBounds()
        # 当前模式运行标志类型，
        self.ModeFlag = Configs['主程序所有模式非运行状态标志']
        # 模式完成标志
        self.ModeFinish = Configs['所有模式完成标志的初始值']
        # 模式监视定时器
        self.TimeWatch = QTimer()
        self.TimeWatch.timeout.connect(self.Watch)
        # 检查Flash模式开始地址初始化为0
        self.CheckFlashStartAddr=0
        # 导出模式结束地址初始化为128
        self.ExportEndAddr=128
        # 数据存储、读取对象
        # 导出数据存储定时器
        self.SaveExportDatasTimer=QTimer()
        self.SaveExportDatasTimer.timeout.connect(self.WatchSaveData)
        self.SaveDatasFinish=False

        # 数据存储文件夹
        self.DatasPath=Configs['绘图文件存储根目录路径']
        self.DataOP=OperateDatas(self.DatasPath)
        # 绘图点击相关变量
        self.ClickData=() # 点击位置绘图曲线点数据
        self.ClickNewData=False # 当前鼠标移动位置数据是否有效
        self.ClickSubPlotIndex=-1# 当前点击子图的下标
        # 接收数据按名称对应下标
        self.title_to_index={}
        for i,v in enumerate(['温度','振动加速度x','振动加速度y','振动加速度z','扭矩','压强','钻压','钻速']):
            self.title_to_index[v]=i
        # 按钮样式
        self.styleButtonGreen = "QPushButton{background-color: "+Configs['按钮初始颜色']+"}\
                     QPushButton{font-family: "+Configs['字体类型']+";font-size:"+str(Configs['字体大小'])+"}\
                    QPushButton:hover{background-color:"+Configs['按钮悬停颜色']+"}\
                    QPushButton:pressed{background-color:"+Configs['按钮按下颜色']+"}\
                    "+Configs['按钮样式']
        self.styleButtonRed="QPushButton{background-color: "+Configs['按钮工作中颜色']+"}\
                     QPushButton{font-family: "+Configs['字体类型']+";font-size:"+str(Configs['字体大小'])+"}\
                    QPushButton:hover{background-color:"+Configs['按钮悬停颜色']+"}\
                    QPushButton:pressed{background-color:"+Configs['按钮按下颜色']+"}\
                    "+Configs['按钮样式']


        if flag_chip==FLAG_Chip_MSP:#当前界面为MSP单片机工作
            # 子图绘图点击数据显示Label
            self.pgLabel = pg.LabelItem(justify='left')  # 数据显示label
            self.pgLabel.setFixedHeight(10)
            self.pgLabel.setFixedWidth(100)
            self.win.addItem(self.pgLabel)

            # 初始子图绘制
            self.ShowTitles = []
            # 初始界面的绘图区域显示
            for title in self.ShowTitles:
                self.CreateSubPlot(title=title)
                self.CreateCurveAndSerie(title)
            # 附加的触发事件:子图的变化
            self.UndControl.triggered.connect(self.UndDrawInit)
            self.DrawControl.triggered.connect(self.DrawInit)
            self.ReDrawButton.clicked.connect(self.ReDrawSubPlots)

        # 配置参数信息显示action触发事件
        self.ParaDisc.triggered.connect(self.ShowParameters)
        self.ButtonConects()#按钮绑定事件
        self.OtherConnects()#其他事件绑定函数

    # label显示数据
    def SetLabelText(self,Text):
        self.pgLabel.setText(Text)

    # 存储导出数据的定时器函数
    def WatchSaveData(self):
        if self.SaveDatasFinish:
            # 存储结束
            # 1.使能软件
            self.EnableSoft()
            # 2.关闭定时器
            self.SaveExportDatasTimer.stop()
            self.SaveDatasFinish=False
            # 3.输出提示
            QMessageBox.about(self, '运行且存储成功',self.USBR.ExportReturnTips[5] + '接收字节个数：' + str(self.USBR.reciveLen))

    # 井下系统控制区点击后，绘图区根据显示需要创建子图
    def UndDrawInit(self):
        # 如果正在绘图，则不能切换绘图子图
        if self.DrawFlag==True:
            return
        # 首先删除原来的所有子图
        for title in self.ShowTitles:
            self.DeleteSubPlot(title)
        # 创建需要显示的子图
        self.ShowTitles=[]
        self.setStatusTip('点击井下系统控制区')

    # 绘图区域点击后，保持原来的绘制
    def DrawInit(self):
        # 不能直接删除原来子图的信息
        # 为了保持数据的连续性
        if self.ShowTitles!=[]:
            return
        # 删除当前label数据
        self.SetLabelText('')
        # 首先删除原来的所有子图
        for title in self.ShowTitles:
            self.DeleteSubPlot(title)
        # 创建需要显示的子图
        self.ShowTitles = self.SubPlotsShowSelect.Selectlist()
        for title in self.ShowTitles:
            self.CreateSubPlot(title=title)
            self.CreateCurveAndSerie(title)

    # 检查Flash模式返回数据绘图
    def DrawCheckFlashInit(self):
        # 删除当前label数据
        self.SetLabelText('')
        # 首先删除原来的所有子图
        for title in self.ShowTitles:
            self.DeleteSubPlot(title)
        # 创建需要显示的子图
        self.ShowTitles =[Configs['检查Flash模式绘图标题']]
        for title in self.ShowTitles:
            self.CreateSubPlot(title=title)
            self.CreateCurveAndSerie(title)

    # 重绘子图
    def ReDrawSubPlots(self):
        # 删除当前label数据
        self.SetLabelText('')
        # 获取选择
        selects=self.SubPlotsShowSelect.Selectlist()
        # 删除：已经绘制的，但是当前未被选中
        for title in self.ShowTitles:
            if title not in selects:
                self.DeleteSubPlot(title)
        # 增加：当前选中的，但是还未绘制的
        for title in selects:
            if title not in self.ShowTitles:
                self.CreateSubPlot(title=title)
                self.CreateCurveAndSerie(title)
        # 更新绘图标题
        self.ShowTitles=selects

    # 模式按钮绑定函数
    def ModeBounds(self):
        self.ModelFormat.clicked.connect(self.Format)
        self.ModelCheckFlash.clicked.connect(self.CheckFlash)
        self.ModelExport.clicked.connect(self.Export)
        self.ModelSelftest.clicked.connect(self.Selftest)

    # 模式监视函数
    def Watch(self):
        if self.ModeFlag==Configs['主程序格式化模式运行标志']:
            if self.ModeFinish!=Configs['所有模式完成标志的初始值']:# 模式结束
                if self.ModeFinish==5:# 正常结束
                    logger.info("格式化模式运行成功！！！")
                    QMessageBox.about(self,'运行结果',self.USBR.FormatReturnTips[self.ModeFinish])
                    self.setStatusTip('格式化模型运行成功！')
                else:

                    QMessageBox.warning(self, "格式化模式运行失败", self.USBR.FormatReturnTips[self.ModeFinish], QMessageBox.Yes)
                    logger.error("格式化运行失败！模式返回"+str(self.ModeFinish))
                    self.setStatusTip('格式化模式运行失败！')
                self.TimeWatch.stop()
                self.EnableW()
                # 修改模式标志类型为-1
                self.ModeFlag = Configs['主程序所有模式非运行状态标志']
        elif self.ModeFlag==Configs['主程序检查Flash模式运行标志']:
            if self.ModeFinish!=Configs['所有模式完成标志的初始值']:# 模式结束
                if self.ModeFinish==5:# 正常结束
                    logger.info("检查Flash模式运行成功！！！")
                    self.setStatusTip('检查Flash模式运行成功！')
                    returnNums=''
                    Len=10
                    for i in self.USBR.ReciveDatas[:self.USBR.reciveLen]:
                        Len-=1
                        returnNums+=hex(i)+','
                        if Len==0:
                            returnNums+='\n'
                            Len=10
                    QMessageBox.about(self, '运行结果', self.USBR.CheckFlashReturnTips[self.ModeFinish]+"\n返回数据为："+returnNums)
                    # 初始化检查Flash子图
                    self.DrawCheckFlashInit()
                    # 绘制接收数据
                    self.subplots[Configs['检查Flash模式绘图标题']]['series'][0]=[i for i in range(1,self.USBR.reciveLen+1)]
                    self.subplots[Configs['检查Flash模式绘图标题']]['series'][1] = self.USBR.ReciveDatas[:self.USBR.reciveLen]
                    self.subplots[Configs['检查Flash模式绘图标题']]['curves'].setData(
                        self.subplots[Configs['检查Flash模式绘图标题']]['series'][0],
                        self.subplots[Configs['检查Flash模式绘图标题']]['series'][1])
                    # 设置绘图区间
                    self.subplots[Configs['检查Flash模式绘图标题']]['plot'].setXRange(-1,self.USBR.reciveLen+1)
                    self.subplots[Configs['检查Flash模式绘图标题']]['plot'].setYRange(min(self.USBR.ReciveDatas[:self.USBR.reciveLen]), max(self.USBR.ReciveDatas[:self.USBR.reciveLen]))
                else:
                    QMessageBox.warning(self, "检查Flash模式运行失败", self.USBR.CheckFlashReturnTips[self.ModeFinish], QMessageBox.Yes)
                    logger.error("检查Flash模式运行失败！模式返回"+str(self.ModeFinish))
                    self.setStatusTip('检查Flash模式运行失败！')
                self.TimeWatch.stop()
                self.EnableW()
                # 修改模式标志类型为-1
                self.ModeFlag = Configs['主程序所有模式非运行状态标志']
        elif self.ModeFlag==Configs['主程序导出模式运行标志']:
            if self.ModeFinish!=Configs['所有模式完成标志的初始值']:# 模式结束
                # 导出模式返回5，完美结束！
                if self.ModeFinish==3:# 正常结束
                    logger.info("导出模式运行成功！！！" )
                    self.setStatusTip('导出模式运行成功！')
                    # 1.初始化存储标志
                    self.SaveDatasFinish=False
                    # 1.开启存储线程,防止UI界面卡顿
                    ThreadExportDatas = myThread_SaveExportDatas(self)
                    ThreadExportDatas.start()
                    # 2.开启定时器
                    self.SaveExportDatasTimer.start(4)# 四秒监视一次存储情况
                    # 3.输出提示
                    self.setStatusTip("正在存储导出数据")
                # 导出模式返回2,3,未收到0xff失败结束
                elif self.ModeFinish==2:
                    # 将收到的数据保存下来，要去除最后一组数据
                    logger.info("导出模式的连续模式关闭失败，接收数据保存！！！")
                    self.setStatusTip('导出模式运行结束。')
                    # 1.初始化存储标志
                    self.SaveDatasFinish = False
                    # 1.开启存储线程
                    ThreadExportDatas = myThread_SaveExportDatas(self)
                    ThreadExportDatas.start()
                    # 2.开启定时器
                    self.SaveExportDatasTimer.start(4) # 开启存储监视器
                    # 3.输出提示
                    self.setStatusTip("正在存储导出数据")
                    pass
                else:
                    QMessageBox.warning(self, "导出模式运行失败", self.USBR.ExportReturnTips[self.ModeFinish], QMessageBox.Yes)
                    logger.error("导出模式运行失败！模式返回" + str(self.ModeFinish))
                    self.setStatusTip('导出模式运行成功！')
                self.TimeWatch.stop() # 关闭模式监视定时器
                # 修改模式标志类型为-1
                self.ModeFlag = Configs['主程序所有模式非运行状态标志']
        elif self.ModeFlag==Configs['主程序自检模式运行标志']:
            if self.ModeFinish!=Configs['所有模式完成标志的初始值']:# 模式结束
                if self.ModeFinish==5:# 正常结束
                    logger.info("自检模式运行成功！！！")
                    self.setStatusTip('自检模式运行成功！')
                    returnNums=''
                    for i in self.USBR.ReciveDatas[:self.USBR.reciveLen]:
                        returnNums+=hex(i)+','
                    QMessageBox.about(self, '运行结果', self.USBR.SelfTestReturnTips[self.ModeFinish]+"\n返回数据为："+returnNums)
                else:
                    QMessageBox.warning(self, "自检模式运行失败", self.USBR.SelfTestReturnTips[self.ModeFinish], QMessageBox.Yes)
                    logger.error("自检模式运行失败！模式返回" + str(self.ModeFinish))
                    self.setStatusTip('自检模式运行失败！')
                self.TimeWatch.stop()
                self.EnableW()
                # 修改模式标志类型为-1
                self.ModeFlag = Configs['主程序所有模式非运行状态标志']
        elif self.ModeFlag==Configs['主程序读参模式运行标志']:
            if self.ModeFinish!=Configs['所有模式完成标志的初始值']:# 模式结束
                if self.ModeFinish==5:# 正常结束
                    datas=''
                    for i in self.USBR.ReciveDatas:
                        datas+=str(i)
                    logger.info("读参模式运行成功！！！")
                    self.setStatusTip('读参模式运行成功！')
                    QMessageBox.about(self, '运行结果', self.USBR.ReadParasReturnTips[self.ModeFinish])
                else:
                    QMessageBox.warning(self, "读参模式运行失败", self.USBR.ReadParasReturnTips[self.ModeFinish], QMessageBox.Yes)
                    logger.error("读参模式运行失败！模式返回" + str(self.ModeFinish))
                    self.setStatusTip('读参模式运行失败！')
                self.TimeWatch.stop()
                self.EnableW()
                # 修改模式标志类型为-1
                self.ModeFlag = Configs['主程序所有模式非运行状态标志']
        elif self.ModeFlag==Configs['主程序配参模式运行标志']:
            if self.ModeFinish!=Configs['所有模式完成标志的初始值']:# 模式结束
                if self.ModeFinish==5:# 正常结束
                    logger.info("配参模式运行失败！模式返回" + str(self.ModeFinish))
                    self.setStatusTip('配参模式运行成功！')
                    QMessageBox.about(self, '运行结果', self.USBR.ConfigParasReturnTips[self.ModeFinish])
                else:
                    QMessageBox.warning(self, "配参模式运行失败", self.USBR.ConfigParasReturnTips[self.ModeFinish], QMessageBox.Yes)
                    logger.error("配参模式运行失败！模式返回" + str(self.ModeFinish))
                    self.setStatusTip('配参模式运行失败！')
                self.TimeWatch.stop()
                self.EnableW()
                # 修改模式标志类型为-1
                self.ModeFlag = Configs['主程序所有模式非运行状态标志']
        else:
            pass

    # 格式化模式
    def Format(self):
        logger.info("点击格式化按钮")
        # 去使能按钮
        self.DisEnableW()
        # 初始化设备
        retF,retN=self.USBR.initDevice()
        if retF==False:
            QMessageBox.warning(self, '运行结果', '转接板初始化失败！')
            logger.error("设备初始化失败!")
            self.EnableW()
            return
        # 修改模式标志类型
        self.ModeFlag = Configs['主程序格式化模式运行标志']
        # 初始模式完成标志
        self.ModeFinish = Configs['所有模式完成标志的初始值']
        thread = myThread(self, Configs['主程序格式化模式运行标志'])
        thread.start()
        # 启动定时器监视完成情况
        self.TimeWatch.start(Configs['格式化模式定时器循环监视时间'])
        self.setStatusTip('格式化模式运行中。。。')

    # 判断字符串是否为16进制数
    def Ju16Number(self,strs):
        for i in strs:
            if i not in Configs['十六进制有效字符']:
                return False
        return True

    # 检查Flash模式
    def CheckFlash(self):
        # 获取导出地址
        self.CheckFlashStartAddr = self.CheckFlashStartAddrEdit.text()
        if self.CheckFlashStartAddr == "" :
            logger.error("Flash的开始地址为空！")
            QMessageBox.warning(self, "警告", "地址输入为空！请检查Flash的开始地址！", QMessageBox.Yes)
            self.CheckFlashStartAddr=0
            return
        if self.Ju16Number(self.CheckFlashStartAddr)==False:# 非法
            logger.error("Flash的开始地址输入非法！")
            QMessageBox.warning(self, "警告", "地址输出非法！请检查Flash的开始地址！", QMessageBox.Yes)
            self.CheckFlashStartAddr = 0
            return
        elif int(self.CheckFlashStartAddr,16)>Configs['检查Flash的开始地址上限']:
            logger.error("Flash的开始地址输入越界！")
            QMessageBox.warning(self, "警告", "地址输入越界！请检查Flash的开始地址！", QMessageBox.Yes)
            self.CheckFlashStartAddr = 0
            return
        self.CheckFlashStartAddr = int(self.CheckFlashStartAddr,16)
        logger.info("点击检查Flash按钮")
        # 去使能按钮
        self.DisEnableW()
        # 初始化设备
        retF, retN = self.USBR.initDevice()
        if retF == False:
            QMessageBox.warning(self, '运行结果', '转接板初始化失败！')
            logger.error("设备初始化失败!")
            self.EnableW()
            return
        # 修改模式标志类型
        self.ModeFlag = Configs['主程序检查Flash模式运行标志']
        # 初始模式完成标志
        self.ModeFinish = Configs['所有模式完成标志的初始值']
        thread = myThread(self, Configs['主程序检查Flash模式运行标志'])
        thread.start()
        # 启动定时器监视完成情况
        self.TimeWatch.start(Configs['检查Flash模式定时器循环监视时间'])
        self.setStatusTip('检查Flash模式运行中。。。')

    # 导出模式
    def Export(self):

        # 获取导出地址
        self.ExportEndAddr=self.ExportEndAddrEdit.text()
        if self.ExportEndAddr=="" :
            QMessageBox.warning(self,"警告","地址输入为空！请设置导出结束地址！",QMessageBox.Yes)
            logger.error("未配置导出结束地址")
            self.ExportEndAddr=128
            return
        if self.Ju16Number(self.ExportEndAddr)==False:
            QMessageBox.warning(self, "警告", "地址输入非法！请设置导出结束地址！", QMessageBox.Yes)
            logger.error("配置导出结束地址非法")
            self.ExportEndAddr = 128
            return
        elif int(self.ExportEndAddr,16)>Configs['导出模式的结束地址上限']:
            QMessageBox.warning(self, "警告", "地址输入越界！请设置导出结束地址！", QMessageBox.Yes)
            logger.error("配置导出结束地址越界")
            self.ExportEndAddr = 128
            return
        elif int(int(self.ExportEndAddr,16)%128)!=0:
            QMessageBox.warning(self, "警告", "地址输入不为128个数的的整数倍数，请重新设置导出结束地址！", QMessageBox.Yes)
            logger.error("配置导出结束地址错误")
            self.ExportEndAddr = 128
            return
        self.ExportEndAddr=int(self.ExportEndAddr,16)
        logger.info("点击导出按钮")
        # 去使能按钮
        self.DisEnableW()
        # 初始化设备
        retF, retN = self.USBR.initDevice()
        if retF == False:
            QMessageBox.warning(self, '运行结果', '转接板初始化失败！')
            logger.error("设备初始化失败!")
            self.EnableW()
            return
        # 修改模式标志类型
        self.ModeFlag = Configs['主程序导出模式运行标志']
        # 初始模式完成标志
        self.ModeFinish = Configs['所有模式完成标志的初始值']
        thread = myThread(self, Configs['主程序导出模式运行标志'])
        thread.start()
        # 启动定时器监视完成情况
        # 去使能软件，准备接收和存储数据
        self.DisEnableSoft()
        self.TimeWatch.start(Configs['导出模式定时器循环监视时间'])
        self.setStatusTip('导出模式运行中。。。')

    # 自检模式
    def Selftest(self):
        logger.info("点击自检按钮")
        # 去使能按钮
        self.DisEnableW()
        # 初始化设备
        retF, retN = self.USBR.initDevice()
        if retF == False:
            QMessageBox.warning(self, '运行结果', '转接板初始化失败！')
            logger.error("设备初始化失败!")
            self.EnableW()
            return
        # 修改模式标志类型
        self.ModeFlag = Configs['主程序自检模式运行标志']
        # 初始模式完成标志
        self.ModeFinish = Configs['所有模式完成标志的初始值']
        thread = myThread(self, Configs['主程序自检模式运行标志'])
        thread.start()
        # 启动定时器监视完成情况
        self.TimeWatch.start(Configs['自检模式定时器循环监视时间'])
        self.setStatusTip('自检模式运行中。。。')

    # 读参模式
    def ReadParas(self):
        logger.info("点击读参按钮")
        # 去使能按钮
        self.DisEnableW()
        # 初始化设备
        retF, retN = self.USBR.initDevice()
        if retF == False:
            QMessageBox.warning(self, '运行结果', '转接板初始化失败！')
            logger.error("设备初始化失败!")
            self.EnableW()
            return
        # 修改模式标志类型
        self.ModeFlag = Configs['主程序读参模式运行标志']
        # 初始模式完成标志
        self.ModeFinish = Configs['所有模式完成标志的初始值']
        thread = myThread(self, Configs['主程序读参模式运行标志'])
        thread.start()
        # 启动定时器监视完成情况
        self.TimeWatch.start(Configs['读参模式定时器循环监视时间'])
        self.setStatusTip('读参模式运行中。。。')

    # 配参模式
    def ConfigParas(self):
        logger.info("点击配参按钮")
        # 去使能按钮
        self.DisEnableW()
        # 初始化设备
        retF, retN = self.USBR.initDevice()
        if retF == False:
            QMessageBox.warning(self, '运行结果', '转接板初始化失败！')
            logger.error("设备初始化失败!")
            self.EnableW()
            return
        # 修改模式标志类型
        self.ModeFlag = Configs['主程序配参模式运行标志']
        # 初始模式完成标志
        self.ModeFinish = Configs['所有模式完成标志的初始值']
        thread = myThread(self, Configs['主程序配参模式运行标志'])
        thread.start()
        # 启动定时器监视完成情况
        self.TimeWatch.start(Configs['配参模式定时器循环监视时间'])
        self.setStatusTip('配参模式运行中。。。')

    # 模式工作时去使能相关控件
    def DisEnableW(self):
        self.ModelFormat.setEnabled(False)
        self.ModelExport.setEnabled(False)
        self.ModelSelftest.setEnabled(False)
        self.ModelCheckFlash.setEnabled(False)
        # 绘图控件去使能
        self.DisEnaDrawSys()

    # 模式结束时使能相关控件
    def EnableW(self):
        self.ModelFormat.setEnabled(True)
        self.ModelExport.setEnabled(True)
        self.ModelSelftest.setEnabled(True)
        self.ModelCheckFlash.setEnabled(True)
        # 绘图控件去使能
        self.EnaDrawSys()

    # 显示软件配置参数函数
    # 功能：在参数显示区域显示当前软件参数情况
    def ShowParameters(self):
        parates = "<font color=\"#000000\" family="+Configs['字体类型']+">当前软件配置如下：</font>" + '<br>'
          # 软件名称
        parates +="软件名称："+Configs['软件名称']+"<br>"
          # 窗体大小
        parates +="初始窗体大小为：初始高度="+str(Configs['初始窗口高度'])+"<br>初始宽度="+str(Configs['初始窗口宽度'])+"<br>"
          # 按钮高度
        parates +="按钮高度="+str(Configs['按钮高度'])+'<br>'
          # 悬浮控件最小宽度
        parates +="悬浮控件的最小宽度："+str(Configs['悬浮控件的最小宽度'])+"<br>"
          # 悬浮控件中的按钮初始大小
        parates +='悬浮按钮的初始大小：初始高度='+str(Configs['悬浮控件中按钮的高度'])+"<br>初始宽度="+str(Configs['悬浮控件中按钮的宽度'])+'<br>'
          # 字体大小、类型
        parates +='字体大小='+Configs['字体大小']+"<br>"+"字体类型="+Configs['字体类型']+"<br>"
          # 分割空白区高度
        parates += '分割空白区高度=' + str(Configs['分割空白的高度']) + "<br>"
          # 悬浮控件中控件的初始宽度
        parates += '悬浮控件中控件的初始宽度=' + str(Configs['悬浮控件中控件的宽度']) + "<br>"
          # 悬浮控件中控件的初始高度
        parates += '悬浮控件中井下控制区的初始高度=' + str(Configs['悬浮控件中井下控制区的高度']) + "<br>"
        parates += '悬浮控件中绘图区的初始高度=' + str(Configs['悬浮控件中绘图区的高度']) + "<br>"
        parates += '悬浮控件中参数显示区的初始高度=' + str(Configs['悬浮控件中参数显示区的高度']) + "<br>"
        parates += '悬浮控件中文件转换区的初始高度=' + str(Configs['悬浮控件中文件转换区的高度']) + "<br>"
          # 绘图区控件信息
        parates += '绘图文件下拉框高度='+str(Configs['绘图文件下拉框高度'])+"<br>"
        parates +='绘图文件存储根目录：'+Configs['绘图文件存储根目录路径']+'<br>'
        parates += '绘图曲线宽度：' + str(Configs['绘图曲线宽度'])+ '<br>'
        parates += '绘图点大小：' + str(Configs['绘图标记点大小']) + '<br>'
          # 检查Flash开始地址上限
        parates += '检查Flash开始地址上限：' + str(Configs['检查Flash的开始地址上限']) + '<br>'
          # 导出模式结束地址上限
        parates += '导出模式结束地址上限：' + str(Configs['导出模式的结束地址上限']) + '<br>'
          # 悬浮区与窗口的宽度比例
        parates += '悬浮区与窗口的宽度比例：' + str(Configs['悬浮区与窗口的宽度比例']) + '<br>'
          # 悬浮区与窗口的高度比例
        parates += '悬浮区与窗口的高度比例：' + str(Configs['悬浮区与窗口的高度比例']) + '<br>'
          # 悬浮区与按钮的宽度比例
        parates += '悬浮区与按钮的宽度比例：' + str(Configs['悬浮区与按钮的宽度比例']) + '<br>'
          # 转换文件存储目录
        parates += '转换文件存储目录：' + Configs['转换文件存储目录'] + '<br>'
          # 各种模式的命令
        parates += '格式化命令：' + hex(Configs['格式化命令']) + '<br>'
        parates += '检查Flash命令：' + hex(Configs['检查Flash命令']) + '<br>'
        parates += '导出命令：' + hex(Configs['导出命令']) + '<br>'
        parates += '自检命令：' + hex(Configs['自检命令']) + '<br>'
        parates += '检查Flash接收数据长度：' + str(Configs['检查Flash接收数据长度']) + '<br>'
        parates += '自检接收数据长度：' + str(Configs['自检接收数据长度']) + '<br>'
        parates += '转接板初始化spi组：' + str(Configs['转接板初始化spi组']) + '<br>'
        parates += '转接板工作模式配置：' + str(Configs['转接板工作模式配置']) + '<br>'
        parates += '转接板spi主从机配置：' + str(Configs['转接板spi主从机配置']) + '<br>'
        parates += '转接板spiCPOL配置：' + str(Configs['转接板spiCPOL配置']) + '<br>'
        parates += '转接板spiCPHA配置：' + str(Configs['转接板spiCPHA配置']) + '<br>'
        parates += '转接板spi接收数据模式配置：' + str(Configs['转接板spi接收数据模式配置']) + '<br>'
        parates += '转接板spi片选电平配置：' + str(Configs['转接板spi片选电平配置']) + '<br>'
        # 显示日志记录文件的数量
        nums=0
        path = "./logs/"
        files = os.listdir(path)
        for i in files:
            Path=path+i
            nums+=len(os.listdir(Path))
        parates +='已保存日志文件数量为：'+str(nums)+"<br>"
        # 显示导出保存文件的数量

        # 显示转换文件的数据

        # 显示配置文件记录的配置参数数量
        parates +="配置文件的配置参数数量："+str(len(Configs.keys()))+'<br>'

        parates += '</font>'
        self.ParaText.setText(parates)

    # 退出软件
    # 功能：退出软件时执行一些后续步骤
    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        #用户提示
        self.setStatusTip("关闭软件")
        #关闭绘制
        if self.DrawFlag==True:
            ret=QMessageBox.warning(self, "警告", "绘图正在进行中！是否强行退出？", QMessageBox.Yes|QMessageBox.No)
            if ret==QMessageBox.Yes:
                self.stoporstart()
                # 记录关闭软件事件
                times = time.localtime(time.time())
                logger.info("在{}时{}分{}秒软件关闭", times[3], times[4], times[5])
                event.accept()
            else:
                event.ignore()
                return
        #记录关闭软件事件
        times = time.localtime(time.time())
        logger.info("在{}时{}分{}秒软件关闭",times[3],times[4],times[5])

    # 创建子图
    # 功能：创建指定标题和绘图长度的折线图对象
    def CreateSubPlot(self,title,size=Configs['初始绘图长度']):#每个子图的x限制个数

        # 每创建一个子图，同时创建它的x，y可移动轴,标签域和LinearRegion
        plot=self.win.addPlot() #curve对象
        # plot = self.win.addPlot(axisItems={'left': self.LeftAxis})  # curve对象
        # 创建坐标轴Label,当设置units后坐标轴会自动缩小
        plot.setAxisItems()
        plot.setLabel('left', "相对时间（s）")
        plot.setLabel('bottom', title)

        # 显示网格
        plot.showGrid(x=True, y=True)
        plot.addLegend(offset=(1, 1))  # 显示曲线属性name 位置放置在左上角
        # 按title进行数据保存
        self.subplots[title]={'plot':plot,'series':[[],[]],'curves':[],'plot_Num':size}
        # 刷新窗口大小：使新子图自适应
        self.resize(self.width() + 1, self.height() + 1)
        self.resize(self.width() - 1, self.height() - 1)

        # 双击和鼠标移动事件绑定
        plot.scene().sigMouseMoved.connect(self.mouseover)
        plot.scene().sigMouseClicked.connect(self.mouse_clicked)

    # 删除子图
    # 功能，删除传入的子图对象
    def DeleteSubPlot(self,title):
        # 判断删除子图在不在当前绘图中
        if title not in self.subplots.keys():
            return
        # 删除对应子图
        self.win.removeItem(self.subplots[title]['plot'])
        self.subplots.pop(title)

    # 一个子图可以有多个绘图对象
    # 功能：创建指定子图对象的折线绘图对象
    def CreateCurveAndSerie(self,title):
        # 绘图曲线设置
        plot=self.subplots[title]['plot'].plot(symbol=Configs['绘图标记点样式'],symbolSize=Configs['绘图标记点大小'],symbolBrush=Configs["绘图点颜色"],fillLevel=0,name=title)#子图绘制折线图
        plot.setData([],[])
        # 设置绘线样式
        plot.setPen(pg.mkPen(color=Configs['绘图曲线颜色'], width=Configs['绘图曲线宽度']))
        plot.setShadowPen(pg.mkPen(color=Configs['绘图曲线阴影颜色'], width=Configs['绘图曲线阴影宽度']))
        # 固定长度时绘图速度加快
        plot.setSkipFiniteCheck(True)

        # 创建数据
        self.subplots[title]['curves']=plot
        self.subplots[title]['series'].append([])
        self.subplots[title]['series'].append([])

    # 子图鼠标点击事件:负责将当前当前序列的下标所指定的数据显示出来
    def mouse_clicked(self,ClickEvent):
        if self.ClickNewData==False :
            return
        # 显示值
        showStr='('+str(self.subplots[self.ClickTitle]['series'][0][self.ClickData])+','+str(self.subplots[self.ClickTitle]['series'][1][self.ClickData])+')'
        # 显示
        self.SetLabelText(showStr)
        # 修改标志
        self.ClickData = None
        self.ClickNewData=False
    # 子图鼠标移动事件：获取当前鼠标移动到的位置的纵坐标（整型：充当数据序列的下标）
    def mouseover(self,evt):
        pos = evt # 当前鼠标的FPoint对象
        title=self.GetSubPlotIndex(evt)
        if title==None:
            self.ClickNewData = False
            return
        mousePoint = self.subplots[title]['plot'].vb.mapSceneToView(pos) # 转换为plot图位置
        index = float(mousePoint.y()) # 由于我的数据时纵轴式显示的，纵轴上的数据表示为帧序号
        # 判断当前点击的数据点是否存在于绘图的曲线上
        if len(self.subplots[title]['series'][1]) == 0:
            self.ClickNewData = False
            return
        if index >= self.subplots[title]['series'][1][-1]:
            indexs=self.subplots[title]['series'][1][-1]
        elif index<=self.subplots[title]['series'][1][0]:
            indexs=self.subplots[title]['series'][1][0]
        else:
            indexs=float(mousePoint.y())
        indexs = int(indexs * Configs['转换单位'] / Configs['间隔时间']) # 数据下标
        startindex=int(self.subplots[title]['series'][1][0]*Configs['转换单位'] / Configs['间隔时间'])
        index=indexs-startindex
        self.ClickNewData = True
        self.ClickData=index
        self.ClickTitle=title

    # 根据鼠标移动的位置判断在那个子图内
    def GetSubPlotIndex(self,evt):
        pos=evt
        for title in self.ShowTitles:
            if self.subplots[title]['plot'].sceneBoundingRect().contains(pos):
                return title
        return None

    # 更新某个子图上的某个数据列
    # 功能：更新指定子图的指定绘图数据序列，新数据newdata_one。动态过滤超出设置长度的数据。
    def RefreshData(self, title, newdata_one, numIndex):
        # 若当前序列个数大于等于设置的最长显示长度
        if len(self.subplots[title]['series'][1]) >= self.subplots[title]['plot_Num']:
            # 舍去第一个数据
            for i in range(1, self.subplots[title]['plot_Num']):
                self.subplots[title]['series'][1][i - 1] = self.subplots[title]['series'][1][i]
                self.subplots[title]['series'][0][i - 1] = self.subplots[title]['series'][0][i]
            # 将新数据加入：纵轴显示机制
            self.subplots[title]['series'][1][self.subplots[title]['plot_Num'] - 1] = numIndex*Configs['间隔时间']/Configs['转换单位']
            self.subplots[title]['series'][0][self.subplots[title]['plot_Num'] - 1] = newdata_one
            # 删除序列里大于显示个数的前面的序列
            del self.subplots[title]['series'][1][:len(self.subplots[title]['series'][0]) - self.subplots[title]['plot_Num']]
            del self.subplots[title]['series'][0][:len(self.subplots[title]['series'][0]) - self.subplots[title]['plot_Num']]
        # 当前序列长度不大于最大长度
        else:
            self.subplots[title]['series'][1].append(numIndex*Configs['间隔时间']/Configs['转换单位'])
            self.subplots[title]['series'][0].append(newdata_one)  # x轴加一
        # *********************************************
        # 设置绘制图显示的数据序列
        self.subplots[title]['curves'].setData(self.subplots[title]['series'][0], self.subplots[title]['series'][1])
        # 设置区间
        self.subplots[title]['plot'].setXRange(self.subplots[title]['series'][0][0], self.subplots[title]['series'][0][-1])# X轴区间依据配置文件设置
        self.subplots[title]['plot'].setYRange(self.subplots[title]['series'][1][0], self.subplots[title]['series'][1][-1])# Y轴区间最小值依据配置文件，最大值依据当前Y轴序列的最大值

    # 读取数据，更新绘图 #定时绘图！！！
    # 功能：绘制数据
    def RefreshDataFromMSPDatabase(self):
        #更新绘图
        if self.DrawDataIndex!=-1 and self.DrawDataIndex<self.DrawDataMaxsize:
            for title in self.ShowTitles:
                self.RefreshData(title, self.DDrawData_Now[self.DrawDataIndex][self.title_to_index[title]],self.DrawFrameIndexs[self.DrawDataIndex])
            self.DrawDataIndex+=1
            #绘制算法结果
        else:# 绘制结束
            # 修改暂停控制按钮
            self.TimeOutOrRestart.setText('暂停动态绘制')
            self.TimeOutOrRestart.setStyleSheet(self.styleButtonGreen)
            # 修改绘图启动按钮和标志
            self.DrawFlag=False
            self.DrawTimer.stop()
            # 直接绘图使能和下拉文件选择
            self.SDraw.setEnabled(True)
            self.DataFilenames.setEnabled(True)
            # 开启井下采集控制系统
            self.EnaUndContralSys()
            self.StopOrStart.setText("启动动态绘制")
            self.StopOrStart.setStyleSheet(self.styleButtonGreen)
            self.statusbar.showMessage("绘制停止")
            self.statusbar.showMessage("数据表中没有新数据！！！")
            QMessageBox.about(self, '绘图结束', '数据绘制完成！')

    # 直接绘图功能
    def SDrawPlot(self):
        if self.ShowTitles == []:
            QMessageBox.warning(self, "警告", "未选中绘图属性！请先选择需要绘图的属性！", QMessageBox.Yes)
            return
        self.statusbar.showMessage("绘制文件所有数据！")
        FrameIndex=self.DrawData_Now[:,0].copy()
        # 判断用户要求的直接绘制的起始和结束帧序号
        if self.DrawStartIndexEdit.text()=="" or self.DrawEndIndexEdit.text()=='':
            QMessageBox.warning(self, "警告", "请配置绘图区间！", QMessageBox.Yes)
            logger.error("绘图区间未选择！！")
            return
        start=int(self.DrawStartIndexEdit.text())
        end=int(self.DrawEndIndexEdit.text())
        if start>FrameIndex[-1] or end>FrameIndex[-1] or start>=end:
            # 越界
            QMessageBox.warning(self, "警告", "存在区间越界或区间设置前后颠倒错误！", QMessageBox.Yes)
            logger.error("存在区间越界或区间设置前后颠倒错误！")
            return
        if (end-start)>10000:
            # 禁止绘图长度大于10000个数据
            QMessageBox.warning(self, "警告", "绘图区间过大！", QMessageBox.Yes)
            logger.error("绘图区间过大！")
            return
        self.DrawFrameIndexs = self.DrawData_Now[:, 0][start:end].copy()
        self.DrawFrameTimes=[i*Configs['间隔时间']/Configs['转换单位'] for i in self.DrawFrameIndexs]
        self.DDrawData_Now = self.DrawData_Now[:, 1:][start:end].copy()
        # 删除绘图
        for title in self.ShowTitles:
            self.DeleteSubPlot(title)
        # 创建绘图
        for title in self.ShowTitles:
            self.CreateSubPlot(title,(end-start))
            self.CreateCurveAndSerie(title)
        # 直接绘制
        for title in self.ShowTitles:
            self.subplots[title]['series'][1]=list(self.DrawFrameTimes)
            self.subplots[title]['series'][0]=list(self.DDrawData_Now[:,self.title_to_index[title]])
            self.subplots[title]['curves'].setData(self.subplots[title]['series'][0], self.subplots[title]['series'][1])
            self.subplots[title]['plot'].setXRange(min(self.subplots[title]['series'][0])-1,max(self.subplots[title]['series'][0])+1)
            self.subplots[title]['plot'].setYRange(min(self.subplots[title]['series'][1])-1,max(self.subplots[title]['series'][1])+1)
    # 按钮绑定事件函数
    # 功能：一些按键槽函数连接
    def ButtonConects(self):
        self.StopOrStart.clicked.connect(self.stoporstart)  #停止或启动绘图
        self.TimeOutOrRestart.clicked.connect(self.TimeOut_Restart) # 暂停或重启绘图
        self.Clear.clicked.connect(self.ClearDraw)# 清空绘图
        self.SDraw.clicked.connect(self.SDrawPlot)#直接绘制
        # 文件转换按钮绑定函数
        self.tranfromButton.clicked.connect(self._ToTransfromFiles)
        # 绘图文件改变时:清空也算改变
        self.DataFilenames.currentIndexChanged.connect(self.FlashDrawFile)

    # 绘图文件选择改变
    def FlashDrawFile(self):
        # 首先判断用户有没有选择要读取的文件
        filePath = self.DataFilenames.currentText()
        if filePath=='':# 防止清空触发函数
            return
        # 为了加快反应速度，只有第一次会去读取，之后会进行记录
        if filePath in self.FileBoundDict.keys():# 有记录
            self.SDrawTipLabel.setText("直接绘图区间选择：[" + str(self.FileBoundDict[filePath][0]) + ',' + str(self.FileBoundDict[filePath][1]) + ']')
            return

        Keys = ['帧序号', '温度', '振动加速度x', '振动加速度y', '振动加速度z', '扭矩', '压强', '钻压', '钻速']
        FilePath = self.DatasPath + filePath  # 拼接路径
        self.DrawData_Now, ret = self.DataOP.ReadDatas_Keys(FilePath, Keys)
        if ret == False:
            self.statusbar.showMessage("文件数据读取失败！")
            logger.error("读取数据文件失败！！")
            self.DisEnaDrawSys()
            return
        self.EnaDrawSys()
        # 修改直接绘图区间的提示
        FrameIndex = self.DrawData_Now[:, 0].copy()
        # 记录
        self.FileBoundDict[filePath] = [FrameIndex[0], FrameIndex[-1]]
        # 显示
        self.SDrawTipLabel.setText("直接绘图区间选择：["+str(FrameIndex[0])+','+str(FrameIndex[-1])+']')

    # 文件转换实现
    def _ToTransfromFiles(self):
        # 获取转换文件对象
        TFfiles=self.DataFilenames_TransFrom.Selectlist()
        if TFfiles==[]:
            QMessageBox.warning(self, "警告", "转换文件未选择！", QMessageBox.Yes)
            return None
        # 获取读取关键字
        Keys=['帧序号','温度','振动加速度x','振动加速度y','振动加速度z','扭矩','压强','钻压','钻速']
        # 读取数据
        self.FilesTransfrom.TransFrom(TFfiles,Keys)
        QMessageBox.about(self, "转换成功", "转换成功！")

    # 配置
    # 绘图
    # 功能：启动或停止绘图
    def stoporstart(self):#停止或读数据库
        if self.DrawFlag:# 有存在的必要吗？
            logger.info("点击停止绘图")
            self.DrawFlag=False
            #停止绘制定时器
            self.DrawTimer.stop() # 关闭绘图更新定时器
            # 开启井下采集控制系统
            self.EnaUndContralSys()
            self.StopOrStart.setText("启动动态绘制")
            self.StopOrStart.setStyleSheet(self.styleButtonGreen)
            self.statusbar.showMessage("停止动态绘图")
            # 修改暂停控制按钮
            self.TimeOutOrRestart.setText('暂停动态绘制')
            self.TimeOutOrRestart.setStyleSheet(self.styleButtonGreen)
            # 直接绘图使能和下拉文件选择
            self.SDraw.setEnabled(True)
            self.DataFilenames.setEnabled(True)
        else:
            if self.ShowTitles==[]:
                QMessageBox.warning(self, "警告", "未选中绘图属性！请先选择需要绘图的属性！", QMessageBox.Yes)
                return
            logger.info("点击启动绘图")
            # 删除绘图
            for title in self.ShowTitles:
                self.DeleteSubPlot(title)
            # 再创建绘图
            for title in self.ShowTitles:
                self.CreateSubPlot(title)
                self.CreateCurveAndSerie(title)
            self.DrawFrameIndexs=self.DrawData_Now[:,0].copy()
            self.DDrawData_Now=self.DrawData_Now[:,1:].copy()
            #绘图初始化
            self.DrawDataIndex=0 # 从头开始绘制
            self.DrawDataMaxsize=self.DDrawData_Now.shape[0] # 最大数据个数
            self.DrawFlag=True
            #修改暂停控制按钮
            self.TimeOutOrRestart.setText('暂停动态绘制')
            self.TimeOutOrRestart.setStyleSheet(self.styleButtonRed)
            #启动绘制定时器
            self.DrawTimer.start(self.DrawF)# 开启绘图更新定时器
            #关闭井下采集控制系统
            self.DisEnaUndContralSys()
            self.StopOrStart.setText("停止动态绘制")
            self.StopOrStart.setStyleSheet(self.styleButtonRed)
            self.statusbar.showMessage("动态绘制开始")
            # 绘制期间不能直接绘制，也不能选择其他文件
            self.SDraw.setEnabled(False)
            self.DataFilenames.setEnabled(False)

    # 功能：暂停或重启绘制
    def TimeOut_Restart(self):
        logger.info("点击重启或暂停绘图")
        if self.DrawFlag==False:# 未在绘图
            self.statusbar.showMessage("未在绘图期间，操作无效！")
            return
        if self.TimeOutOrRestart.text()=='暂停动态绘制':
            self.TimeOutOrRestart.setText('重启动态绘制')
            self.TimeOutOrRestart.setStyleSheet(self.styleButtonGreen)
            self.DrawTimer.start(Configs['默认绘图停止的循环绘图时间'])#一百分钟
            self.statusbar.showMessage("绘制暂停")
        elif self.TimeOutOrRestart.text()=='重启动态绘制':
            self.TimeOutOrRestart.setText('暂停动态绘制')
            self.TimeOutOrRestart.setStyleSheet(self.styleButtonRed)
            self.DrawTimer.start(self.DrawF)
            self.statusbar.showMessage("绘制重启")

    # 功能：清空绘图
    def ClearDraw(self):
        logger.info("点击清空绘图")
        for title in self.ShowTitles:
            self.subplots[title]['series']=[[],[]]
            self.subplots[title]['curves'].setData([],[])
        self.setStatusTip('清空绘图！')
        self.SetLabelText('')

    # 其他类型事件连接函数
    # 功能：另类事件连接函数设置，如输入框数据变动时槽函数执行体的连接
    def OtherConnects(self):
        #设置显示个数
        self.ShowNumEdit.textChanged.connect(self.SetShowNum)
        #配置绘制速度
        self.DrawFEdit.textChanged.connect(self.SetDrawF)

    # 设置显示长度
    # 功能：读取设置显示长度框数据，设置显示长度
    def SetShowNum(self):
        if self.ShowNumEdit.text()=="":#若没有数字就默认上一次的个数
            return None
        shownum=int(self.ShowNumEdit.text())
        if shownum<=0:
            return None
        # 设置当前显示子图的显示长度
        for title in self.ShowTitles:
            self.subplots[title]['plot_Num']=shownum
        self.statusbar.showMessage("设置显示" + str(shownum) + "个数据。")

    # 设置绘制速度
    # 功能：读取设置绘制速度框，设置绘制速度
    def SetDrawF(self):
        if self.DrawFEdit.text()=="":#空字符
            return None
        DrawF=int(self.DrawFEdit.text())
        if DrawF<=0:
            return None
        self.DrawF=DrawF
        # 如果正在绘图，就动态改变绘图速度
        if self.DrawFlag==True:
            self.DrawTimer.start(self.DrawF)

        self.statusbar.showMessage("设置绘图速度：" + str(DrawF/1000) + "秒")

    # 使能井下系统
    # 使能井下系统控件
    def EnaUndContralSys(self):
        self.ModelExport.setEnabled(True)
        self.ModelSelftest.setEnabled(True)
        self.ModelCheckFlash.setEnabled(True)
        self.ModelFormat.setEnabled(True)
        self.ExportEndAddrEdit.setEnabled(True)
        self.CheckFlashStartAddrEdit.setEnabled(True)


    # 去使能井下系统
    # 去使能井下系统控件
    def DisEnaUndContralSys(self):
        self.ModelExport.setEnabled(False)
        self.ModelSelftest.setEnabled(False)
        self.ModelCheckFlash.setEnabled(False)
        self.ModelFormat.setEnabled(False)
        self.ExportEndAddrEdit.setEnabled(False)
        self.CheckFlashStartAddrEdit.setEnabled(False)

    # 使能绘图系统
    # 使能绘图系统控件
    def EnaDrawSys(self):
        self.DataFilenames.setEnabled(True)
        self.StopOrStart.setEnabled(True)
        self.TimeOutOrRestart.setEnabled(True)
        self.Clear.setEnabled(True)
        self.ShowNumEdit.setEnabled(True)
        self.DrawFEdit.setEnabled(True)
        self.SDraw.setEnabled(True)
        self.ReDrawButton.setEnabled(True)
        self.SubPlotsShowSelect.setEnabled(True)
        self.DrawStartIndexEdit.setEnabled(True)
        self.DrawEndIndexEdit.setEnabled(True)

    # 去使能绘图系统
    # 去使能绘图系统控件
    def DisEnaDrawSys(self):
        self.DataFilenames.setEnabled(False)
        self.StopOrStart.setEnabled(False)
        self.TimeOutOrRestart.setEnabled(False)
        self.Clear.setEnabled(False)
        self.ShowNumEdit.setEnabled(False)
        self.DrawFEdit.setEnabled(False)
        self.SDraw.setEnabled(False)
        self.ReDrawButton.setEnabled(False)
        self.SubPlotsShowSelect.setEnabled(False)
        self.DrawStartIndexEdit.setEnabled(False)
        self.DrawEndIndexEdit.setEnabled(False)

    # 使能文件转换系统
    def EnaTransfromFiles(self):
        self.SaveRoadEdit.setEnabled(True)
        self.DataFilenames_TransFrom.setEnabled(True)
        self.tranfromButton.setEnabled(True)

    # 去使能文件转换系统
    def DisEnaTransfromFiles(self):
        self.SaveRoadEdit.setEnabled(False)
        self.DataFilenames_TransFrom.setEnabled(False)
        self.tranfromButton.setEnabled(False)

    # 使能软件
    def EnableSoft(self):
        self.EnaUndContralSys()
        self.EnaDrawSys()
        self.EnaTransfromFiles()
        # Action去使能
        self.UndControl.setEnabled(True)
        self.DrawControl.setEnabled(True)
        self.ParaDisc.setEnabled(True)
        self.tansfromFile.setEnabled(True)

    # 去使能软件
    def DisEnableSoft(self):
        self.DisEnaUndContralSys()
        self.DisEnaDrawSys()
        self.DisEnaTransfromFiles()
        # Action去使能
        self.UndControl.setEnabled(False)
        self.DrawControl.setEnabled(False)
        self.ParaDisc.setEnabled(False)
        self.tansfromFile.setEnabled(False)
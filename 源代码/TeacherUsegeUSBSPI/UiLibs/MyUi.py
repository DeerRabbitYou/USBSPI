from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QCheckBox,QComboBox,QLineEdit,QListWidget,QListWidgetItem
import os

class ComboCheckBox(QComboBox):

    def loadItems(self, items):
        self.items = items
        self.items.insert(0, '全部')
        self.row_num = len(self.items)
        self.Selectedrow_num = 0
        self.qCheckBox = []
        self.qLineEdit = QLineEdit()
        self.qLineEdit.setReadOnly(True)
        self.qListWidget = QListWidget()
        self.addQCheckBox(0)
        self.qCheckBox[0].stateChanged.connect(self.All)
        for i in range(0, self.row_num):
            self.addQCheckBox(i)
            self.qCheckBox[i].stateChanged.connect(self.showMessage)
        self.setModel(self.qListWidget.model())
        self.setView(self.qListWidget)
        self.setLineEdit(self.qLineEdit)


    def showPopup(self):
        #  重写showPopup方法，避免下拉框数据多而导致显示不全的问题
        select_list = self.Selectlist()  # 当前选择数据
        self.loadItems(items=self.items[1:])  # 重新添加组件
        for select in select_list:
            index = self.items[:].index(select)
            self.qCheckBox[index].setChecked(True)   # 选中组件
        return QComboBox.showPopup(self)

    def printResults(self):# 返回当前选中数据
        list = self.Selectlist()
        return list

    def addQCheckBox(self, i):
        self.qCheckBox.append(QCheckBox())
        qItem = QListWidgetItem(self.qListWidget)
        self.qCheckBox[i].setText(self.items[i])
        self.qListWidget.setItemWidget(qItem, self.qCheckBox[i])

    def Selectlist(self):
        Outputlist = []
        for i in range(1, self.row_num):
            if self.qCheckBox[i].isChecked() == True:
                Outputlist.append(self.qCheckBox[i].text())
        self.Selectedrow_num = len(Outputlist)
        return Outputlist

    def showMessage(self):
        Outputlist = self.Selectlist()
        self.qLineEdit.setReadOnly(False)
        self.qLineEdit.clear()
        show = ';'.join(Outputlist)

        if self.Selectedrow_num == 0:
            self.qCheckBox[0].setCheckState(0)
        elif self.Selectedrow_num == self.row_num - 1:
            self.qCheckBox[0].setCheckState(2)
        else:
            self.qCheckBox[0].setCheckState(1)
        self.qLineEdit.setText(show)
        self.qLineEdit.setReadOnly(True)

    def All(self, zhuangtai):
        if zhuangtai == 2:
            for i in range(1, self.row_num):
                self.qCheckBox[i].setChecked(True)
        elif zhuangtai == 1:
            if self.Selectedrow_num == 0:
                self.qCheckBox[0].setCheckState(2)
        elif zhuangtai == 0:
            self.clear()

    def clear(self):
        for i in range(self.row_num):
            self.qCheckBox[i].setChecked(False)

    def currentText(self):
        text = QComboBox.currentText(self).split(';')
        if text.__len__() == 1:
            if not text[0]:
                return []
        return text

#获取配置文件参数
from others.GetConfigParas import GetConfigsToDict
Configs=GetConfigsToDict() # 读取配置信息

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # 按钮样式
        # styleButton="border: 1px solid grey;border-radius:15px;padding: 1px 1px 1px 1px;QPushButton{background-color:rgb(0,255,0)}\ QPushButton:hover{background-color:rgb(0,0,255)}"
        # styleButton="border: 1px solid grey;border-radius:15px;padding: 1px 1px 1px 1px;background-color:rgb(0,255,0);}"
        # styleButtonGreen='border: 1px grey solid;border-radius:2px;padding: 1px 1px 1px 1px; border-style:outset;background-color:#96c24e;font:Times New Roman;'
        styleButtonGreen = "QPushButton{background-color: " + Configs['按钮初始颜色'] + "}\
                             QPushButton{font-family:" + Configs['字体类型'] + ";font-color:+" + Configs[
            '字体颜色'] + ";font-size:" + Configs['字体大小'] + ";}\
                            QPushButton:hover{background-color:" + Configs['按钮悬停颜色'] + "}\
                            QPushButton:pressed{background-color:" + Configs['按钮按下颜色'] + "}\
                            " + Configs['按钮样式']
        # 初始化窗口大小和比例因子
        self.InitsizeAndBL(MainWindow)

        # 初始化整体布局
        self.InitWindow(MainWindow)

        # 初始化工具栏和悬浮控件
        self.InitToolbarAndFloat(MainWindow)

        # 创建四个功能区
        self.InitFunctionArea()

        # 绘图区控件初始化
        self.InitDraw(styleButtonGreen)

        # 井下控制区控件初始化
        self.InitUndControl(styleButtonGreen)

        # 参数显示区控件初始化
        self.InitParas()

        # 文件转换区控件初始化
        self.InitTransfromFile(styleButtonGreen)

        # 侧边Action布局初始化
        self.InitActions(MainWindow)

        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.contrals_dockWidget)

        # 侧边Action触发绑定
        self.ActionsTriggered(MainWindow)

        # 其他初始化操作
        self.MyFunction_init()

        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # Action触发函数绑定
    def ActionsTriggered(self,MainWindow):
        # 侧边控制区按钮触发函数连接********************************************************************
        self.retranslateUi(MainWindow)
        self.UndControl.triggered.connect(self.ShowContral)
        self.UndControl.triggered.connect(self.UndControl_Widget.show)
        self.UndControl.triggered.connect(self.Draw_Widget.hide)
        self.UndControl.triggered.connect(self.ParaDisc_Widget.hide)
        self.UndControl.triggered.connect(self.transfromFile_Widget.hide)

        self.DrawControl.triggered.connect(self.ShowContral)
        self.DrawControl.triggered.connect(self.UndControl_Widget.hide)
        self.DrawControl.triggered.connect(self.Draw_Widget.show)
        self.DrawControl.triggered.connect(self.ParaDisc_Widget.hide)
        self.DrawControl.triggered.connect(self.ReflashFiles)  # 更新存储文件的下拉框信息
        self.DrawControl.triggered.connect(self.transfromFile_Widget.hide)

        self.ParaDisc.triggered.connect(self.ShowContral)
        self.ParaDisc.triggered.connect(self.UndControl_Widget.hide)
        self.ParaDisc.triggered.connect(self.Draw_Widget.hide)
        self.ParaDisc.triggered.connect(self.ParaDisc_Widget.show)
        self.ParaDisc.triggered.connect(self.transfromFile_Widget.hide)

        self.tansfromFile.triggered.connect(self.ShowContral)
        self.tansfromFile.triggered.connect(self.UndControl_Widget.hide)
        self.tansfromFile.triggered.connect(self.Draw_Widget.hide)
        self.tansfromFile.triggered.connect(self.ParaDisc_Widget.hide)
        self.tansfromFile.triggered.connect(self.TransFlashFiles)  # 更新存储文件的下拉框信息
        self.tansfromFile.triggered.connect(self.transfromFile_Widget.show)

    # 侧边Action布局初始化
    def InitActions(self,MainWindow):
        # 侧边按钮*********************************************************************************
        # 绘图
        #######
        # 井下参数采集系统控制
        self.UndControl = QtWidgets.QAction(MainWindow)
        self.UndControl.setObjectName("UndControl")
        self.toolBar.addAction(self.UndControl)
        self.UndControl.setFont(QFont(Configs['字体类型']))
        # 工具栏的部件分隔用的空白Widget控件
        self.NoneWidget1 = QtWidgets.QDockWidget(MainWindow)
        self.NoneWidget1.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.NoneWidget1.setMaximumHeight(Configs['分割空白的高度'])
        self.toolBar.addWidget(self.NoneWidget1)
        self.NoneWidget1.setStyleSheet('background-color:' + Configs['分割空白的颜色'])

        # 绘图
        self.DrawControl = QtWidgets.QAction(MainWindow)
        self.DrawControl.setObjectName("DrawControl")
        self.toolBar.addAction(self.DrawControl)
        self.DrawControl.setFont(QFont(Configs['字体类型']))
        # 工具栏的部件分隔用的空白Widget控件
        self.NoneWidget2 = QtWidgets.QDockWidget(MainWindow)
        self.NoneWidget2.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.NoneWidget2.setMaximumHeight(Configs['分割空白的高度'])
        self.toolBar.addWidget(self.NoneWidget2)
        self.NoneWidget2.setStyleSheet('background-color:' + Configs['分割空白的颜色'])
        # 参数说明
        self.ParaDisc = QtWidgets.QAction(MainWindow)
        self.ParaDisc.setObjectName("ParaDisc")
        self.toolBar.addAction(self.ParaDisc)
        self.ParaDisc.setFont(QFont(Configs['字体类型']))
        # 工具栏的部件分隔用的空白Widget控件
        self.NoneWidget3 = QtWidgets.QDockWidget(MainWindow)
        self.NoneWidget3.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.NoneWidget3.setMaximumHeight(Configs['分割空白的高度'])
        self.toolBar.addWidget(self.NoneWidget3)
        self.contrals_dockWidget.setWidget(self.dockWidgetContents_2)
        self.NoneWidget3.setStyleSheet('background-color:' + Configs['分割空白的颜色'])
        # 文件转换
        self.tansfromFile = QtWidgets.QAction(MainWindow)
        self.tansfromFile.setObjectName("tansfromFile")
        self.toolBar.addAction(self.tansfromFile)
        self.tansfromFile.setFont(QFont(Configs['字体类型']))
        # 工具栏的部件分隔用的空白Widget控件
        self.NoneWidget4 = QtWidgets.QDockWidget(MainWindow)
        self.NoneWidget4.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
        self.NoneWidget4.setMaximumHeight(Configs['分割空白的高度'])
        self.toolBar.addWidget(self.NoneWidget4)
        self.contrals_dockWidget.setWidget(self.dockWidgetContents_2)
        self.NoneWidget4.setStyleSheet('background-color:' + Configs['分割空白的颜色'])

    # 文件转换区控件初始化
    def InitTransfromFile(self,styleButtonGreen):
        # 设置转换文件保存路径
        # 设置保存路径提示label
        self.SaveFileRoadLabel_TransFrom = QtWidgets.QLabel(self.transfromFile_Widget)
        self.SaveFileRoadLabel_TransFrom.setObjectName('SaveFileRoadLabel_TransFrom')
        self.verticalLayout_TransfromControl.addWidget(self.SaveFileRoadLabel_TransFrom)
        self.SaveFileRoadLabel_TransFrom.setText("转换文件的存储路径：")
        self.SaveFileRoadLabel_TransFrom.setFont(QFont(Configs['字体类型']))
        self.SaveFileRoadLabel_TransFrom.setFixedHeight(Configs['绘图文件下拉框高度'])
        # 路径设置
        self.SaveRoadEdit = QtWidgets.QLineEdit(self.transfromFile_Widget)
        self.SaveRoadEdit.setObjectName("SaveRoadEdit")
        self.verticalLayout_TransfromControl.addWidget(self.SaveRoadEdit)
        self.SaveRoadEdit.setFont(QFont(Configs['字体类型']))

        # 文件转换按钮和label
        # 下拉数据文件显示
        self.DataFilenamesLabel_TransFrom = QtWidgets.QLabel(self.transfromFile_Widget)
        self.DataFilenamesLabel_TransFrom.setObjectName('DataFilenamesLabel_TransFrom')
        self.verticalLayout_TransfromControl.addWidget(self.DataFilenamesLabel_TransFrom)
        self.DataFilenamesLabel_TransFrom.setText("h5文件选择：")
        self.DataFilenamesLabel_TransFrom.setFont(QFont(Configs['字体类型']))
        self.DataFilenamesLabel_TransFrom.setFixedHeight(Configs['绘图文件下拉框高度'])
        # 转换文件选择
        self.DataFilenames_TransFrom = ComboCheckBox(self.transfromFile_Widget)
        self.DataFilenames_TransFrom.setMinimumSize(QtCore.QSize(Configs['悬浮控件中按钮的宽度'], Configs['悬浮控件中按钮的高度']))
        self.DataFilenames_TransFrom.loadItems(['1','2'])
        self.verticalLayout_TransfromControl.addWidget(self.DataFilenames_TransFrom)
        # 转换按钮
        self.tranfromButton = QtWidgets.QPushButton(self.transfromFile_Widget)
        self.tranfromButton.setObjectName("tranfromButton")
        self.verticalLayout_TransfromControl.addWidget(self.tranfromButton)
        self.tranfromButton.setStyleSheet(
            styleButtonGreen)
        self.tranfromButton.setFixedWidth(Configs['悬浮控件中按钮的宽度'])
        self.tranfromButton.setFixedHeight(Configs['悬浮控件中按钮的高度'])

    # 参数显示区控件初始化
    def InitParas(self):
        # 参数显示框
        self.ParaText = QtWidgets.QTextEdit(self.ParaDisc_Widget)
        self.ParaText.setObjectName("ParaText")
        self.ParaText.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)  # 设置不自动换行
        self.ParaText.setReadOnly(True)  # 设置只能查看
        self.verticalLayout_Paras.addWidget(self.ParaText)
        self.ParaText.setFont(QFont(Configs['字体类型']))

    # 井下控制区控件初始化
    def InitUndControl(self,styleButtonGreen):
        pass
        # 通信模式按钮
        # 格式化模式
        self.ModelFormat = QtWidgets.QPushButton(self.UndControl_Widget)
        self.ModelFormat.setObjectName("ModelFormat")
        self.verticalLayout_UnderControl.addWidget(self.ModelFormat)
        self.ModelFormat.setStyleSheet(styleButtonGreen)
        self.ModelFormat.setFixedWidth(Configs['悬浮控件中按钮的宽度'])
        self.ModelFormat.setFixedHeight(Configs['悬浮控件中按钮的高度'])

        # 导出模式
        self.ExportEndAddrEdit = QtWidgets.QLineEdit(self.UndControl_Widget)
        self.ExportEndAddrEdit.setObjectName("ExportEndAddrEdit")
        self.verticalLayout_UnderControl.addWidget(self.ExportEndAddrEdit)
        self.ExportEndAddrEdit.setFont(QFont(Configs['字体类型']))

        self.ModelExport = QtWidgets.QPushButton(self.UndControl_Widget)
        self.ModelExport.setObjectName("ModelExport")
        self.verticalLayout_UnderControl.addWidget(self.ModelExport)
        self.ModelExport.setStyleSheet(styleButtonGreen)
        self.ModelExport.setFixedWidth(Configs['悬浮控件中按钮的宽度'])
        self.ModelExport.setFixedHeight(Configs['悬浮控件中按钮的高度'])
        # 自测模式
        self.ModelSelftest = QtWidgets.QPushButton(self.UndControl_Widget)
        self.ModelSelftest.setObjectName("ModelSelftest")
        self.verticalLayout_UnderControl.addWidget(self.ModelSelftest)
        self.ModelSelftest.setStyleSheet(
            styleButtonGreen)
        self.ModelSelftest.setFixedWidth(Configs['悬浮控件中按钮的宽度'])
        self.ModelSelftest.setFixedHeight(Configs['悬浮控件中按钮的高度'])

        # 检查Flash模式
        # 配置检查Flash模式开始地址
        self.CheckFlashStartAddrEdit = QtWidgets.QLineEdit(self.UndControl_Widget)
        self.CheckFlashStartAddrEdit.setObjectName("CheckFlashStartAddrEdit")
        self.verticalLayout_UnderControl.addWidget(self.CheckFlashStartAddrEdit)
        self.CheckFlashStartAddrEdit.setFont(QFont(Configs['字体类型']))
        self.ModelCheckFlash = QtWidgets.QPushButton(self.UndControl_Widget)
        self.ModelCheckFlash.setObjectName("ModelCheckFlash")
        self.verticalLayout_UnderControl.addWidget(self.ModelCheckFlash)
        self.ModelCheckFlash.setStyleSheet(
            styleButtonGreen)
        self.ModelCheckFlash.setFixedWidth(Configs['悬浮控件中按钮的宽度'])
        self.ModelCheckFlash.setFixedHeight(Configs['悬浮控件中按钮的高度'])

    # 绘图区控件初始化
    def InitDraw(self,styleButtonGreen):
        # 下拉数据文件显示
        self.DataFilenamesLabel = QtWidgets.QLabel(self.Draw_Widget)
        self.DataFilenamesLabel.setObjectName('DataFilenamesLabel')
        self.verticalLayout_DrawControl.addWidget(self.DataFilenamesLabel)
        self.DataFilenamesLabel.setText("绘图数据文件选择：")
        self.DataFilenamesLabel.setFont(QFont(Configs['字体类型']))
        self.DataFilenamesLabel.setFixedHeight(Configs['绘图文件下拉框高度'])
        self.DataFilenames = QtWidgets.QComboBox(self.Draw_Widget)
        self.DataFilenames.setObjectName('DatasFilenames')
        self.verticalLayout_DrawControl.addWidget(self.DataFilenames)
        self.DataFilenames.setFixedWidth(Configs['悬浮控件中按钮的宽度'])
        self.DataFilenames.setFixedHeight(Configs['悬浮控件中按钮的高度'])
        self.DataFilenames.setFont(QFont(Configs['字体类型']))

        # 属性选择提示标签
        self.SelectParasTipLabel = QtWidgets.QLabel(self.Draw_Widget)
        self.SelectParasTipLabel.setObjectName('SelectParasTipLabel')
        self.verticalLayout_DrawControl.addWidget(self.SelectParasTipLabel)
        self.SelectParasTipLabel.setText("绘图属性选择：")
        self.SelectParasTipLabel.setFont(QFont(Configs['字体类型']))
        self.SelectParasTipLabel.setFixedHeight(Configs['绘图文件下拉框高度'])
        # 子图显示与否的复选区域
        self.SubPlotsShowSelect = ComboCheckBox(self.Draw_Widget)
        self.SubPlotsShowSelect.setMinimumSize(QtCore.QSize(Configs['悬浮控件中按钮的宽度'], Configs['悬浮控件中按钮的高度']))
        self.SubPlotsShowSelect.loadItems(['温度', '振动加速度x', '振动加速度y', '振动加速度z', '扭矩', '压强', '钻压', '钻速'])
        self.verticalLayout_DrawControl.addWidget(self.SubPlotsShowSelect)
        # 选中按钮
        self.ReDrawButton = QtWidgets.QPushButton(self.Draw_Widget)
        self.ReDrawButton.setObjectName("ReDrawButton")
        self.verticalLayout_DrawControl.addWidget(self.ReDrawButton)
        self.ReDrawButton.setStyleSheet(styleButtonGreen)
        self.ReDrawButton.setFixedWidth(Configs['悬浮控件中按钮的宽度'])
        self.ReDrawButton.setFixedHeight(Configs['悬浮控件中按钮的高度'])

        # 直接绘制区间选择提示标签
        self.SDrawTipLabel = QtWidgets.QLabel(self.Draw_Widget)
        self.SDrawTipLabel.setObjectName('SDrawTipLabel')
        self.verticalLayout_DrawControl.addWidget(self.SDrawTipLabel)
        self.SDrawTipLabel.setText("直接绘图区间选择：")
        self.SDrawTipLabel.setFont(QFont(Configs['字体类型']))
        self.SDrawTipLabel.setFixedHeight(Configs['绘图文件下拉框高度'])
        # 直接绘制：区间选择
        # 开始下标
        self.DrawStartIndexEdit = QtWidgets.QLineEdit(self.Draw_Widget)
        self.DrawStartIndexEdit.setObjectName("DrawStartIndexEdit")
        self.verticalLayout_DrawControl.addWidget(self.DrawStartIndexEdit)
        self.DrawStartIndexEdit.setFont(QFont(Configs['字体类型']))
        # 结束下标
        self.DrawEndIndexEdit = QtWidgets.QLineEdit(self.Draw_Widget)
        self.DrawEndIndexEdit.setObjectName("DrawEndIndexEdit")
        self.verticalLayout_DrawControl.addWidget(self.DrawEndIndexEdit)
        self.DrawEndIndexEdit.setFont(QFont(Configs['字体类型']))
        # 直接绘制
        self.SDraw = QtWidgets.QPushButton(self.Draw_Widget)
        self.SDraw.setObjectName("SDraw")
        self.verticalLayout_DrawControl.addWidget(self.SDraw)
        self.SDraw.setStyleSheet(
            styleButtonGreen)
        self.SDraw.setFixedWidth(Configs['悬浮控件中按钮的宽度'])
        self.SDraw.setFixedHeight(Configs['悬浮控件中按钮的高度'])

        # 配置显示个数
        self.ShowNumEdit = QtWidgets.QLineEdit(self.Draw_Widget)
        self.ShowNumEdit.setObjectName("ShowNumEdit")
        self.verticalLayout_DrawControl.addWidget(self.ShowNumEdit)
        self.ShowNumEdit.setFont(QFont(Configs['字体类型']))
        # 配置绘制速度
        self.DrawFEdit = QtWidgets.QLineEdit(self.Draw_Widget)
        self.DrawFEdit.setObjectName("DrawFEdit")
        self.verticalLayout_DrawControl.addWidget(self.DrawFEdit)
        self.DrawFEdit.setFont(QFont(Configs['字体类型']))

        # 开始或停止绘图
        self.StopOrStart = QtWidgets.QPushButton(self.Draw_Widget)
        self.StopOrStart.setObjectName("StopOrStart")
        self.verticalLayout_DrawControl.addWidget(self.StopOrStart)
        self.StopOrStart.setStyleSheet(
            styleButtonGreen)
        self.StopOrStart.setFixedWidth(Configs['悬浮控件中按钮的宽度'])
        self.StopOrStart.setFixedHeight(Configs['悬浮控件中按钮的高度'])
        # 暂停或重启绘图
        self.TimeOutOrRestart = QtWidgets.QPushButton(self.Draw_Widget)
        self.TimeOutOrRestart.setObjectName("TimeOutOrRestart")
        self.verticalLayout_DrawControl.addWidget(self.TimeOutOrRestart)
        self.TimeOutOrRestart.setStyleSheet(styleButtonGreen)
        self.TimeOutOrRestart.setFixedWidth(Configs['悬浮控件中按钮的宽度'])
        self.TimeOutOrRestart.setFixedHeight(Configs['悬浮控件中按钮的高度'])

        # 清空当前绘图
        self.Clear = QtWidgets.QPushButton(self.Draw_Widget)
        self.Clear.setObjectName("Clear")
        self.verticalLayout_DrawControl.addWidget(self.Clear)
        self.Clear.setStyleSheet(styleButtonGreen)
        self.Clear.setFixedWidth(Configs['悬浮控件中按钮的宽度'])
        self.Clear.setFixedHeight(Configs['悬浮控件中按钮的高度'])

    # 初始化四个功能区和布局
    def InitFunctionArea(self):
        # 井下参数采集系统控制区：
        self.UndControl_Widget = QtWidgets.QTabWidget(self.dockWidgetContents_2)
        self.UndControl_Widget.setGeometry(QtCore.QRect(20, 10, Configs['悬浮控件中控件的宽度'], Configs['悬浮控件中井下控制区的高度']))
        self.UndControl_Widget.setObjectName("UndControl_Widget")
        # 绘图区
        self.Draw_Widget = QtWidgets.QTabWidget(self.dockWidgetContents_2)
        self.Draw_Widget.setGeometry(QtCore.QRect(20, 10, Configs['悬浮控件中控件的宽度'], Configs['悬浮控件中绘图区的高度']))
        self.Draw_Widget.setObjectName("Draw_Widget")
        # 软件参数显示区
        self.ParaDisc_Widget = QtWidgets.QWidget(self.dockWidgetContents_2)
        self.ParaDisc_Widget.setGeometry(QtCore.QRect(20, 10, Configs['悬浮控件中控件的宽度'], Configs['悬浮控件中参数显示区的高度']))
        self.ParaDisc_Widget.setObjectName("ParaDisc_Widget")
        # 文件转换区
        self.transfromFile_Widget = QtWidgets.QWidget(self.dockWidgetContents_2)
        self.transfromFile_Widget.setGeometry(QtCore.QRect(20, 10, Configs['悬浮控件中控件的宽度'], Configs['悬浮控件中文件转换区的高度']))
        self.transfromFile_Widget.setObjectName("transfromFile_Widget")
        # 控件区布局创建******************************************************************************
        # 参数说明区布局
        self.verticalLayout_Paras = QtWidgets.QVBoxLayout(self.ParaDisc_Widget)
        self.verticalLayout_Paras.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_Paras.setObjectName("verticalLayout_Paras")
        # 井下参数采集系统控制区
        self.verticalLayout_UnderControl = QtWidgets.QVBoxLayout(self.UndControl_Widget)
        self.verticalLayout_UnderControl.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_UnderControl.setObjectName('verticalLayout_UnderControl')
        # 绘图控制区
        self.verticalLayout_DrawControl = QtWidgets.QVBoxLayout(self.Draw_Widget)
        self.verticalLayout_DrawControl.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_DrawControl.setObjectName('verticalLayout_DrawControl')
        # 文件转换控制区
        self.verticalLayout_TransfromControl = QtWidgets.QVBoxLayout(self.transfromFile_Widget)
        self.verticalLayout_TransfromControl.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_TransfromControl.setObjectName('verticalLayout_DrawControl')

    # 初始化工具栏和悬浮控件
    def InitToolbarAndFloat(self,MainWindow):
        # 侧边工具栏***************************************************************************
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.toolBar.setStyleSheet('background-color:' + Configs['侧边工具栏背景颜色'])

        # 控制子窗口：停靠窗口*******************************************************************
        self.contrals_dockWidget = QtWidgets.QDockWidget(MainWindow)
        # QtWidgets.QDockWidget.DockWidgetFloatable|
        self.contrals_dockWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetClosable)
        self.contrals_dockWidget.setAllowedAreas(QtCore.Qt.LeftDockWidgetArea | QtCore.Qt.RightDockWidgetArea)
        self.contrals_dockWidget.setObjectName("contrals_dockWidget")
        # 设置悬浮控件为固定宽度
        self.contrals_dockWidget.setFixedWidth(int(self.WindowWeight * self.BLWeight))
        # 侧边控件悬浮widget*************************************************************************
        self.dockWidgetContents_2 = QtWidgets.QWidget()
        self.dockWidgetContents_2.setObjectName("dockWidgetContents_2")
        self.dockWidgetContents_2.setMinimumWidth(Configs['悬浮控件的最小宽度'])  # 设置最小宽度

    # 窗体大小和控件大小比例参数初始化
    def InitsizeAndBL(self,MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(Configs["初始窗口宽度"], Configs["初始窗口高度"])
        # 保存初始窗口大小
        self.WindowWeight = Configs["初始窗口宽度"]
        self.WindowHeight = Configs["初始窗口高度"]
        # 读取配置的绘图区与悬浮控件的长宽比例
        self.BLWeight = Configs['悬浮区与窗口的宽度比例']
        self.BLHeight = Configs['悬浮区与窗口的高度比例']
        # 读取配置的悬浮区与按钮控件的宽度比例
        self.BLfWeight = Configs['悬浮区与按钮的宽度比例']

    # 初始化窗体整体布局
    def InitWindow(self,MainWindow):

        # 中心区
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.centralwidget.setStyleSheet('background-color:' + Configs["绘图区后置背景颜色"])
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        # self.horizontalLayout.setContentsMargins(0,0,0,0)
        # 中心区设为绘图区：创建绘图布局
        self.DrawLayout = QtWidgets.QVBoxLayout()
        self.DrawLayout.setObjectName("DrawLayout")
        self.horizontalLayout.addLayout(self.DrawLayout)
        self.DrawLayout.setContentsMargins(0, 0, 0, 0)
        MainWindow.setCentralWidget(self.centralwidget)
        # 菜单
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, Configs["初始窗口宽度"], 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        # 状态栏
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        self.statusbar.showMessage("提示：")
        self.statusbar.setStyleSheet('border-image:url(' + Configs["状态栏背景图片"] + ')')
        MainWindow.setStatusBar(self.statusbar)

    # 窗体大小动态改变函数
    def resizeEvent(self,Event):
        # 获取当前窗口的大小
        self.WindowWeight=Event.size().width()
        self.WindowHeight=Event.size().height()
        # 重设悬浮区域的大小
        self.contrals_dockWidget.setFixedWidth(int(self.WindowWeight*self.BLWeight))
        # 重设悬浮区中四个widget的宽度和高度
        self.UndControl_Widget.setFixedWidth(int(self.WindowWeight*self.BLWeight))
        self.UndControl_Widget.setFixedHeight(int(self.WindowHeight * self.BLHeight))
        self.Draw_Widget.setFixedWidth(int(self.WindowWeight * self.BLWeight))
        self.Draw_Widget.setFixedHeight(int(self.WindowHeight * self.BLHeight))
        self.ParaDisc_Widget.setFixedWidth(int(self.WindowWeight * self.BLWeight))
        self.ParaDisc_Widget.setFixedHeight(int(self.WindowHeight * self.BLHeight))
        self.transfromFile_Widget.setFixedWidth(int(self.WindowWeight * self.BLWeight))
        self.transfromFile_Widget.setFixedHeight(int(self.WindowHeight * self.BLHeight))
        fW=int(self.WindowWeight*self.BLWeight)
        fH=int(self.WindowHeight*self.BLWeight)
        # 调整井下控制区内控件的宽度
        self.ExportEndAddrEdit.setFixedWidth(int(fW * self.BLfWeight))
        self.DrawStartIndexEdit.setFixedWidth(int(fW * self.BLfWeight))
        self.DrawEndIndexEdit.setFixedWidth(int(fW * self.BLfWeight))
        self.CheckFlashStartAddrEdit.setFixedWidth(int(fW * self.BLfWeight))
        self.ModelFormat.setFixedWidth(int(fW * self.BLfWeight))
        self.ModelExport.setFixedWidth(int(fW * self.BLfWeight))
        self.ModelSelftest.setFixedWidth(int(fW * self.BLfWeight))
        self.ModelCheckFlash.setFixedWidth(int(fW * self.BLfWeight))
        # 调整绘图区内控件的宽度
        self.SDrawTipLabel.setFixedWidth(int(fW * self.BLfWeight))
        self.ReDrawButton.setFixedWidth(int(fW * self.BLfWeight))
        self.Clear.setFixedWidth(int(fW * self.BLfWeight))
        self.DrawFEdit.setFixedWidth(int(fW * self.BLfWeight))
        self.ShowNumEdit.setFixedWidth(int(fW * self.BLfWeight))
        self.TimeOutOrRestart.setFixedWidth(int(fW * self.BLfWeight))
        self.StopOrStart.setFixedWidth(int(fW * self.BLfWeight))
        self.SDraw.setFixedWidth(int(fW * self.BLfWeight))
        self.DataFilenames.setFixedWidth(int(fW * self.BLfWeight))
        self.SelectParasTipLabel.setFixedWidth(int(fW * self.BLfWeight))
        self.SubPlotsShowSelect.setFixedWidth(int(fW * self.BLfWeight))
        # 文件转换区控件的宽度调整
        self.SaveRoadEdit.setFixedWidth(int(fW * self.BLfWeight))
        self.tranfromButton.setFixedWidth(int(fW * self.BLfWeight))
        self.DataFilenames_TransFrom.setFixedWidth(int(fW * self.BLfWeight))

    # 更新下拉框文件信息
    def ReflashFiles(self):
        # 首先清空文件
        self.DataFilenames.clear()
        Dir=Configs['绘图文件存储根目录路径']
        # 读取更目录下的所有年子目录
        YDirs=os.listdir(Dir)
        if YDirs==[]:
            return
        # 读取目录下的所有年子目录
        for i in YDirs:
            MDir=os.listdir(Dir+'/'+i+'/')
            # 读取目录下的所有月子目录
            for j in MDir:
                DDir=os.listdir(Dir+'/'+i+'/'+j+'/')
                # 读取目录下所有记录文件
                for Day in DDir:
                    Files=os.listdir(Dir+'/'+i+'/'+j+'/'+Day+'/')
                    for file in Files:
                        self.DataFilenames.addItem(i+'/'+j+'/'+Day+'/'+file)

    # 重新刷新文件，转换文件
    def TransFlashFiles(self):
        self.DataFilenames_TransFrom.clear()
        files = []
        Dir = Configs['绘图文件存储根目录路径']
        # 读取更目录下的所有年子目录
        YDirs = os.listdir(Dir)
        if YDirs == []:
            self.DataFilenames_TransFrom.loadItems(['空'])
            return
        # 读取目录下的所有年子目录
        for i in YDirs:
            MDir = os.listdir(Dir + '/' + i + '/')
            # 读取目录下的所有月子目录
            for j in MDir:
                DDir = os.listdir(Dir + '/' + i + '/' + j + '/')
                # 读取目录下所有记录文件
                for Day in DDir:
                    Files = os.listdir(Dir + '/' + i + '/' + j + '/' + Day + '/')
                    for file in Files:
                        files.append(Dir + i + '/' + j + '/' + Day + '/' + file)
        self.DataFilenames_TransFrom.loadItems(files)

    # 显示停靠控制区域
    def ShowContral(self):
        self.contrals_dockWidget.show()

    # 页面初始化加载
    def MyFunction_init(self):#加载页面时的一些初始化设定操作
        self.contrals_dockWidget.setVisible(False)  # 初始隐藏停靠控件
        self.ShowNumEdit.setValidator(QtGui.QIntValidator(1,Configs['绘图点数上限']))# 设置只能输入数字且输入数字的范围
        self.DrawFEdit.setValidator(QtGui.QIntValidator(1, Configs['绘图时间上限']))  # 设置只能输入数字且输入数字的范围:10秒之内的频率
        self.DrawStartIndexEdit.setValidator(QtGui.QIntValidator(0, Configs['直接绘制的区间起始限制']))
        self.DrawEndIndexEdit.setValidator(QtGui.QIntValidator(0, Configs['直接绘制的区间结束限制']))

    # 井下控制区控件的文字显示初始化
    def InitShowUndeControl(self,_translate):
        self.UndControl.setText(_translate("MainWindow", "井下参数采集系统控制"))
        self.ExportEndAddrEdit.setPlaceholderText(_translate("MainWindow", '导出模式结束地址配置'))
        self.ModelExport.setText(_translate("MainWindow", "导出模式"))
        self.ModelFormat.setText(_translate("MainWindow", "格式化模式"))
        self.ModelSelftest.setText(_translate("MainWindow", "自测模式"))
        self.CheckFlashStartAddrEdit.setPlaceholderText(_translate("MainWindow", "检查Flash开始地址配置"))
        self.ModelCheckFlash.setText(_translate("MainWindow", "检查Flash模式"))

    # 绘图区控件的文字显示初始化
    def InitShowDraw(self, _translate):
        self.DrawStartIndexEdit.setPlaceholderText(_translate("MainWindow", '直接绘制的起始帧序号'))
        self.DrawEndIndexEdit.setPlaceholderText(_translate("MainWindow", '直接绘制的结束帧序号'))
        self.DrawControl.setText(_translate("MainWindow", "绘图控制"))
        self.StopOrStart.setText(_translate("MainWindow", "开始动态绘制"))
        self.SDraw.setText(_translate("MainWindow", "直接绘制"))
        self.TimeOutOrRestart.setText(_translate("MainWindow", "暂停动态绘制"))
        self.Clear.setText(_translate("MainWindow", "清空绘图"))
        self.ReDrawButton.setText(_translate("MainWindow", "选中"))
        self.ShowNumEdit.setPlaceholderText(_translate("MainWindow", "显示个数设置："))
        self.DrawFEdit.setPlaceholderText(_translate("MainWindow", "绘制速度配置（毫秒）："))

    # 参数显示区控件的文字显示初始化
    def InitShowParas(self, _translate):
        self.ParaDisc.setText(_translate("MainWindow", "软件参数说明"))

    # 文件转换区控件的文字显示初始化
    def InitShowTransfromFiles(self, _translate):
        self.tranfromButton.setText(_translate("MainWindow", "转换"))
        self.tansfromFile.setText(_translate("MainWindow", "文件转换"))

    # 加载控件标题和文字
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", ""))
        self.toolBar.setWindowTitle(_translate("MainWindow", ""))
        # 井下控制区控件的文字显示
        self.InitShowUndeControl(_translate)
        # 绘图区控件的文字显示
        self.InitShowDraw(_translate)
        # 参数显示区控件的文字显示
        self.InitShowParas(_translate)
        # 文件转换区的控件文字显示
        self.InitShowTransfromFiles(_translate)







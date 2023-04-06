#--coding:utf-8--
# Configs={
#         '按钮高度':30,'按钮初始颜色':'#96c24e','按钮工作中颜色':'#ec2c64',\
#         '按钮悬停颜色':'#648e93','按钮按下颜色':'#553b18',\
#         '按钮样式':'QPushButton{border-radius:2px;border: 1px grey solid;padding: 1px 1px 1px 1px;}',\
#         '悬浮控件中按钮的宽度':188,'悬浮控件中按钮的高度':30,\
#         '字体类型':'黑体','字体大小':'10px','字体颜色':'#000000',\
#         '绘图区后置背景颜色':'#ff9900',\
#         '分割空白的高度':10,'分割空白的颜色':'#ff9900',\
#         '初始窗口宽度':931,'初始窗口高度':684,\
#         '软件icon路径':'./Pics/图标.ico',\
#         '状态栏背景图片':'./Pics/statuBack.jpg',\
#         '软件名称':'井上数据回放分析软件',\
#         '侧边工具栏背景颜色':'#10aec2',\
#         '悬浮控件的最小宽度':220,\
#         '悬浮控件中控件的宽度':193,'悬浮控件中井下控制区的高度':310,\
#         '悬浮控件中绘图区的高度':500,'悬浮控件中参数显示区的高度':310,\
#         '绘图文件下拉框高度':25,\
#         '绘图文件存储根目录路径':'./datasDir/',\
#         '绘图点数上限':10000,'绘图时间上限':10000,\
#         '初始绘图速度':500,\
#         '定时器循环监视时间':100,\
#         '默认绘图停止的循环绘图时间':1000000,\
#         '绘图控件的背景颜色':'#541e24',\
#         '绘图曲线颜色':'#2d0c13','绘图标记点颜色':'#96c24e'
#         }
Thisfile=r'./Config/configs.csv'
import csv
# with open(files+'configs.csv','w',encoding='utf-8',newline='') as f:
#     cw=csv.writer(f)
#     for key,v in Configs.items():
#         cw.writerow([key,type(v),v])
# if type(files)==str:
#         print(1)

def GetConfigsToDict():
        result = {}
        with open(Thisfile, 'r', encoding='utf-8', newline='') as f:
                cr=csv.reader(f)
                for line in cr:
                        if line[1]=='<class \'int\'>':
                                result[line[0]]=int(line[2])
                        elif line[1]=='<class \'str\'>':
                                result[line[0]]=line[2]
                        elif line[1]=='<class \'float\'>':
                                result[line[0]] = float(line[2])
        return result

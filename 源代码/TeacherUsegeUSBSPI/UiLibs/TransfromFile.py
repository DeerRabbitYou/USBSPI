#--coding:utf-8--
import csv
import os
from UiLibs.save_get_Datas import OperateDatas
import numpy as np
class TF():
    def __init__(self,SaveDir,H5SaveDir):
        # 存储目录路径
        self.SaveDir=SaveDir

    def TransFrom(self,files,keys):
        # 创建H5文件操作对象
        self.OPh5 = OperateDatas('')
        # 读取不同文件的数据
        # 存储数据： {文件名：{关键词：[数据]}}
        RetDatas = {}
        for file in files:
            if os.path.exists(file)==False:
                continue
            # 读取文件
            datas, flag = self.OPh5.ReadDatas_Keys(file, keys)
            if flag == False:
                continue
            # 创建关键字
            RetDatas[file] = {}
            # 按关键字读取数据
            for index in range(len(keys)):
                RetDatas[file][keys[index]] = datas[:,index]
        if RetDatas=={}:
            return None
        # 将数据按文件路径为名进行文件转换
        # 文件存储路径为
        for filename in RetDatas.keys():
            # 生成文件名
            name=filename.replace('/','_')
            name=name.replace('.h5','.csv')
            name = name.replace('._', '_')
            fileRoad=self.SaveDir+name
            # print(RetDatas[filename])
            # 创建文件
            with open(fileRoad,'w',encoding='utf-8-sig',newline='') as f:
                cw=csv.writer(f)
                results=[]
                for key in keys:
                    result=[key]
                    result.extend(RetDatas[filename][key])
                    results.append(result)
                results=np.array(results)
                results=results.T
                cw.writerows(results)
        return RetDatas








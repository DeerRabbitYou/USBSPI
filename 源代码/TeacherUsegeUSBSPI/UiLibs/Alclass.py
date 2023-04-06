#encoding:utf-8
#使用卡尔曼算法进行滤波

import numpy as np
#卡尔曼滤波算法
class KF():
    def __init__(self,A,H,Q,R,Xk):
        self.A=A.copy()
        self.H=H.copy()
        self.Q=Q.copy()
        self.R=R.copy()
        self.N=A.shape[0]
        self.M=H.shape[0]
        self.P=np.zeros((self.N,self.N))
        #初始化数据
        self.Xk=Xk.copy()

    def predict(self,X):
        # 1.0
        Xk = np.dot(self.A, self.Xk)
        # 2.0
        Pkk = np.dot(np.dot(self.A, self.P), self.A.T) + self.Q
        # 3.0
        KK = np.dot(np.dot(Pkk, self.H.T), np.linalg.pinv(np.dot(np.dot(self.H, self.Pkk), self.H.T) + self.R))
        # 4.0
        self.Xk = Xk + np.dot(KK, (np.array([X]) - np.dot(self.H, Xk)))
        # 5.0
        self.P = np.dot((np.identity(self.N) - np.dot(KK, self.H)), Pkk)
        return self.Xk.copy()

#均值滤波算法
class Mean():
    def __init__(self,N,flag=0):
        self.N=N
        if N>=3:
           self.Flag=flag
        else:
            self.Flag=1
        self.PriDatas=[]
    def predict(self,X):
        if len(self.PriDatas)<self.N:
            self.PriDatas.append(X)
        else:
            self.PriDatas=[self.PriDatas[i] for i in range(1,len(self.PriDatas))]
            self.PriDatas.append(X)
        if self.Flag==0 and len(self.PriDatas)>=3:#去除最高，最低值后求平均值
            sorts=np.array(np.sort(self.PriDatas))
            return np.mean(sorts[1:len(sorts)-1])
        else:
            return np.mean(self.PriDatas)



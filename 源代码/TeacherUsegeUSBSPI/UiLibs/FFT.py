#--coding:utf-8--
from scipy.fftpack import fft,ifft,fftfreq,rfft,rfftfreq,irfft
import matplotlib.pyplot as plt
import numpy as np
#最高频率围为220hz，因此采样频率至少为440
fs=2000#采样频率设置为500hz
#则一秒的采样点数为500
N=2000
x=np.linspace(0,1,N)
#频率间隔为1hz
#测试信号y=8*sin(2*pi*200*x)+5.5cos(2*pi*210*x)-55sin(2*pi*220*x):时域表达
y=7*np.sin(2*np.pi*200*x)+5.5*np.cos(2*np.pi*210*x)-3.4*np.sin(2*np.pi*220*x)
plt.plot(x,y)
plt.show()

#FFT
result=fft(y)
#绝对值
ABS=np.abs(result)
#幅度计算
Amplitude=ABS/(N/2)
#频率计算
Frequency=np.linspace(0,N,N)
plt.plot(Frequency,Amplitude)
plt.show()

#rFFT
result=rfft(y)
xf=rfftfreq(N,1/N)
plt.plot(xf,np.abs(result))
plt.show()

#irfft
Iresult=irfft(result)
plt.plot(Iresult)
plt.show()
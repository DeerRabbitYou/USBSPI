using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Runtime.InteropServices;

namespace USB2XXX
{
    class USB2PWM
    {
        //定义函数返回错误代码
        public const Int32 PWM_SUCCESS = (0);   //函数执行成功
        public const Int32 PWM_ERR_NOT_SUPPORT = (-1);  //适配器不支持该函数
        public const Int32 PWM_ERR_USB_WRITE_FAIL = (-2);  //USB写数据失败
        public const Int32 PWM_ERR_USB_READ_FAIL = (-3);  //USB读数据失败
        public const Int32 PWM_ERR_CMD_FAIL = (-4);  //命令执行失败
        //定义初始化PWM的数据类型
        public struct PWM_CONFIG
        {
            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 8)]
            public UInt16[] Prescaler;  //预分频器
            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 8)]
            public UInt16[] Precision;  //占空比调节精度
            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 8)]
            public UInt16[] Pulse;      //占空比，实际占空比=(Pulse/Precision)*100%
            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 8)]
            public UInt16[] Phase;      //波形相位，取值0到Precision-1
            [MarshalAs(UnmanagedType.ByValArray, SizeConst = 8)]
            public Byte[] Polarity;    //波形极性
            public Byte ChannelMask;    //通道号
        }
        //定义PWM测量数据
        public struct PWM_CAP_DATA
        {
            public UInt16 LowValue;//低电平时间，单位为us
            public UInt16 HighValue;//高电平时间，单位为us
        }
        //UTA0101 UTA0201 UTA0301 UTA0302引脚定义参考引脚定义说明文档，主频为200M
        //UTA0403 UTA0402 UTA0401  LIN1对应的PWM通道为0x40,LIN2对应的PWM通道为0x80，主频84M
        //UTA0503  LIN1对应的PWM通道为0x02,LIN2对应的PWM通道为0x04，主频220M
        //UTA0504  LIN1->0x01 LIN2->0x02 LIN3->0x04 LIN4->0x08 DO0->0x10 DO1->0x20,主频240M
        //函数定义
        [DllImport("USB2XXX.dll")]
        public static extern Int32 PWM_Init(Int32 DevHandle, ref PWM_CONFIG pConfig);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 PWM_Start(Int32 DevHandle,Byte ChannelMask,Int32 RunTimeUs);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 PWM_SetPulse(Int32 DevHandle,Byte ChannelMask,UInt16[] pPulse);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 PWM_SetPhase(Int32 DevHandle,Byte ChannelMask,UInt16[] pPhase);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 PWM_SetFrequency(Int32 DevHandle,Byte ChannelMask,UInt16[] pPrescaler,UInt16[] pPrecision);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 PWM_Stop(Int32 DevHandle,Byte ChannelMask);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 PWM_CAP_Init(Int32 DevHandle, Byte Channel,Byte TimePrecUs);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 PWM_CAP_GetData(Int32 DevHandle, Byte Channel,ref PWM_CAP_DATA pPWMData);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 PWM_CAP_Stop(Int32 DevHandle, Byte Channel);
    }
}

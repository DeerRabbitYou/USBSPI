Imports System.Runtime.InteropServices
Module usb2pwm
    '定义初始化PWM的数据类型
    Public Structure PWM_CONFIG
        <MarshalAs(UnmanagedType.ByValArray, SizeConst:=8)> _
        Dim Prescaler As UInt16()
        <MarshalAs(UnmanagedType.ByValArray, SizeConst:=8)> _
        Dim Precision As UInt16()
        <MarshalAs(UnmanagedType.ByValArray, SizeConst:=8)> _
        Dim Pulse As UInt16()
        <MarshalAs(UnmanagedType.ByValArray, SizeConst:=8)> _
        Dim Phase As UInt16()
        <MarshalAs(UnmanagedType.ByValArray, SizeConst:=8)> _
        Dim Polarity As Byte()
        Dim ChannelMask As Byte  '通道号，若要使能某个通道，则对应位为1，最低位对应通道0
    End Structure
    '定义PWM测量数据
    Public Structure PWM_CAP_DATA
        Dim LowValue As UInt16
        Dim HighValue As UInt16
    End Structure
    '定义函数返回错误代码
    Public Const PWM_SUCCESS As Int32 = (0)             '函数执行成功
    Public Const PWM_ERR_NOT_SUPPORT As Int32 = (-1)    '适配器不支持该函数
    Public Const PWM_ERR_USB_WRITE_FAIL As Int32 = (-2) 'USB写数据失败
    Public Const PWM_ERR_USB_READ_FAIL As Int32 = (-3)  'USB读数据失败
    Public Const PWM_ERR_CMD_FAIL As Int32 = (-4)       '命令执行失败

Declare Function PWM_Init Lib "USB2XXX.dll" (ByVal DevHandle As UInt32, ByRef pConfig As PWM_CONFIG) As Int32
Declare Function PWM_Start Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal ChannelMask As Byte,ByVal RunTimeUs As Int32) As Int32
Declare Function PWM_SetPulse Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal ChannelMask As Byte,<[In]()> ByVal pPulse As Int16()) As Int32
Declare Function PWM_SetPhase Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal ChannelMask As Byte,<[In]()> ByVal pPhase As Int16()) As Int32
Declare Function PWM_SetFrequency Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal ChannelMask As Byte,<[In]()> ByVal pPrescaler As Int16(),<[In]()> ByVal pPrecision As Int16()) As Int32
Declare Function PWM_Stop Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal ChannelMask As Byte) As Int32

Declare Function PWM_CAP_Init Lib "USB2XXX.dll" (ByVal DevHandle As UInt32, ByVal Channel As Byte) As Int32
Declare Function PWM_CAP_GetData Lib "USB2XXX.dll" (ByVal DevHandle As UInt32, ByVal Channel As Byte,ByRef pPWMData As PWM_CAP_DATA) As Int32
Declare Function PWM_CAP_Stop Lib "USB2XXX.dll" (ByVal DevHandle As UInt32, ByVal Channel As Byte) As Int32

End Module

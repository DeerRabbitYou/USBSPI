Attribute VB_Name = "usb2pwm"
Public Const PWM_SUCCESS             As Long = (0)
Public Const PWM_ERR_NOT_SUPPORT     As Long = (-1)
Public Const PWM_ERR_USB_WRITE_FAIL  As Long = (-2)
Public Const PWM_ERR_USB_READ_FAIL   As Long = (-3)
Public Const PWM_ERR_CMD_FAIL        As Long = (-4)

Public Type PWM_CONFIG
    Prescaler(7) As Integer '预分频器
    Precision(7) As Integer '占空比调节精度,实际频率 = 168MHz/(Prescaler*Precision)
    Pulse(7) As Integer     '占空比，实际占空比=(Pulse/Precision)*100%
    Phase(7) As Integer     '波形相位，取值0到Precision-1
    Polarity(7) As Byte '波形极性，取值0或者1
    ChannelMask As Byte '通道号，若要使能某个通道，则对应位为1，最低位对应通道0
End Type

Public Type PWM_CAP_DATA
    LowValue As Integer     '低电平时间，单位为us
    HighValue As Integer    '高电平时间，单位为us
End Type

'UTA0403 UTA0402 UTA0401  LIN1对应的PWM通道为0x40,LIN2对应的PWM通道为0x80
'UTA0503  LIN1对应的PWM通道为0x02,LIN2对应的PWM通道为0x04
Declare Function PWM_Init Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByRef pConfig As PWM_CONFIG) As Long
Declare Function PWM_Start Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal ChannelMask As Byte, ByVal RunTimeUs As Long) As Long
Declare Function PWM_SetPulse Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal ChannelMask As Byte, ByVal pPulse As Any) As Long
Declare Function PWM_SetPhase Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal ChannelMask As Byte, ByVal pPhase As Any) As Long
Declare Function PWM_SetFrequency Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal ChannelMask As Byte, ByVal pPrescaler As Any, ByVal pPrecision As Any) As Long
Declare Function PWM_Stop Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal ChannelMask As Byte) As Long
'LIN1对应的PWM通道为0,LIN2对应的PWM通道为1
Declare Function PWM_CAP_Init Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal Channel As Byte) As Long
Declare Function PWM_CAP_GetData Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal Channel As Byte, ByRef pPWMData As PWM_CAP_DATA) As Long
Declare Function PWM_CAP_Stop Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal Channel As Byte) As Long

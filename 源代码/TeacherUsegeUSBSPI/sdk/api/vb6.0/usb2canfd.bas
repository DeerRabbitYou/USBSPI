Attribute VB_Name = "usb2canfd"

Public Type CANFD_MSG
    ID As Long
    DLC As 
    Flags As Byte
    __Res0 As Byte
    TimeStampHigh As Byte
    TimeStamp As Long
    Data(63) As Byte
End Type

Public Type CANFD_INIT_CONFIG
    Mode As Byte
    ISOCRCEnable As Byte
    RetrySend As Byte
    ResEnable As Byte
    NBT_BRP As Byte
    NBT_SEG1 As Byte
    NBT_SEG2 As Byte
    NBT_SJW As Byte
    DBT_BRP As Byte
    DBT_SEG1 As Byte
    DBT_SEG2 As Byte
    DBT_SJW As Byte
    __Res0(7) As Byte
End Type

Public Type CANFD_FILTER_CONFIG
    Enable As Byte
    Index As Byte
    __Res0 As Byte
    __Res1 As Byte
    ID_Accept As Long
    ID_Mask As Long
End Type

Public Type CANFD_BUS_ERROR
    TEC As Byte
    REC As Byte
    Flags As Byte
    __Res0 As Byte
End Type

Public Type CANFD_DIAGNOSTIC
    NREC As Byte
    NTEC As Byte
    DREC As Byte
    DTEC As Byte
    ErrorFreeMsgCount As Integer
    Flags As Integer
End Type

'函数返回值错误信息定义
Public Const CANFD_SUCCESS As Long = (0)   '函数执行成功
Public Const CANFD_ERR_NOT_SUPPORT As Long = (-1)  '适配器不支持该函数
Public Const CANFD_ERR_USB_WRITE_FAIL As Long = (-2)  'USB写数据失败
Public Const CANFD_ERR_USB_READ_FAIL As Long = (-3)  'USB读数据失败
Public Const CANFD_ERR_CMD_FAIL As Long = (-4)  '命令执行失败
'CANFD_MSG.ID定义
Public Const CANFD_MSG_FLAG_RTR As Long = (&H40000000)
Public Const CANFD_MSG_FLAG_IDE As Long = (&H80000000)
Public Const CANFD_MSG_FLAG_ID_MASK As Long = (&H1FFFFFFF)
'CANFD_MSG.Flags定义
Public Const CANFD_MSG_FLAG_BRS As Byte = (&H01)  'CANFD加速帧标志
Public Const CANFD_MSG_FLAG_ESI As Byte = (&H02)
Public Const CANFD_MSG_FLAG_FDF As Byte = (&H04)  'CANFD帧标志
Public Const CANFD_MSG_FLAG_TXD As Byte = (&H80)
'CANFD_DIAGNOSTIC.Flags定义
Public Const CANFD_DIAGNOSTIC_FLAG_NBIT0_ERR     (&H0001)'在发送报文（或应答位、主动错误标志或过载标志）期间，器件要发送显性电平（逻辑值为0的数据或标识符位），但监视的总线值为隐性。
Public Const CANFD_DIAGNOSTIC_FLAG_NBIT1_ERR As Long = (&H0002)'在发送报文（仲裁字段除外）期间，器件要发送隐性电平（逻辑值为1的位），但监视到的总线值为显性。
Public Const CANFD_DIAGNOSTIC_FLAG_NACK_ERR As Long = (&H0004)'发送报文未应答。
Public Const CANFD_DIAGNOSTIC_FLAG_NFORM_ERR As Long = (&H0008)'接收报文的固定格式部分格式错误。
Public Const CANFD_DIAGNOSTIC_FLAG_NSTUFF_ERR  As Long = (&H0010)'在接收报文的一部分中，序列中包含了5个以上相等位，而报文中不允许出现这种序列。
Public Const CANFD_DIAGNOSTIC_FLAG_NCRC_ERR As Long = (&H0020)'接收的报文的CRC校验和不正确。输入报文的CRC与通过接收到的数据计算得到的CRC不匹配。
Public Const CANFD_DIAGNOSTIC_FLAG_TXBO_ERR As Long = (&H0080)'器件进入离线状态（且自动恢复）。
Public Const CANFD_DIAGNOSTIC_FLAG_DBIT0_ERR As Long = (&H0100)'见NBIT0_ERR
Public Const CANFD_DIAGNOSTIC_FLAG_DBIT1_ERR As Long = (&H0200)'见NBIT1_ERR
Public Const CANFD_DIAGNOSTIC_FLAG_DFORM_ERR As Long = (&H0800)'见NFORM_ERR
Public Const CANFD_DIAGNOSTIC_FLAG_DSTUFF_ERR As Long = (&H1000)'见NSTUFF_ERR
Public Const CANFD_DIAGNOSTIC_FLAG_DCRC_ERR As Long = (&H2000)'见NCRC_ERR
Public Const CANFD_DIAGNOSTIC_FLAG_ESI_ERR As Long = (&H4000)'接收的CAN FD报文的ESI标志置1
Public Const CANFD_DIAGNOSTIC_FLAG_DLC_MISMATCH As Long = (&H8000)'DLC不匹配,在发送或接收期间，指定的DLC大于FIFO元素的PLSIZE
'CANFD_BUS_ERROR.Flags定义
Public Const CANFD_BUS_ERROR_FLAG_TX_RX_WARNING As Byte = (&H01)
Public Const CANFD_BUS_ERROR_FLAG_RX_WARNING As Byte = (&H02)
Public Const CANFD_BUS_ERROR_FLAG_TX_WARNING As Byte = (&H04)
Public Const CANFD_BUS_ERROR_FLAG_RX_BUS_PASSIVE As Byte = (&H08)
Public Const CANFD_BUS_ERROR_FLAG_TX_BUS_PASSIVE As Byte = (&H10)
Public Const CANFD_BUS_ERROR_FLAG_TX_BUS_OFF As Byte = (&H20)

Declare Function CANFD_GetCANSpeedArg Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByRef pCanConfig As CANFD_INIT_CONFIG, ByVal SpeedBpsNBT As Long, ByVal SpeedBpsDBT As Long) As Long
Declare Function CANFD_Init Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal CANIndex As Byte, ByRef pCanConfig As CANFD_INIT_CONFIG) As Long
Declare Function CANFD_StartGetMsg Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal CANIndex As Byte) As Long
Declare Function CANFD_StopGetMsg Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal CANIndex As Byte) As Long
Declare Function CANFD_SendMsg Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal CANIndex As Byte, ByVal pCanSendMsg As Long,unsigned ByVal SendMsgNum As Long) As Long
Declare Function CANFD_GetMsg Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal CANIndex As Byte, ByVal pCanGetMsg As Long,ByVal BufferSize As Long) As Long
Declare Function CANFD_ClearMsg Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal CANIndex As Byte) As Long
Declare Function CANFD_SetFilter Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal CANIndex As Byte, ByRef pCanFilter As CANFD_FILTER_CONFIG,ByVal Len As Byte) As Long
Declare Function CANFD_GetDiagnostic Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal CANIndex As Byte, ByRef pCanDiagnostic As CANFD_DIAGNOSTIC) As Long
Declare Function CANFD_GetBusError Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal CANIndex As Byte, ByRef pCanBusError As CANFD_BUS_ERROR) As Long
Declare Function CANFD_SetSchedule Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal CANIndex As Byte, ByVal pCanMsgTab As Long,ByVal pMsgNum  As Long,ByVal pSendTimes As Long,ByVal MsgTabNum As Byte) As Long
Declare Function CANFD_StartSchedule Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal CANIndex As Byte, ByVal MsgTabIndex As Byte,ByVal TimePrecMs As Byte,ByVal OrderSend As Byte) As Long
Declare Function CANFD_StopSchedule Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal CANIndex As Byte) As Long



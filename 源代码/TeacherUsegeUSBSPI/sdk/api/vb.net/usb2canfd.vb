Imports System.Runtime.InteropServices
Module usb2canfd
    Public Structure CANFD_MSG
        Dim ID As UInt32
        Dim DLC As Byte
        Dim Flags As Byte
        Dim __Res0 As Byte
        Dim TimeStampHigh As Byte
        Dim TimeStamp As UInt32
        <MarshalAs(UnmanagedType.ByValArray, SizeConst:=64)> _
        Dim Data As Byte()
    End Structure

    Public Structure CANFD_INIT_CONFIG
        Dim Mode As Byte
        Dim ISOCRCEnable As Byte
        Dim RetrySend As Byte
        Dim ResEnable As Byte
        Dim NBT_BRP As Byte
        Dim NBT_SEG1 As Byte
        Dim NBT_SEG2 As Byte
        Dim NBT_SJW As Byte
        Dim DBT_BRP As Byte
        Dim DBT_SEG1 As Byte
        Dim DBT_SEG2 As Byte
        Dim DBT_SJW As Byte
        <MarshalAs(UnmanagedType.ByValArray, SizeConst:=8)> _
        Dim __Res0 As Byte()
    End Structure

    Public Structure CANFD_DIAGNOSTIC
        Dim NREC As Byte
        Dim NTEC As Byte
        Dim DREC As Byte
        Dim DTEC As Byte
        Dim ErrorFreeMsgCount As UInt16
        Dim Flags As UInt16
    End Structure

    Public Structure CANFD_BUS_ERROR
        Dim TEC As Byte
        Dim REC As Byte
        Dim Flags As Byte
        Dim __Res0 As Byte
    End Structure

    Public Structure CANFD_FILTER_CONFIG
        Dim Enable As Byte
        Dim Index As Byte
        Dim __Res0 As Byte
        Dim __Res1 As Byte
        Dim ID_Accept As UInt32
        Dim ID_Mask As UInt32
    End Structure

    Public Const CANFD_SUCCESS As Int32 = 0
    Public Const CANFD_ERR_NOT_SUPPORT As Int32 = -1
    Public Const CANFD_ERR_USB_WRITE_FAIL As Int32 = -2
    Public Const CANFD_ERR_USB_READ_FAIL As Int32 = -3
    Public Const CANFD_ERR_CMD_FAIL As Int32 = -4

'CANFD_MSG.ID定义
    Public Const CANFD_MSG_FLAG_RTR      =(&H40000000)
    Public Const CANFD_MSG_FLAG_IDE      =(&H80000000)
    Public Const CANFD_MSG_FLAG_ID_MASK  =(&H1FFFFFFF)
'CANFD_MSG.Flags定义
    Public Const CANFD_MSG_FLAG_BRS      =(&H01)  'CANFD加速帧标志
    Public Const CANFD_MSG_FLAG_ESI      =(&H02)
    Public Const CANFD_MSG_FLAG_FDF      =(&H04)  'CANFD帧标志
    Public Const CANFD_MSG_FLAG_TXD      =(&H80)
'CANFD_DIAGNOSTIC.Flags定义
    Public Const CANFD_DIAGNOSTIC_FLAG_NBIT0_ERR     =(&H0001)'在发送报文（或应答位、主动错误标志或过载标志）期间，器件要发送显性电平（逻辑值为0的数据或标识符位），但监视的总线值为隐性。
    Public Const CANFD_DIAGNOSTIC_FLAG_NBIT1_ERR     =(&H0002)'在发送报文（仲裁字段除外）期间，器件要发送隐性电平（逻辑值为1的位），但监视到的总线值为显性。
    Public Const CANFD_DIAGNOSTIC_FLAG_NACK_ERR      =(&H0004)'发送报文未应答。
    Public Const CANFD_DIAGNOSTIC_FLAG_NFORM_ERR     =(&H0008)'接收报文的固定格式部分格式错误。
    Public Const CANFD_DIAGNOSTIC_FLAG_NSTUFF_ERR    =(&H0010)'在接收报文的一部分中，序列中包含了5个以上相等位，而报文中不允许出现这种序列。
    Public Const CANFD_DIAGNOSTIC_FLAG_NCRC_ERR      =(&H0020)'接收的报文的CRC校验和不正确。输入报文的CRC与通过接收到的数据计算得到的CRC不匹配。
    Public Const CANFD_DIAGNOSTIC_FLAG_TXBO_ERR      =(&H0080)'器件进入离线状态（且自动恢复）。
    Public Const CANFD_DIAGNOSTIC_FLAG_DBIT0_ERR     =(&H0100)'见NBIT0_ERR
    Public Const CANFD_DIAGNOSTIC_FLAG_DBIT1_ERR     =(&H0200)'见NBIT1_ERR
    Public Const CANFD_DIAGNOSTIC_FLAG_DFORM_ERR     =(&H0800)'见NFORM_ERR
    Public Const CANFD_DIAGNOSTIC_FLAG_DSTUFF_ERR    =(&H1000)'见NSTUFF_ERR
    Public Const CANFD_DIAGNOSTIC_FLAG_DCRC_ERR      =(&H2000)'见NCRC_ERR
    Public Const CANFD_DIAGNOSTIC_FLAG_ESI_ERR       =(&H4000)'接收的CAN FD报文的ESI标志置1
    Public Const CANFD_DIAGNOSTIC_FLAG_DLC_MISMATCH  =(&H8000)'DLC不匹配,在发送或接收期间，指定的DLC大于FIFO元素的PLSIZE
'CANFD_BUS_ERROR.Flags定义
    Public Const CANFD_BUS_ERROR_FLAG_TX_RX_WARNING   =(&H01)
    Public Const CANFD_BUS_ERROR_FLAG_RX_WARNING      =(&H02)
    Public Const CANFD_BUS_ERROR_FLAG_TX_WARNING      =(&H04)
    Public Const CANFD_BUS_ERROR_FLAG_RX_BUS_PASSIVE  =(&H08)
    Public Const CANFD_BUS_ERROR_FLAG_TX_BUS_PASSIVE  =(&H10)
    Public Const CANFD_BUS_ERROR_FLAG_TX_BUS_OFF      =(&H20)

    Declare Function CANFD_Init Lib "USB2XXX.dll" (ByVal DevHandle As UInt32, ByVal CANIndex As Byte, ByRef pCanConfig As CANFD_INIT_CONFIG) As Int32
    Declare Function CANFD_StartGetMsg Lib "USB2XXX.dll" (ByVal DevHandle As UInt32, ByVal CANIndex As Byte) As Int32
    Declare Function CANFD_StopGetMsg Lib "USB2XXX.dll" (ByVal DevHandle As UInt32, ByVal CANIndex As Byte) As Int32
    Declare Function CANFD_SendMsg Lib "USB2XXX.dll" (ByVal DevHandle As UInt32, ByVal CANIndex As Byte, ByVal pCanSendMsg As CANFD_MSG(),ByVal SendMsgNum As Int32) As Int32
    Declare Function CANFD_GetMsg Lib "USB2XXX.dll" (ByVal DevHandle As UInt32, ByVal CANIndex As Byte, <Out()> ByVal pCanGetMsg As CANFD_MSG(),ByVal BufferSize As Int32) As Int32
    Declare Function CANFD_ClearMsg Lib "USB2XXX.dll" (ByVal DevHandle As UInt32, ByVal CANIndex As Byte) As Int32
    Declare Function CANFD_SetFilter Lib "USB2XXX.dll" (ByVal DevHandle As UInt32, ByVal CANIndex As Byte, ByRef pCanFilter As CANFD_FILTER_CONFIG,ByVal Len As Byte) As Int32
    Declare Function CANFD_GetDiagnostic Lib "USB2XXX.dll" (ByVal DevHandle As UInt32, ByVal CANIndex As Byte, ByRef pCanDiagnostic As CANFD_DIAGNOSTIC) As Int32
    Declare Function CANFD_GetBusError Lib "USB2XXX.dll" (ByVal DevHandle As UInt32, ByVal CANIndex As Byte, ByRef pCanBusError As CANFD_BUS_ERROR) As Int32
    Declare Function CANFD_SetSchedule Lib "USB2XXX.dll" (ByVal DevHandle As UInt32, ByVal CANIndex As Byte, ByVal pCanMsgTab As CANFD_MSG(),ByVal pMsgNum As Byte(),ByVal pSendTimes As Short(),ByVal MsgTabNum As Byte) As Int32
    Declare Function CANFD_StartSchedule Lib "USB2XXX.dll" (ByVal DevHandle As UInt32, ByVal CANIndex As Byte, ByVal MsgTabIndex As Byte,ByVal TimePrecMs As Byte,ByVal OrderSend As Byte) As Int32
    Declare Function CANFD_StopSchedule Lib "USB2XXX.dll" (ByVal DevHandle As UInt32, ByVal CANIndex As Byte)


End Module

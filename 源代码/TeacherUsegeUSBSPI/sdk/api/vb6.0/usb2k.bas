Attribute VB_Name = "u2b2k"

Public Type K_MSG
    Fmt As Byte         'Format byte
    TgtAddr As Byte     'This is the target address for the message. It may be a physical or a functional address.
    SrcAddr As Byte     'Source address
    Len As Byte         'This byte is provided if the length in the header byte Fmt.DataLen is set to 0.
    SId As Byte         'Service Identification byte
    Data(254) As Byte   'depending on service
    CS As Byte          'Checksum byte
End Type

Public Const K_SUCCESS                  As Long = (0)   //函数执行成功
Public Const K_ERR_NOT_SUPPORT          As Long = (-1)  //适配器不支持该函数
Public Const K_ERR_USB_WRITE_FAIL       As Long = (-2)  //USB写数据失败
Public Const K_ERR_USB_READ_FAIL        As Long = (-3)  //USB读数据失败
Public Const K_ERR_CMD_FAIL             As Long = (-4)  //命令执行失败
Public Const K_ERR_SERVER_NO_RESPONSE   As Long = (-5)  //ECU无响应
Public Const K_ERR_RESPONSE             As Long = (-6)  //ECU响应数据错误
Public Const K_ERR_SEND_DATA            As Long = (-7)  //数据发送出错
Public Const K_ERR_CHECK_ERROR          As Long = (-8)  //数据发送出错

Declare Function K_Init Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal Channel As Byte,ByVal BaudRate As Long) As Long
Declare Function K_5BaudInit Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal Channel As Byte,ByVal Addr As Byte,ByRef pKB1 As Byte,ByRef pKB2 As Byte) As Long
Declare Function K_FastInit Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal Channel As Byte,ByRef pRequest As K_MSG,ByRef pResponse  As K_MSG,ByVal InterByteTimeMs As Byte) As Long
Declare Function K_Request Lib "USB2XXX.dll" (ByVal DevHandle As Long, ByVal Channel As Byte,ByRef pRequest As K_MSG,ByRef pResponse  As K_MSG,ByVal InterByteTimeMs As Byte,ByVal ResponseTimeOutMs As Long) As Long


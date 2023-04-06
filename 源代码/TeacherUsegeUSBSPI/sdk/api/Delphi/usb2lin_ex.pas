unit usb2lin_ex;

interface

const
//定义函数返回错误代码
LIN_EX_SUCCESS            = (0);   //函数执行成功
LIN_EX_ERR_NOT_SUPPORT    = (-1);  //适配器不支持该函数
LIN_EX_ERR_USB_WRITE_FAIL = (-2);  //USB写数据失败
LIN_EX_ERR_USB_READ_FAIL  = (-3);  //USB读数据失败
LIN_EX_ERR_CMD_FAIL       = (-4);  //命令执行失败
LIN_EX_ERR_CH_NO_INIT     = (-5);  //该通道未初始化
LIN_EX_ERR_READ_DATA      = (-6);  //LIN读数据失败
LIN_EX_ERR_PARAMETER      = (-7);  //函数参数传入有误
//校验类型
LIN_EX_CHECK_STD    = 0;  //标准校验，不含PID
LIN_EX_CHECK_EXT    = 1;  //增强校验，包含PID
LIN_EX_CHECK_USER   = 2;  //自定义校验类型，需要用户自己计算并传入Check，不进行自动校验
LIN_EX_CHECK_NONE   = 3;  //不计算校验数据
LIN_EX_CHECK_ERROR  = 4;  //接收数据校验错误
//主从机定义
LIN_EX_MASTER       = 1;  //主机
LIN_EX_SLAVE        = 0;  //从机
//帧类型
LIN_EX_MSG_TYPE_UN     = 0;  //未知类型
LIN_EX_MSG_TYPE_MW     = 1;  //主机向从机发送数据
LIN_EX_MSG_TYPE_MR     = 2;  //主机从从机读取数据
LIN_EX_MSG_TYPE_SW     = 3;  //从机发送数据
LIN_EX_MSG_TYPE_SR     = 4;  //从机接收数据
LIN_EX_MSG_TYPE_BK     = 5;  //只发送BREAK信号，若是反馈回来的数据，表明只检测到BREAK信号
LIN_EX_MSG_TYPE_SY     = 6;  //表明检测到了BREAK，SYNC信号
LIN_EX_MSG_TYPE_ID     = 7;  //表明检测到了BREAK，SYNC，PID信号
LIN_EX_MSG_TYPE_DT     = 8;  //表明检测到了BREAK，SYNC，PID,DATA信号
LIN_EX_MSG_TYPE_CK     = 9;  //表明检测到了BREAK，SYNC，PID,DATA,CHECK信号

//定义初始化LIN初始化数据类型
type
PLIN_CONFIG = ^LIN_CONFIG;
LIN_CONFIG = record
  BaudRate:LongWord;      //波特率,最大20K
  CheckMode:Byte;         //校验模式，0-标准校验模式，1-增强校验模式（包含PID）
  MasterMode:Byte;        //主从模式，0-从模式，1-主模式
  BreakBits:Byte;         //Break长度，0x00-10bit,0x20-11bit
end;
//LIN数据收发帧格式定义
type
PLIN_EX_MSG = ^LIN_EX_MSG;
LIN_EX_MSG = record
    Timestamp:LongWord;    //从机接收数据时代表时间戳，单位为0.1ms;主机读写数据时，表示数据读写后的延时时间，单位为ms
    MsgType:Byte;      //帧类型
    CheckType:Byte;    //校验类型
    DataLen:Byte;      //LIN数据段有效数据字节数
    Sync:Byte;         //固定值，0x55
    PID:Byte;          //帧ID
    Data:Array[0..7] Of Byte;      //数据
    Check:Byte;        //校验,只有校验数据类型为LIN_EX_CHECK_USER的时候才需要用户传入数据
    BreakBits:Byte;    //该帧的BRAK信号位数，有效值为10到26，若设置为其他值则默认为13位
    Reserve1:Byte;
end;

//初始化
function LIN_EX_Init(DevHandle:LongWord;LINIndex:Byte;BaudRate:LongWord;MasterMode:Byte):Integer; stdcall;
//主机模式操作函数
function LIN_EX_MasterSync(DevHandle:LongWord;LINIndex:Byte;pInMsg,pOutMsg:PLIN_EX_MSG;MsgLen:LongWord):Integer; stdcall;
function LIN_EX_MasterWrite(DevHandle:LongWord;LINIndex,PID:Byte;pData:PByte;DataLen,CheckType:Byte):Integer; stdcall;
function LIN_EX_MasterRead(DevHandle:LongWord;LINIndex,PID:Byte;pData:PByte):Integer; stdcall;
//从机模式操作函数
function LIN_EX_SlaveSetIDMode(DevHandle:LongWord;LINIndex:Byte;pLINMsg:PLIN_EX_MSG;MsgLen:LongWord):Integer; stdcall;
function LIN_EX_SlaveGetIDMode(DevHandle:LongWord;LINIndex:Byte;pLINMsg:PLIN_EX_MSG):Integer; stdcall;
function LIN_EX_SlaveGetData(DevHandle:LongWord;LINIndex:Byte;pLINMsg:PLIN_EX_MSG):Integer; stdcall;
//电源控制相关函数
function LIN_EX_CtrlPowerOut(DevHandle:LongWord;State:Byte):Integer; stdcall;
function LIN_EX_GetVbatValue(DevHandle:LongWord;pBatValue:PWord):Integer; stdcall;
//主机模式自动发送数据相关函数
function LIN_EX_MasterStartSch(DevHandle:LongWord;LINIndex:Byte;pLINMsg:PLIN_EX_MSG;MsgLen:LongWord):Integer; stdcall;
function LIN_EX_MasterStopSch(DevHandle:LongWord;LINIndex:Byte):Integer; stdcall;
function LIN_EX_MasterGetSch(DevHandle:LongWord;LINIndex:Byte;pLINMsg:PLIN_EX_MSG):Integer; stdcall;

implementation
function LIN_EX_Init;external 'USB2XXX.dll' name 'LIN_EX_Init';
function LIN_EX_MasterSync;external 'USB2XXX.dll' name 'LIN_EX_MasterSync';
function LIN_EX_MasterWrite;external 'USB2XXX.dll' name 'LIN_EX_MasterWrite';
function LIN_EX_MasterRead;external 'USB2XXX.dll' name 'LIN_EX_MasterRead';
function LIN_EX_SlaveSetIDMode;external 'USB2XXX.dll' name 'LIN_EX_SlaveSetIDMode';
function LIN_EX_SlaveGetIDMode;external 'USB2XXX.dll' name 'LIN_EX_SlaveGetIDMode';
function LIN_EX_SlaveGetData;external 'USB2XXX.dll' name 'LIN_EX_SlaveGetData';
function LIN_EX_CtrlPowerOut;external 'USB2XXX.dll' name 'LIN_EX_CtrlPowerOut';
function LIN_EX_GetVbatValue;external 'USB2XXX.dll' name 'LIN_EX_GetVbatValue';
function LIN_EX_MasterStartSch;external 'USB2XXX.dll' name 'LIN_EX_MasterStartSch';
function LIN_EX_MasterStopSch;external 'USB2XXX.dll' name 'LIN_EX_MasterStopSch';
function LIN_EX_MasterGetSch;external 'USB2XXX.dll' name 'LIN_EX_MasterGetSch';
end.

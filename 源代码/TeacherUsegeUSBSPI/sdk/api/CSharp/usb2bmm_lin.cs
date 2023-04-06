using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Runtime.InteropServices;
//注意：使用这些函数需要1.7.4及以上的固件才支持
namespace USB2XXX
{
    class USB2BMM_LIN
    {
        //定义函数返回错误代码
        public const Int32 BMM_LIN_SUCCESS           =  (0);   //函数执行成功
        public const Int32 BMM_LIN_ERR_NOT_SUPPORT   =  (-1);  //适配器不支持该函数
        public const Int32 BMM_LIN_ERR_USB_WRITE_FAIL=  (-2);  //USB写数据失败
        public const Int32 BMM_LIN_ERR_USB_READ_FAIL =  (-3);  //USB读数据失败
        public const Int32 BMM_LIN_ERR_CMD_FAIL      =  (-4);  //命令执行失败
        public const Int32 BMM_LIN_ERR_CH_NO_INIT    =  (-5);  //该通道未初始化
        public const Int32 BMM_LIN_ERR_READ_DATA     =  (-6);  //LIN读数据失败
        public const Int32 BMM_LIN_ERR_PARAMETER     =  (-7);  //函数参数传入有误
        public const Int32 BMM_LIN_ERR_WRITE         =  (-8);  //发送数据出错
        public const Int32 BMM_LIN_ERR_READ          =  (-9);  //读数据出错
        public const Int32 BMM_LIN_ERR_RESP          =  (-10);
        public const Int32 BMM_LIN_ERR_CHECK         =  (-11);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 BMM_LIN_Init(Int32 DevHandle,Byte LINIndex,Int32 BaudRate);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 BMM_LIN_SetPara(Int32 DevHandle, Byte LINIndex, Byte BreakBits, Int32 InterByteSpace, Int32 BreakSpace);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 BMM_LIN_WriteData(Int32 DevHandle,Byte LINIndex,Byte[] pData,Int32 Len);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 BMM_LIN_ReadData(Int32 DevHandle,Byte LINIndex,Byte[] pData);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 BMM_LIN_WaitDataNum(Int32 DevHandle,Byte LINIndex,Int32 DataNum,Int32 TimeOutMs);
    }
}

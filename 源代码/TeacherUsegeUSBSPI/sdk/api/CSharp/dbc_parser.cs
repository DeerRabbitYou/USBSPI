using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Runtime.InteropServices;
using USB2XXX;

namespace USB2XXX
{
    class DBCParser
    {
        public const Int32 DBC_PARSER_OK               =    0;//没有错误
        public const Int32 DBC_PARSER_FILE_OPEN        = (-1);//打开文件出错
        public const Int32 DBC_PARSER_FILE_FORMAT      = (-2);//文件格式错误
        public const Int32 DBC_PARSER_DEV_DISCONNECT   = (-3);//设备未连接
        public const Int32 DBC_PARSER_HANDLE_ERROR     = (-4);//LDF Handle错误
        public const Int32 DBC_PARSER_GET_INFO_ERROR   = (-5);//获取解析后的数据出错
        public const Int32 DBC_PARSER_DATA_ERROR       = (-6);//数据处理错误
        public const Int32 DBC_PARSER_SLAVE_NACK = (-7);//从机未响应数据

        [DllImport("USB2XXX.dll")]
        public static extern UInt64 DBC_ParserFile(int DevHandle, StringBuilder pDBCFileName);
        [DllImport("USB2XXX.dll")]
        public static extern Int32  DBC_GetMsgQuantity(UInt64 DBCHandle);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 DBC_GetMsgName(UInt64 DBCHandle, int index, StringBuilder pMsgName);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 DBC_GetMsgSignalQuantity(UInt64 DBCHandle, StringBuilder pMsgName);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 DBC_GetMsgSignalName(UInt64 DBCHandle, StringBuilder pMsgName, int index, StringBuilder pSignalName);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 DBC_GetMsgPublisher(UInt64 DBCHandle, StringBuilder pMsgName, StringBuilder pPublisher);
        //设置信号值
        [DllImport("USB2XXX.dll")]
        public static extern Int32 DBC_SetSignalValue(UInt64 DBCHandle, StringBuilder pMsgName, StringBuilder pSignalName, double Value);
        //获取信号值
        [DllImport("USB2XXX.dll")]
        public static extern Int32 DBC_GetSignalValue(UInt64 DBCHandle, StringBuilder pMsgName, StringBuilder pSignalName, double[] pValue);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 DBC_GetSignalValueStr(UInt64 DBCHandle, StringBuilder pMsgName, StringBuilder pSignalName, StringBuilder pValueStr);

        //将CAN消息数据填充到信号里面
        [DllImport("USB2XXX.dll")]
        public static extern Int32  DBC_SyncCANMsgToValue(UInt64 DBCHandle, IntPtr pCANMsg,int MsgLen);
        [DllImport("USB2XXX.dll")]
        public static extern Int32  DBC_SyncCANFDMsgToValue(UInt64 DBCHandle, IntPtr pCANFDMsg, int MsgLen);
        //将信号数据填充到CAN消息里面
        [DllImport("USB2XXX.dll")]
        public static extern Int32 DBC_SyncValueToCANMsg(UInt64 DBCHandle, StringBuilder pMsgName, IntPtr pCANMsg);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 DBC_SyncValueToCANFDMsg(UInt64 DBCHandle, StringBuilder pMsgName, IntPtr pCANFDMsg);
    }
}

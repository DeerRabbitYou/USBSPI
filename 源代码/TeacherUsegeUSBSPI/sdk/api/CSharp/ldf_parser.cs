using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Runtime.InteropServices;
using USB2XXX;

namespace USB2XXX
{
    class LDFParser
    {
        public const Int32 LDF_PARSER_OK               =    0;//没有错误
        public const Int32 LDF_PARSER_FILE_OPEN        = (-1);//打开文件出错
        public const Int32 LDF_PARSER_FILE_FORMAT      = (-2);//文件格式错误
        public const Int32 LDF_PARSER_DEV_DISCONNECT   = (-3);//设备未连接
        public const Int32 LDF_PARSER_HANDLE_ERROR     = (-4);//LDF Handle错误
        public const Int32 LDF_PARSER_GET_INFO_ERROR   = (-5);//获取解析后的数据出错
        public const Int32 LDF_PARSER_DATA_ERROR       = (-6);//数据处理错误
        public const Int32 LDF_PARSER_SLAVE_NACK = (-7);//从机未响应数据

        [DllImport("USB2XXX.dll")]
        public static extern UInt64 LDF_ParserFile(int DevHandle, int LINIndex, byte isMaster, byte[] pLDFFileName);
        [DllImport("USB2XXX.dll")]
        public static extern Int32  LDF_GetProtocolVersion(UInt64 LDFHandle);
        [DllImport("USB2XXX.dll")]
        public static extern Int32  LDF_GetLINSpeed(UInt64 LDFHandle);
        [DllImport("USB2XXX.dll")]
        public static extern Int32  LDF_GetFrameQuantity(UInt64 LDFHandle);
        [DllImport("USB2XXX.dll")]
        public static extern Int32  LDF_GetFrameName(UInt64 LDFHandle, int index, byte[] pFrameName);
        [DllImport("USB2XXX.dll")]
        public static extern Int32  LDF_GetFrameSignalQuantity(UInt64 LDFHandle, byte[] pFrameName);
        [DllImport("USB2XXX.dll")]
        public static extern Int32  LDF_GetFrameSignalName(UInt64 LDFHandle, byte[] pFrameName, int index, byte[] pSignalName);
        [DllImport("USB2XXX.dll")]
        public static extern Int32  LDF_SetSignalValue(UInt64 LDFHandle, byte[] pFrameName, byte[] pSignalName, double Value);
        [DllImport("USB2XXX.dll")]
        public static extern Int32  LDF_GetSignalValue(UInt64 LDFHandle, byte[] pFrameName, byte[] pSignalName, double[] pValue);
        [DllImport("USB2XXX.dll")]
        public static extern Int32  LDF_GetSignalValueStr(UInt64 LDFHandle, byte[] pFrameName, byte[] pSignalName, byte[] pValueStr);
        [DllImport("USB2XXX.dll")]
        public static extern Int32  LDF_SetFrameRawValue(UInt64 LDFHandle, byte[] pFrameName, byte[] pRawData);
        [DllImport("USB2XXX.dll")]
        public static extern Int32  LDF_GetFrameRawValue(UInt64 LDFHandle, byte[] pFrameName, byte[] pRawData);
        [DllImport("USB2XXX.dll")]
        public static extern Int32  LDF_GetFramePublisher(UInt64 LDFHandle, byte[] pFrameName, byte[] pPublisher);
        [DllImport("USB2XXX.dll")]
        public static extern Int32  LDF_GetMasterName(UInt64 LDFHandle,  byte[] pMasterName);
        [DllImport("USB2XXX.dll")]
        public static extern Int32  LDF_GetSchQuantity(UInt64 LDFHandle);
        [DllImport("USB2XXX.dll")]
        public static extern Int32  LDF_GetSchName(UInt64 LDFHandle, int index, byte[] pSchName);
        [DllImport("USB2XXX.dll")]
        public static extern Int32  LDF_GetSchFrameQuantity(UInt64 LDFHandle, byte[] pSchName);
        [DllImport("USB2XXX.dll")]
        public static extern Int32  LDF_GetSchFrameName(UInt64 LDFHandle, byte[] pSchName, int index, byte[] pFrameName);
        [DllImport("USB2XXX.dll")]
        public static extern Int32  LDF_ExeFrameToBus(UInt64 LDFHandle, byte[] pFrameName,byte FillBitValue);
        [DllImport("USB2XXX.dll")]
        public static extern Int32  LDF_ExeSchToBus(UInt64 LDFHandle, byte[] pSchName,byte FillBitValue);
    }
}

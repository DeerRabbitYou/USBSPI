using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Runtime.InteropServices;
//注意：使用这些函数需要1.5.30及以上的固件才支持
namespace USB2XXX
{
    class ELMOS_PROGRAMER
    {
        //定义函数返回错误代码
        public const Int32 ELMOS_SUCCESS             = (0);     //函数执行成功
        public const Int32 ELMOS_ERR_OPEN_DEV        = (-1);    //打开设备失败
        public const Int32 ELMOS_ERR_INIT_DEV        = (-2);    //初始化设备失败
        public const Int32 ELMOS_ERR_FILE_FORMAT     = (-3);    //文件格式错误
        public const Int32 ELMOS_ERR_BEGIN_PROG      = (-4);    //进入编程模式错误
        public const Int32 ELMOS_ERR_CMD_FAIL        = (-5);    //命令执行失败
        public const Int32 ELMOS_ERR_PRG_FAILD       = (-6);    //写Flash失败
        public const Int32 ELMOS_ERR_FIND_CHIP       = (-7);    //寻找芯片失败
        [DllImport("USB2XXX.dll")]
        public static extern Int32  ELMOS_StartProg(Int32 DeviceHandle, byte LINChannel,byte[] AppFileName);
         
    }
}

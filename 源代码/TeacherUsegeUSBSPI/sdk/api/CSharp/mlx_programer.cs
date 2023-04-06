using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Runtime.InteropServices;
//注意：使用这些函数需要1.5.30及以上的固件才支持
namespace USB2XXX
{
    class MLX_PROGRAMER
    {
        //定义函数返回错误代码
        public const Int32 MLX_SUCCESS             = (0);     //函数执行成功
        public const Int32 MLX_ERR_OPEN_DEV        = (-1);    //打开设备失败
        public const Int32 MLX_ERR_INIT_DEV        = (-2);    //初始化设备失败
        public const Int32 MLX_ERR_FILE_FORMAT     = (-3);    //文件格式错误
        public const Int32 MLX_ERR_BEGIN_PROG      = (-4);    //进入编程模式错误
        public const Int32 MLX_ERR_CMD_FAIL        = (-5);    //命令执行失败
        public const Int32 MLX_ERR_WRITE_FLASH     = (-6);    //写Flash失败

        //初始化
        [DllImport("USB2XXX.dll")]
        public static extern Int32  MLX_ProgInit(Int32 DevHandle,Byte LINIndex,Byte BaudRateOfKbps,Byte UseFastLIN);
        //主机模式操作函数
        [DllImport("USB2XXX.dll")]
        public static extern Int32 MLX_ProgNVRAM(Int32 DevHandle, Byte LINIndex, Byte[] nvramFileName, Byte nad);
        [DllImport("USB2XXX.dll")]
        public static extern Int32 MLX_ProgFlash(Int32 DevHandle, Byte LINIndex,Byte[] LoaderFileName,Byte[] AppFileName,Byte nad);
         
    }
}

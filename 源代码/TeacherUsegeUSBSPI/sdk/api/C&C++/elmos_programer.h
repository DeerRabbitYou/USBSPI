/**
  ******************************************************************************
  * @file    elmos_programer.h
  * $Author: wdluo $
  * $Revision: 447 $
  * $Date:: 2013-06-29 18:24:57 +0800 #$
  * @brief   elmos_programer相关函数和数据类型定义.
  ******************************************************************************
  * @attention
  *
  *<center><a href="http:\\www.toomoss.com">http://www.toomoss.com</a></center>
  *<center>All Rights Reserved</center></h3>
  * 
  ******************************************************************************
  */
#ifndef __ELMOS_PROGRAMER_H_
#define __ELMOS_PROGRAMER_H_

#include <stdint.h>
#ifndef OS_UNIX
#include <Windows.h>
#else
#include <unistd.h>
#ifndef WINAPI
#define WINAPI
#endif
#endif
//定义函数返回错误代码
#define ELMOS_SUCCESS             (0)     //函数执行成功
#define ELMOS_ERR_OPEN_DEV        (-1)    //打开设备失败
#define ELMOS_ERR_INIT_DEV        (-2)    //初始化设备失败
#define ELMOS_ERR_FILE_FORMAT     (-3)    //文件格式错误
#define ELMOS_ERR_BEGIN_PROG      (-4)    //进入编程模式错误
#define ELMOS_ERR_CMD_FAIL        (-5)    //命令执行失败
#define ELMOS_ERR_PRG_FAILD       (-6)    //编程失败
#define ELMOS_ERR_FIND_CHIP       (-7)    //寻找芯片失败

#ifdef __cplusplus
extern "C"
{
#endif

    int WINAPI ELMOS_StartProg(int DeviceHandle, unsigned char LINChannel,const char* AppFileName);

#ifdef __cplusplus
}
#endif


#endif


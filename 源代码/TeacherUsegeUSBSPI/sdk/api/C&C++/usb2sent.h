/**
  ******************************************************************************
  * @file    usb2sent.h
  * $Author: wdluo $
  * $Revision: 447 $
  * $Date:: 2013-06-29 18:24:57 +0800 #$
  * @brief   usb2sent相关函数和数据类型定义.
  ******************************************************************************
  * @attention
  *
  *<center><a href="http:\\www.toomoss.com">http://www.toomoss.com</a></center>
  *<center>All Rights Reserved</center></h3>
  * 
  ******************************************************************************
  */
#ifndef __USB2SENT_H_
#define __USB2SENT_H_

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
#define SENT_SUCCESS             (0)   //函数执行成功
#define SENT_ERR_NOT_SUPPORT     (-1)  //适配器不支持该函数
#define SENT_ERR_USB_WRITE_FAIL  (-2)  //USB写数据失败
#define SENT_ERR_USB_READ_FAIL   (-3)  //USB读数据失败
#define SENT_ERR_CMD_FAIL        (-4)  //命令执行失败
#define SENT_ERR_PARAMETER       (-7)  //函数参数传入有误

#ifdef __cplusplus
extern "C"
{
#endif
//初始化
int WINAPI  SENT_Init(int DevHandle,unsigned char Channel,unsigned char TicksTimeUs,unsigned char MasterMode);
int WINAPI  SENT_SendData(int DevHandle,unsigned char Channel,unsigned char Status,unsigned char SendPause,unsigned char *pHalfByteData,unsigned char DataNum);
#ifdef __cplusplus
}
#endif

#endif

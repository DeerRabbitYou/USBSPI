/**
  ******************************************************************************
  * @file    usb2lin_ex.h
  * $Author: wdluo $
  * $Revision: 447 $
  * $Date:: 2013-06-29 18:24:57 +0800 #$
  * @brief   usb2lin_ex相关函数和数据类型定义.
  ******************************************************************************
  * @attention
  *
  *<center><a href="http:\\www.toomoss.com">http://www.toomoss.com</a></center>
  *<center>All Rights Reserved</center></h3>
  * 
  ******************************************************************************
  */
#ifndef __USB2BMM_LIN_H_
#define __USB2BMM_LIN_H_

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
#define BMM_LIN_SUCCESS             (0)   //函数执行成功
#define BMM_LIN_ERR_NOT_SUPPORT     (-1)  //适配器不支持该函数
#define BMM_LIN_ERR_USB_WRITE_FAIL  (-2)  //USB写数据失败
#define BMM_LIN_ERR_USB_READ_FAIL   (-3)  //USB读数据失败
#define BMM_LIN_ERR_CMD_FAIL        (-4)  //命令执行失败
#define BMM_LIN_ERR_CH_NO_INIT      (-5)  //该通道未初始化
#define BMM_LIN_ERR_READ_DATA       (-6)  //LIN读数据失败
#define BMM_LIN_ERR_PARAMETER       (-7)  //函数参数传入有误
#define BMM_LIN_ERR_WRITE           (-8)  //发送数据出错
#define BMM_LIN_ERR_READ            (-9)  //读数据出错
#define BMM_LIN_ERR_RESP            (-10)
#define BMM_LIN_ERR_CHECK           (-11)
#ifdef __cplusplus
extern "C"
{
#endif

    int WINAPI BMM_LIN_Init(int DevHandle,unsigned char LINIndex,int BaudRate);
    int WINAPI BMM_LIN_SetPara(int DevHandle, unsigned char LINIndex, unsigned char BreakBits, int  InterByteSpace, int  BreakSpace);
    int WINAPI BMM_LIN_WriteData(int DevHandle,unsigned char LINIndex,unsigned char *pData,unsigned int Len);
    int WINAPI BMM_LIN_ReadData(int DevHandle,unsigned char LINIndex,unsigned char *pData);
    int WINAPI BMM_LIN_WaitDataNum(int DevHandle,unsigned char LINIndex,unsigned int DataNum,int TimeOutMs);

#ifdef __cplusplus
}
#endif


#endif


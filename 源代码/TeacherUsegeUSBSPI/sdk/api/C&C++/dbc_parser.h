/*******************************************************************************
  * @file    dbc_parser.h
  * $Author: wdluo $
  * $Revision: 447 $
  * $Date:: 2022-03-30 18:24:57 +0800 #$
  * @brief   DBC文件解析相关函数和数据类型定义.
  ******************************************************************************
  * @attention
  *
  *<center><a href="http:\\www.toomoss.com">http://www.toomoss.com</a></center>
  *<center>All Rights Reserved</center></h3>
  *
  ******************************************************************************
  */
#ifndef __DBC_PARSER_H_
#define __DBC_PARSER_H_

#include <stdint.h>
#ifndef OS_UNIX
#include <Windows.h>
#else
#include <unistd.h>
#ifndef WINAPI
#define WINAPI
#endif
#endif

#define DBC_PARSER_OK                   0//没有错误
#define DBC_PARSER_FILE_OPEN         (-1)//打开文件出错
#define DBC_PARSER_FILE_FORMAT       (-2)//文件格式错误
#define DBC_PARSER_DEV_DISCONNECT    (-3)//设备未连接
#define DBC_PARSER_HANDLE_ERROR      (-4)//DBC Handle错误
#define DBC_PARSER_GET_INFO_ERROR    (-5)//获取解析后的数据出错
#define DBC_PARSER_DATA_ERROR        (-6)//数据处理错误
#define DBC_PARSER_SLAVE_NACK        (-7)//从机未响应数据

#ifdef __cplusplus
extern "C"
{
#endif
    long long WINAPI DBC_ParserFile(int DevHandle, char* pDBCFileName);
    int WINAPI DBC_GetMsgQuantity(long long DBCHandle);
    int WINAPI DBC_GetMsgName(long long DBCHandle, int index, char* pMsgName);
    int WINAPI DBC_GetMsgSignalQuantity(long long DBCHandle, char* pMsgName);
    int WINAPI DBC_GetMsgSignalName(long long DBCHandle, char* pMsgName, int index, char* pSignalName);
    int WINAPI DBC_GetMsgPublisher(long long DBCHandle, char* pMsgName, char* pPublisher);
    //设置信号值
    int WINAPI DBC_SetSignalValue(long long DBCHandle, char* pMsgName, char* pSignalName, double Value);
    //获取信号值
    int WINAPI DBC_GetSignalValue(long long DBCHandle, char* pMsgName, char* pSignalName, double* pValue);
    int WINAPI DBC_GetSignalValueStr(long long DBCHandle, char* pMsgName, char* pSignalName, char* pValueStr);
    //将CAN消息数据填充到信号里面
    int WINAPI DBC_SyncCANMsgToValue(long long DBCHandle, void* pCANMsg,int MsgLen);
    int WINAPI DBC_SyncCANFDMsgToValue(long long DBCHandle, void* pCANFDMsg, int MsgLen);
    //将信号数据填充到CAN消息里面
    int WINAPI DBC_SyncValueToCANMsg(long long DBCHandle, char* pMsgName, void* pCANMsg);
    int WINAPI DBC_SyncValueToCANFDMsg(long long DBCHandle, char* pMsgName, void* pCANFDMsg);
#ifdef __cplusplus
}
#endif

#endif



/**
  ******************************************************************************
  * @file    hexfile_decode.h
  * $Author: wdluo $
  * $Revision: 447 $
  * $Date:: 2013-06-29 18:24:57 +0800 #$
  * @brief   HEX,S19文件解码相关函数和数据类型定义.
  ******************************************************************************
  * @attention
  *
  *<center><a href="http:\\www.toomoss.com">http://www.toomoss.com</a></center>
  *<center>All Rights Reserved</center></h3>
  * 
  ******************************************************************************
  */
#ifndef __HEXFILE_DECODE_H_
#define __HEXFILE_DECODE_H_

#include <stdint.h>
#ifndef OS_UNIX
#include <Windows.h>
#else
#include <unistd.h>
#ifndef WINAPI
#define WINAPI
#endif
#endif

//文件数据块定义
typedef struct _HEX_FILE_BLOCK
{
    unsigned int  StartAddr;//数据块起始地址
    unsigned int  DataNum;  //数据块字节数
    unsigned char *pData;   //数据块数据存储指针
}HEX_FILE_BLOCK,*PHEX_FILE_BLOCK;

//存储器类型
#define MEMTYPE_UINT8    1  //1个地址单元存储1字节数据
#define MEMTYPE_UINT16   2  //1个地址单元存储2字节数据
#define MEMTYPE_UINT32   4  //1个地址单元存储4字节数据

#ifdef __cplusplus
extern "C"
{
#endif
    int WINAPI hexfile_load_file(const char *filename, char *fileBuf);
    int WINAPI hexfile_convert_s19(char *fileBuf, int lenFileBuf, HEX_FILE_BLOCK *pHexFileBlock, int maxBlockNum, char memType);
    int WINAPI hexfile_convert_ihx(char *fileBuf, int lenFileBuf, HEX_FILE_BLOCK *pHexFileBlock, int maxBlockNum, char memType);
    int WINAPI hexfile_convert_txt(char *fileBuf, int lenFileBuf, HEX_FILE_BLOCK *pHexFileBlock, int maxBlockNum, char memType);
    int WINAPI hexfile_free_data(HEX_FILE_BLOCK *pHexFileBlock, int maxBlockNum);
    int WINAPI hexfile_save_image(const char *filename,HEX_FILE_BLOCK *pHexFileBlock, int maxBlockNum, char memType,char fillBytes);
    int WINAPI hexfile_convert_image(char *pOutData,HEX_FILE_BLOCK *pHexFileBlock, int maxBlockNum, char memType,char fillBytes);
#ifdef __cplusplus
}
#endif

#endif

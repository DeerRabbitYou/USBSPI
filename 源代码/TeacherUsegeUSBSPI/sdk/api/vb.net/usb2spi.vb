Imports System.Runtime.InteropServices
Module usb2spi
    '定义SPI通道
    Public Const SPI1        As Byte =(&H00)
    Public Const SPI1_CS0    As Byte =(&H00)
    Public Const SPI1_CS1    As Byte =(&H10)
    Public Const SPI1_CS2    As Byte =(&H20)
    Public Const SPI1_CS3    As Byte =(&H30)
    Public Const SPI1_CS4    As Byte =(&H40)

    Public Const SPI2        As Byte =(&H01)
    Public Const SPI2_CS0    As Byte =(&H01)
    Public Const SPI2_CS1    As Byte =(&H11)
    Public Const SPI2_CS2    As Byte =(&H21)
    Public Const SPI2_CS3    As Byte =(&H31)
    Public Const SPI2_CS4    As Byte =(&H41)
    '定义工作模式
    Public Const SPI_MODE_HARD_FDX       As Byte =0 '硬件控制（全双工模式）
    Public Const SPI_MODE_HARD_HDX       As Byte =1 '硬件控制（半双工模式）
    Public Const SPI_MODE_SOFT_HDX       As Byte =2 '软件控制（半双工模式）
    Public Const SPI_MODE_SOFT_ONE_WIRE  As Byte =3 '单总线模式，数据线输入输出都为MOSI
    Public Const SPI_MODE_SOFT_FDX       As Byte =4 '软件控制（全双工模式）
    '定义主从机模式
    Public Const SPI_MASTER      As Byte =1 '主机
    Public Const SPI_SLAVE       As Byte =0 '从机
    '定义数据移位方式
    Public Const SPI_MSB         As Byte =0 '高位在前
    Public Const SPI_LSB         As Byte =1 '低位在前
    '定义片选输出极性
    Public Const SPI_SEL_LOW     As Byte =0 '片选输出低电平
    Public Const SPI_SEL_HIGH    As Byte =1 '片选输出高电平

    '定义EVENT引脚,注意EVENT引脚不要跟SPI通信引脚冲突
    Public Const SPI_EVENT_P0   As UInt16 =(&H0001)
    Public Const SPI_EVENT_P1   As UInt16 =(&H0002)
    Public Const SPI_EVENT_P2   As UInt16 =(&H0004)
    Public Const SPI_EVENT_P3   As UInt16 =(&H0008)
    Public Const SPI_EVENT_P4   As UInt16 =(&H0010)
    Public Const SPI_EVENT_P5   As UInt16 =(&H0020)
    Public Const SPI_EVENT_P6   As UInt16 =(&H0040)
    Public Const SPI_EVENT_P7   As UInt16 =(&H0080)
    Public Const SPI_EVENT_P8   As UInt16 =(&H0100)
    Public Const SPI_EVENT_P9   As UInt16 =(&H0200)
    Public Const SPI_EVENT_P10  As UInt16 =(&H0400)
    Public Const SPI_EVENT_P11  As UInt16 =(&H0800)
    Public Const SPI_EVENT_P12  As UInt16 =(&H1000)
    Public Const SPI_EVENT_P13  As UInt16 =(&H2000)
    Public Const SPI_EVENT_P14  As UInt16 =(&H4000)
    Public Const SPI_EVENT_P15  As UInt16 =(&H8000)

    '定义事件类型
    Public Const EVENT_TYPE_LOW     As Byte =&H00
    Public Const EVENT_TYPE_HIGH    As Byte =&H11
    Public Const EVENT_TYPE_RISING  As Byte =&H01
    Public Const EVENT_TYPE_FALLING As Byte =&H10

    '定义从机模式下连续读取数据的回调函数
    Public Delegate Function PSPI_GET_DATA_HANDLE(ByVal DevHandle As UInt32,ByVal SPIIndex As UInt32, <Out()> ByVal pData As Byte(),ByVal DataNum As UInt32) As Int32

    '定义初始化SPI的数据类型
    Public Structure SPI_CONFIG
        Dim   Mode As Byte              'SPI控制方式:0-硬件控制（全双工模式）,1-硬件控制（半双工模式），2-软件控制（半双工模式）,3-单总线模式，数据线输入输出都为MOSI,4-软件控制（全双工模式）
        Dim   Master As Byte            '主从选择控制:0-从机，1-主机
        Dim   CPOL As Byte              '时钟极性控制:0-SCK空闲时为低电平，1-SCK空闲时为高电平
        Dim   CPHA As Byte              '时钟相位控制:0-第一个SCK时钟采样，1-第二个SCK时钟采样
        Dim   LSBFirst As Byte          '数据移位方式:0-MSB在前，1-LSB在前
        Dim   SelPolarity As Byte       '片选信号极性:0-低电平选中，1-高电平选中
        Dim   ClockSpeedHz As UInt32    'SPI时钟频率:单位为HZ，硬件模式下最大50000000，最小390625，频率按2的倍数改变
    End Structure

    '定义SPI Flash器件配置参数数据类型
    Public Structure SPI_FLASH_CONFIG
        Dim CMD_WriteEnable As Byte          '使能写命令
        Dim CMD_WriteDisable As Byte         '禁止写命令
        Dim CMD_WritePage As Byte            '写数据命令
        Dim WritePageAddressBytes As Byte    '写数据时的地址宽度，单位为字节
        Dim CMD_EraseSector As Byte          '扇区擦出命令
        Dim EraseSectorAddressBytes As Byte  '扇区擦出的地址宽度，单位为字节
        Dim CMD_EraseBulk As Byte            '块擦出命令
        Dim CMD_EraseChip As Byte            '整片擦出命令
        Dim CMD_ReadID As Byte               '读芯片ID命令
        Dim CMD_ReadData As Byte             '读数据命令
        Dim ReadDataAddressBytes As Byte     '读数据时的地址宽度，单位为字节
        Dim CMD_ReadFast As Byte             '快速模式读数据命令
        Dim ReadFastAddressBytes As Byte     '快速读数据时的地址宽度，单位为字节
        Dim CMD_ReadStatus As Byte           '读取状态寄存器命令
        Dim CMD_WriteStatus As Byte          '写状态寄存器命令
        <MarshalAs(UnmanagedType.ByValArray, SizeConst:=16)> _
        Dim ID As Byte()                   '芯片ID存储数组
        Dim ID_Length As Byte                'ID长度，单位为字节
        Dim PageSize As Int32                           '页大小，单位为字节
        Dim NumPages As Int32                           '芯片总的页数
        Dim SectorSize As Int32                         '扇区大小，单位为字节
    End Structure

    '定义函数返回错误代码
    Public Const SPI_SUCCESS            As Int32 = (0)   '函数执行成功
    Public Const SPI_ERR_NOT_SUPPORT    As Int32 = (-1)  '适配器不支持该函数
    Public Const SPI_ERR_USB_WRITE_FAIL As Int32 = (-2)  'USB写数据失败
    Public Const SPI_ERR_USB_READ_FAIL  As Int32 = (-3)  'USB读数据失败
    Public Const SPI_ERR_CMD_FAIL       As Int32 = (-4)  '命令执行失败
    Public Const SPI_ERR_PARAMETER      As Int32 = (-5)  '参数错误
    Public Const SPI_ERR_EVENT_TIMEOUT  As Int32 = (-6)  '检测Event超时


    Declare Function SPI_Init Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32, ByRef pConfig As SPI_CONFIG) As Int32
    Declare Function SPI_WriteBytes Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[In]()> ByVal pWriteData As Byte(),ByVal WriteLen As Int32) As Int32
    Declare Function SPI_WriteBytesAsync Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[In]()> ByVal pWriteData As Byte(),ByVal WriteLen As Int32) As Int32
    Declare Function SPI_ReadBytes Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[Out]()> ByVal pReadData As Byte(),ByVal ReadLen As Int32) As Int32
    Declare Function SPI_WriteReadBytes Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[In]()> ByVal pWriteData As Byte(),ByVal WriteLen As Int32,<[Out]()> ByVal pReadData As Byte(),ByVal ReadLen As Int32,ByVal IntervalTimeUs As Int32) As Int32
    Declare Function SPI_WriteBytesOfEvent Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[In]()> ByVal pWriteData As Byte(),ByVal WriteLen As Int32,ByVal EventPin As Int32,ByVal EventType As Byte,ByVal TimeOutOfMs As Int32) As Int32
    Declare Function SPI_ReadBytesOfEvent Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[Out]()> ByVal pReadData As Byte(),ByVal ReadLen As Int32,ByVal EventPin As Int32,ByVal EventType As Byte,ByVal TimeOutOfMs As Int32) As Int32
    Declare Function SPI_WriteReadBytesOfEvent Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[In]()> ByVal pWriteData As Byte(),ByVal WriteLen As Int32,<[Out]()> ByVal pReadData As Byte(),ByVal ReadLen As Int32,ByVal IntervalTimeUs As Int32,ByVal EventPin As Int32,ByVal EventType As Byte,ByVal TimeOutOfMs As Int32) As Int32
    Declare Function SPI_WriteBits Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[Out]()> ByVal pWriteBitStr As Byte()) As Int32
    Declare Function SPI_ReadBits Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[Out]()> ByVal pReadBitStr As Byte(),ByVal ReadBitsNum As Int32) As Int32
    Declare Function SPI_WriteReadBits Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[Out]()> ByVal pWriteBitStr As Byte(),<[Out]()> ByVal pReadBitStr As Byte(),ByVal ReadBitsNum As Int32) As Int32
    Declare Function SPI_SlaveWriteBytes Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[In]()> ByVal pWriteData As Byte(),ByVal WriteLen As Int32,ByVal TimeOutMs As Int32) As Int32
    Declare Function SPI_SlaveReadBytes Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[Out]()> ByVal pReadData As Byte(),ByVal ReadLen As Int32,ByVal TimeOutMs As Int32) As Int32
    Declare Function SPI_SlaveReadWriteBytes Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[Out]()> ByVal pReadData As Byte(),ByVal ReadDataLen As Int32,<[In]()> ByVal pWriteData As Byte(),ByVal WriteDataLen As Int32,ByVal TimeOutMs As Int32) As Int32
    Declare Function SPI_SlaveWriteReadBytes Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[In]()> ByVal pWriteData As Byte(),ByVal WriteDataLen As Int32,<[Out]()> ByVal pReadData As Byte(),ByVal ReadDataLen As Int32,ByVal TimeOutMs As Int32) As Int32
    Declare Function SPI_SlaveContinueRead Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32, ByRef pSlaveReadDataHandle As SPI_GET_DATA_HANDLE) As Int32
    Declare Function SPI_SlaveGetBytes Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[Out]()> ByVal pReadData As Byte(),ByVal TimeOutOfMs As Int32) As Int32
    Declare Function SPI_SlaveContinueWriteReadStop Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32) As Int32
    Declare Function SPI_SlaveContinueWrite Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[In]()> ByVal pWriteData As Byte(),ByVal WriteLen As Int32) As Int32
    Declare Function SPI_FlashInit Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,ByVal ClockSpeed As Int32,ByRef pConfig As SPI_FLASH_CONFIG) As Int32
    Declare Function SPI_FlashReadID Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[Out]()> ByVal pIDAs Byte()) As Int32
    Declare Function SPI_FlashEraseSector Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,ByVal StartSector As Int32,ByVal NumSector As Int32,ByVal TimeOutMs As Int32) As Int32
    Declare Function SPI_FlashEraseChip Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,ByVal TimeOutMs As Int32) As Int32
    Declare Function SPI_FlashErase Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,ByVal StartAddr As Int32,ByVal AddrBytes As Byte,ByVal EraseCmd As Byte,ByVal TimeOutMs As Int32) As Int32
    Declare Function SPI_FlashWrite Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,ByVal StartAddr As Int32,<[In]()> ByVal pWriteData As Byte(),ByVal WriteLen As Int32) As Int32
    Declare Function SPI_FlashRead Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,ByVal StartAddr As Int32,<[Out]()> ByVal pReadData As Byte(),ByVal ReadLen As Int32) As Int32
    Declare Function SPI_FlashReadFast Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,ByVal StartAddr As Int32,<[Out]()> ByVal pReadData As Byte(),ByVal ReadLen As Int32) As Int32
    Declare Function SPI_BlockWriteBytes Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[In]()> ByVal pWriteData As Byte(),ByVal BlockSize As Int32,ByVal BlockNum As Int32,ByVal IntervalTimeUs As Int32) As Int32
    Declare Function SPI_BlockReadBytes Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[Out]()> ByVal pReadData As Byte(),ByVal BlockSize As Int32,ByVal BlockNum As Int32,ByVal IntervalTimeUs As Int32) As Int32
    Declare Function SPI_BlockWriteReadBytes Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[In]()> ByVal pWriteData As Byte(),ByVal WriteBlockSize As Int32,<[Out]()> ByVal pReadData As Byte(),ByVal ReadBlockSize As Int32,ByVal BlockNum As Int32,ByVal IntervalTimeUs As Int32) As Int32
    Declare Function SPI_BlockWriteBytesOfEvent Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[In]()> ByVal pWriteData As Byte(),ByVal BlockSize As Int32,ByVal BlockNum As Int32,ByVal EventPin As Int32,ByVal EventType As Byte,ByVal TimeOutOfMs As Int32) As Int32
    Declare Function SPI_BlockReadBytesOfEvent Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[Out]()> ByVal pReadData As Byte(),ByVal BlockSize As Int32,ByVal BlockNum As Int32,ByVal EventPin As Int32,ByVal EventType As Byte,ByVal TimeOutOfMs As Int32) As Int32
    Declare Function SPI_BlockWriteReadBytesOfEvent Lib "USB2XXX.dll" (ByVal DevHandle As UInt32,ByVal SPIIndex As Int32,<[In]()> ByVal pWriteData As Byte(),ByVal WriteBlockSize As Int32,<[Out]()> ByVal pReadData As Byte(),ByVal ReadBlockSize As Int32,ByVal BlockNum As Int32,ByVal EventPin As Int32,ByVal EventType As Byte,ByVal TimeOutOfMs As Int32) As Int32


End Module

package com.toomoss.USB2XXX;

import java.util.Arrays;
import java.util.List;

import com.sun.jna.Library;
import com.sun.jna.Native;
import com.sun.jna.Structure;

public interface USB2CANFD extends Library {
	USB2CANFD INSTANCE  = (USB2CANFD)Native.loadLibrary("USB2XXX",USB2CANFD.class); 
	
	//函数返回值错误信息定义
	public static int CANFD_SUCCESS            = (0);   //函数执行成功
	public static int CANFD_ERR_NOT_SUPPORT    = (-1);  //适配器不支持该函数
	public static int CANFD_ERR_USB_WRITE_FAIL = (-2);  //USB写数据失败
	public static int CANFD_ERR_USB_READ_FAIL  = (-3);  //USB读数据失败
	public static int CANFD_ERR_CMD_FAIL       = (-4);  //命令执行失败
	//CANFD_MSG.ID定义
	public static int CANFD_MSG_FLAG_RTR     = (0x40000000);
	public static int CANFD_MSG_FLAG_IDE     = (0x80000000);
	public static int CANFD_MSG_FLAG_ID_MASK = (0x1FFFFFFF);
	//CANFD_MSG.Flags定义
	public static byte CANFD_MSG_FLAG_BRS     = (0x01);  //CANFD加速帧标志
	public static byte CANFD_MSG_FLAG_ESI     = (0x02);
	public static byte CANFD_MSG_FLAG_FDF     = (0x04);  //CANFD帧标志
	public static byte CANFD_MSG_FLAG_TXD     = (0x80);
	//CANFD_DIAGNOSTIC.Flags定义
	public static int CANFD_DIAGNOSTIC_FLAG_NBIT0_ERR    = (0x0001);//在发送报文（或应答位、主动错误标志或过载标志）期间，器件要发送显性电平（逻辑值为0的数据或标识符位），但监视的总线值为隐性。
	public static int CANFD_DIAGNOSTIC_FLAG_NBIT1_ERR    = (0x0002);//在发送报文（仲裁字段除外）期间，器件要发送隐性电平（逻辑值为1的位），但监视到的总线值为显性。
	public static int CANFD_DIAGNOSTIC_FLAG_NACK_ERR     = (0x0004);//发送报文未应答。
	public static int CANFD_DIAGNOSTIC_FLAG_NFORM_ERR    = (0x0008);//接收报文的固定格式部分格式错误。
	public static int CANFD_DIAGNOSTIC_FLAG_NSTUFF_ERR   = (0x0010);//在接收报文的一部分中，序列中包含了5个以上相等位，而报文中不允许出现这种序列。
	public static int CANFD_DIAGNOSTIC_FLAG_NCRC_ERR     = (0x0020);//接收的报文的CRC校验和不正确。输入报文的CRC与通过接收到的数据计算得到的CRC不匹配。
	public static int CANFD_DIAGNOSTIC_FLAG_TXBO_ERR     = (0x0080);//器件进入离线状态（且自动恢复）。
	public static int CANFD_DIAGNOSTIC_FLAG_DBIT0_ERR    = (0x0100);//见NBIT0_ERR
	public static int CANFD_DIAGNOSTIC_FLAG_DBIT1_ERR    = (0x0200);//见NBIT1_ERR
	public static int CANFD_DIAGNOSTIC_FLAG_DFORM_ERR    = (0x0800);//见NFORM_ERR
	public static int CANFD_DIAGNOSTIC_FLAG_DSTUFF_ERR   = (0x1000);//见NSTUFF_ERR
	public static int CANFD_DIAGNOSTIC_FLAG_DCRC_ERR     = (0x2000);//见NCRC_ERR
	public static int CANFD_DIAGNOSTIC_FLAG_ESI_ERR      = (0x4000);//接收的CAN FD报文的ESI标志置1
	public static int CANFD_DIAGNOSTIC_FLAG_DLC_MISMATCH = (0x8000);//DLC不匹配,在发送或接收期间，指定的DLC大于FIFO元素的PLSIZE
	//CANFD_BUS_ERROR.Flags定义
	public static byte CANFD_BUS_ERROR_FLAG_TX_RX_WARNING  = (0x01);
	public static byte CANFD_BUS_ERROR_FLAG_RX_WARNING     = (0x02);
	public static byte CANFD_BUS_ERROR_FLAG_TX_WARNING     = (0x04);
	public static byte CANFD_BUS_ERROR_FLAG_RX_BUS_PASSIVE = (0x08);
	public static byte CANFD_BUS_ERROR_FLAG_TX_BUS_PASSIVE = (0x10);
	public static byte CANFD_BUS_ERROR_FLAG_TX_BUS_OFF     = (0x20);

	//1.CANFD信息帧的数据类型定义
	public class CANFD_MSG  extends Structure
	{
		public static class ByReference extends CANFD_MSG implements Structure.ByReference {}  
		public static class ByValue extends CANFD_MSG implements Structure.ByValue {}

		@Override
		protected List getFieldOrder() {
			// TODO Auto-generated method stub
			return Arrays.asList(new String[]{"ID","DLC","Flags","__Res0","TimeStampHigh","TimeStamp","Data"});
		}
		public int    ID;           //报文ID,bit[30]-RTR,bit[31]-IDE,bit[28..0]-ID
		public byte   DLC;          //数据字节长度，可设置为-0,1,2,3,4,5,6,7,8,12,16,20,24,32,48,64
		public byte   Flags;        //bit[0]-BRS,bit[1]-ESI,bit[2]-FDF,bit[6..5]-通道号,bit[7]-发送标志
		public byte   __Res0;       //保留
		public byte   TimeStampHigh;//时间戳高位
		public int    TimeStamp;    //帧接收或者发送时的时间戳，单位为10us
		public byte[]	Data = new byte[64];     //报文的数据。
	}

	//2.CANFD初始化配置数据类型定义
	public class CANFD_INIT_CONFIG  extends Structure
	{
		public static class ByReference extends CANFD_INIT_CONFIG implements Structure.ByReference {}  
		public static class ByValue extends CANFD_INIT_CONFIG implements Structure.ByValue {}

		@Override
		protected List getFieldOrder() {
			// TODO Auto-generated method stub
			return Arrays.asList(new String[]{"Mode","ISOCRCEnable","RetrySend","ResEnable","NBT_BRP","NBT_SEG1","NBT_SEG2","NBT_SJW","DBT_BRP","DBT_SEG1","DBT_SEG2","DBT_SJW","__Res0"});
		}
		public byte Mode; //0-正常模式，1-自发自收模式
		public byte ISOCRCEnable;//0-禁止ISO CRC,1-使能ISO CRC
		public byte RetrySend;//0-禁止重发，1-无限制重发
		public byte ResEnable;//0-不接入内部120欧终端电阻，1-接入内部120欧终端电阻
		//波特率参数可以用TCANLINPro软件里面的波特率计算工具计算
		//仲裁段波特率参数,波特率=40M/NBT_BRP*(1+NBT_SEG1+NBT_SEG2)
		public byte NBT_BRP;
		public byte NBT_SEG1;
		public byte NBT_SEG2;
		public byte NBT_SJW;
		//数据段波特率参数,波特率=40M/DBT_BRP*(1+DBT_SEG1+DBT_SEG2)
		public byte DBT_BRP;
		public byte DBT_SEG1;
		public byte DBT_SEG2;
		public byte DBT_SJW;
		public byte[]	__Res0 = new byte[8];
	}

	//3.CANFD诊断帧信息结构体定义
	public class CANFD_DIAGNOSTIC  extends Structure {
		public static class ByReference extends CANFD_DIAGNOSTIC implements Structure.ByReference {}  
		public static class ByValue extends CANFD_DIAGNOSTIC implements Structure.ByValue {}

		@Override
		protected List getFieldOrder() {
			// TODO Auto-generated method stub
			return Arrays.asList(new String[]{"NREC","NTEC","DREC","DTEC","ErrorFreeMsgCount","Flags"});
		}
		public byte NREC;//标称比特率接收错误计数
		public byte NTEC;//标称比特率发送错误计数
		public byte DREC;//数据比特率接收错误计数
		public byte DTEC;//数据比特率发送错误计数
		public short ErrorFreeMsgCount;//无错误帧计数
		public short Flags;//参考诊断标志定义
	}
	//4.CANFD总线错误信息结构体定义
	public class CANFD_BUS_ERROR  extends Structure {
		public static class ByReference extends CANFD_BUS_ERROR implements Structure.ByReference {}  
		public static class ByValue extends CANFD_BUS_ERROR implements Structure.ByValue {}

		@Override
		protected List getFieldOrder() {
			// TODO Auto-generated method stub
			return Arrays.asList(new String[]{"TEC","REC","Flags","__Res0"});
		}
		public byte TEC;//发送错误计数
		public byte REC;//接收错误计数
		public byte Flags;//参考总线错误标志定义
		public byte __Res0;
	}
	//5.CAN 滤波器设置数据类型定义
	public class CANFD_FILTER_CONFIG  extends Structure {
		public static class ByReference extends CANFD_FILTER_CONFIG implements Structure.ByReference {}  
		public static class ByValue extends CANFD_FILTER_CONFIG implements Structure.ByValue {}

		@Override
		protected List getFieldOrder() {
			// TODO Auto-generated method stub
			return Arrays.asList(new String[]{"Enable","Index","__Res0","__Res1","ID_Accept","ID_Mask"});
		}
		public byte   Enable;   //使能该过滤器，1-使能，0-禁止
		public byte   Index;    //过滤器索引号，取值范围为0到31
		public byte __Res0;
		public byte __Res1;
		public int    ID_Accept;//验收码ID,bit[28..0]为有效ID位，bit[31]为IDE
		public int    ID_Mask;  //屏蔽码，对应bit位若为1，则需要对比对应验收码bit位，相同才接收
	}

	//USB2CANFD函数定义
	int  CANFD_Init(int DevHandle, byte CANIndex, CANFD_INIT_CONFIG pCanConfig);
	int  CANFD_StartGetMsg(int DevHandle, byte CANIndex);
	int  CANFD_StopGetMsg(int DevHandle, byte CANIndex);
	int  CANFD_SendMsg(int DevHandle, byte CANIndex, CANFD_MSG[] pCanSendMsg,int SendMsgNum);
	int  CANFD_GetMsg(int DevHandle, byte CANIndex, CANFD_MSG[] pCanGetMsg,int BufferSize);
	int  CANFD_ClearMsg(int DevHandle, byte CANIndex);
	int  CANFD_SetFilter(int DevHandle, byte CANIndex, CANFD_FILTER_CONFIG pCanFilter,byte Len);
	int  CANFD_GetDiagnostic(int DevHandle, byte CANIndex, CANFD_DIAGNOSTIC pCanDiagnostic);
	int  CANFD_GetBusError(int DevHandle, byte CANIndex, CANFD_BUS_ERROR pCanBusError);

	/**
	  * @brief  设置CAN调度表数据
	  * @param  DevHandle 设备索引号
	  * @param  CANIndex CAN通道号，取值0或者1
	  * @param  pCanMsgTab CAN调度表列表首地址
	  * @param  pMsgNum 调度表列表中每个调度表包含消息帧数
	  * @param  pSendTimes 每个调度表里面帧发送次数，若为0xFFFF，则循环发送，通过调用CAN_StopSchedule函数停止调用
	  * @param  MsgTabNum 调度表数
	  * @retval 函数执行状态，小于0函数执行出错
	  */
	int  CANFD_SetSchedule(int DevHandle, byte CANIndex, CANFD_MSG[] pCanMsgTab,byte[] pMsgNum,unsigned short[] pSendTimes,byte MsgTabNum);
	/**
	  * @brief  启动调度表
	  * @param  DevHandle 设备索引号
	  * @param  CANIndex CAN通道号，取值0或者1
	  * @param  MsgTabIndex CAN调度表索引号
	  * @param  TimePrecMs 调度表时间精度，比如调度表里面最小帧周期为10ms，那么就建议设置为10
	  * @param  OrderSend 设置为1则顺序发送调度表里面的帧，设置为0则并行发送调度表里面的帧 
	  * @retval 函数执行状态，小于0函数执行出错
	  */
	int  CANFD_StartSchedule(int DevHandle, byte CANIndex, byte MsgTabIndex,byte TimePrecMs,byte OrderSend);
	/**
	  * @brief  停止调度方式发送数据
	  * @param  DevHandle 设备索引号
	  * @param  CANIndex CAN通道号，取值0或者1
	  * @param  MsgTabIndex CAN调度表索引号
	  * @retval 函数执行状态，小于0函数执行出错
	  */
	int  CANFD_StopSchedule(int DevHandle, byte CANIndex);

	int  CANFD_SetRelay(int DevHandle, byte RelayState);
}

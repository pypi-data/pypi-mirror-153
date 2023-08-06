# Traffic Monitor Detector Raw Data (TMD_I480)
# modify from TMD
# v6,v7,v8,v9
#
# parsing Traffic Monitor Detector
# hardware:(Batman-201/601): ISK IWR6843/1843
# company: Joybien Technologies: www.joybien.com
# author: Zach Chen
# ver:0.1.1 2021/09/16
# ver:2.0.1 2022/04/28
# ver:2.0.2 2022/05/12
# ver:2.0.3 2022/05/12
# ver:2.0.4 2022/05/15
#===========================================
# output: V6,V7,V8,v9 Raw data
#
# playback data type:
# 	v6: list/dataFrame
# 	v7: list/dataFrame
# 	v8: dictionary
# 	v9: dictionary


import serial
import time
import struct
import pandas as pd
import numpy as np
import csv

class header:
	version = 0
	totalPackLen = 0
	platform = 0
	timeStamp = 0
	totalPacketLen = 0
	frameNumber = 0
	subFrameNumber = 0
	chirpMargin = 0
	frameMargin = 0 
	trackProcessTime = 0
	uartSendTime = 0
	numTLVs = 0
	checksum = 0


class TrafficMD_I480:
	
	magicWord =  [b'\x01',b'\x02',b'\x03',b'\x04',b'\x05',b'\x06',b'\x07',b'\x08',b'\0x99']
	port = ""
	hdr = header

	# provide csv file dataframe
	# real-time 
	v6_col_names_rt = ['fN','type','range','azimuth','elv' ,'doppler','sx', 'sy', 'sz'] #ok
	v7_col_names_rt = ['fN','type','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','tid']
	v8_col_names_rt = ['fN','type','targetID']
	v9_col_names_rt = ['fN','type','snr','noise']
	
	# read from file for trace point clouds
	fileName = ''
	v6_col_names = ['time','fN','type','range','azimuth','elv' ,'doppler','sx', 'sy', 'sz']
	v7_col_names = ['time','fN','type','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','tid']
	v8_col_names = ['time','fN','type','targetID']
	v9_col_names = ['time','fN','type','snr','noise']
	sim_startFN = 0
	sim_stopFN  = 0 
	
	v6simo = []
	v7simo = []
	v8simo = {}
	v9simo = {}
	
	# add for interal use
	tlvLength = 0
	numOfPoints = 0
	# for debug use 
	dbg = False #Packet unpacket Check: True show message 
	sm  = False #Observed StateMachine: True Show message
	plen = 16 
	
	def __init__(self,port):
		self.port = port
		print("(jb)Traffic Monitor Detector(TMD_I480) raw Data lib initial")
		print("(jb)For Hardware:Batman-201/501/601(ISK)")
		print("(jb)Version: v0.1.0")
		print("(jb)Hardware: IWR-6843/1843")
		print("(jb)Firmware: TMD")
		print("(jb)UART Baud Rate:921600")
		print("==============Info=================")
		print("Output: V6,V7,V8,V9 data:(RAW)")
		print("V6: Point Cloud Spherical")
		print("V6 structure: [(range,azimuth,elevation,doppler,sx,sy,sz),......]")
		print("V7: Target Object List")
		print("V7 structure: [(tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ),....]")
		print("V8: Target Index")
		print("V8 structure: [id1,id2....]")
		print("V9: Point Cloud Side Info")
		print("V9 [(snr,noise),....]")
		print("")
		print("tlvRead status: {0:'EMPTY',1:'inData',10:'IDLE',99:'FALSE'} ")
		print("")
		print("===================================")
	 
		
	def useDebug(self,ft):
		self.dbg = ft
		
	def stateMachine(self,ft):
		self.sm = ft
		
	def getHeader(self):
		return self.hdr
	
	#################################################################
	# for version manegement
	def jb_u32ToBytes(self, v): # convert u32 as Bytes
		A = np.zeros( (4, 1) )
		for i in range(4):
			A[3 - i] = int(v  % 256)
			v = int(v / 256)
		return int(A[0, 0]), int(A[1, 0]), int(A[2, 0]), int(A[3, 0])
	
	def jb_versionManagement(self):
		# test, for example: 
		# result as following,
		# (1) Platform    : IWR ISK, JB, 1843
		# (2) FW   version: V80.61R
		# (3) TOOL version: I.04.08.00
		#
		# (1) Platform
		vHardware, vMagic, vType, vRxTxNum = self.jb_u32ToBytes(self.hdr.platform)			
		# hardware type
		if int(vHardware / 16) == 0:
			tmp = ''
		elif int(vHardware / 16) == 1:
			tmp = 'IWR '
		elif int(vHardware / 16) == 2:
			tmp = 'AWR '
		else:
			tmp = ''
		# hardware antenna
		if int(vHardware % 16) == 0:
			tmp += ''
		elif int(vHardware % 16) == 1:
			tmp += 'ISK'
		elif int(vHardware % 16) == 2:
			tmp += 'AOP'
		else:
			tmp += ''
		vHardware = tmp	
		# sel magic
		if int(vMagic % 16) == 15:
			vMagic = 'JB'
		else:
			vMagic = ''			
		print("Platform    : {}, {}, {:02x}{:02x}".format(vHardware, vMagic, vType, vRxTxNum))
		# (2) FW version
		vAnt, vMagic, vMajor, vMinor = self.jb_u32ToBytes(self.hdr.chirpMargin)			
		# hardware antenna
		if vAnt == 'I':
			vAnt = ', Ant= ISK'
		elif vAnt == 'A':
			vAnt = ', Ant= AOP'
		else:	
			vAnt = ''
		print("FW   version: V{:02d}.{:02d}{:c} {}".format(vMajor, vMinor, vMagic, vAnt))
		# (3) TOOL version
		vTool, vMajor, vMinor, vMicro = self.jb_u32ToBytes(self.hdr.frameMargin)			
		print("TOOL version: {:c}.{:02d}.{:02d}.{:02d}".format(vTool, vMajor, vMinor, vMicro))
	#################################################################
				
	def headerShow(self):
		print("***Header***********") 
		print("Version:     \t%x "%(self.hdr.version))
		#print("Platform:    \t%X "%(self.hdr.platform))
		print("TimeStamp:   \t%s "%(self.hdr.timeStamp))
		print("TotalPackLen:\t%d "%(self.hdr.totalPackLen))
		print("PID(frame#): \t%d "%(self.hdr.frameNumber))
		print("subframe#  : \t%d "%(self.hdr.subFrameNumber))
	    ########################################################
		# original
		#print("Platform:    \t%X "%(self.hdr.platform))		
		#print("Inter-chirp Processing Margin:\t{:d} us".format(self.hdr.chirpMargin))
		#print("Inter-frame Processing Margin:\t{:d} us".format(self.hdr.frameMargin))
		# new replaced
		self.jb_versionManagement()
	    ########################################################
		
		print("Inter-frame Processing Time:\t{:d} us".format(self.hdr.trackProcessTime))
		print("UART Send Time:\t{:d} us".format(self.hdr.uartSendTime))
		print("numTLVs:     \t%d "%(self.hdr.numTLVs))
		print("Check Sum   :\t{:x}".format(self.hdr.checksum))
		print("***End Of Header***") 
			
	#for class internal use
	def tlvTypeInfo(self,dtype,count,dShow):
		sbyte = 8  #tlvHeader Struct = 8 bytes
		unitByte = 20 
		dataByte = 0
		pString = ""
		nString = "numOfPoints :"
		stateString = "V6"
		if dtype == 6:
			unitByte = 0   #pointUnit= 20bytes
			sbyte = 8      #tlvHeader Struct = 8 bytes
			dataByte= 16    #pointStruct 8bytes:(range,azimuth,elevation,doppler)
			pString = "DPIF Point Cloud Spherical TLV"
			nString = ""
			stateString = "V6"
		elif dtype == 7:
			unitByte = 0   #pointUnit= 0bytes 
			sbyte = 8 	   #tlvHeader Struct = 8 bytes
			#old: dataByte = 40  #target struct 40 bytes:(tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ)  # I441
			dataByte = 112 #target struct 112 bytes:(tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ,ec0..15,g,c) # I480 
			pString = "Target Object List TLV"
			nString = "numOfObjects:"
			stateString = "V7"
		elif dtype == 8:
			unitByte = 0 #pointUnit= 0bytes 
			sbyte = 8    #tlvHeader Struct = 8 bytes
			dataByte = 1 #targetID = 1 byte
			pString = "Target Index TLV"
			nString = "numOfIDs"
			stateString = "V8"
		elif dtype == 9:
			unitByte = 0 #pointUnit= 0bytes 
			sbyte = 8    #tlvHeader Struct = 8 bytes
			dataByte = 4 #(snr,noise") =  4 byte
			pString = "DPIF Point Cloud Side Info"
			nString = "numOfIDs"
			stateString = "V9"
		else:
			unitByte = 0
			sbyte = 1
			pString = "*** Type Error ***"
			stateString = 'idle'
		 
		#retCnt = count - unitByte - sbyte
		nPoint = count / dataByte
		if dShow == True:
			print("-----[{:}] ----:{:}".format(pString,stateString))
			print("tlv Type({:2d}Bytes):  \t{:d}".format(sbyte,dtype))
			print("tlv length:      \t{:d}".format(count)) 
			print("num of point:    \t{:d}".format(int(nPoint)))
			print("value length:    \t{:d}".format(count))  
		
		return unitByte,stateString, sbyte, dataByte,count, int(nPoint)
		
	def list2df(self,dck,l6,l7,l8,l9):
		#print("---------------list2df: v6----------------")
		#print(l6)
		
		ll6 = pd.DataFrame(l6,columns=self.v6_col_names_rt)
		ll7 = pd.DataFrame(l7,columns=self.v7_col_names_rt)
		ll8 = pd.DataFrame(l8,columns=self.v8_col_names_rt)
		ll9 = pd.DataFrame(l9,columns=self.v9_col_names_rt)
		#print("------ll6---------list2df: v6----------------")
		#print(ll6)
		return (dck,ll6,ll7,ll8,ll9)

#
# TLV: Type-Length-Value
# read TLV data
# input:
#     disp: True:print message
#			False: hide printing message
# output:(return parameter)
# (pass_fail, v6, v7, v8, v9)
#  pass_fail: True: Data available    False: Data not available
#
#  v6: DPIF point cloud Spherical infomation
#  v7: Target Object List information
#  v8: Target Index information
#  v9: DPIF Point Cloud Side Infomation
#  
#   0: empty: tlv = 0
#   1: data output
#  
#   10: idle
#   99: error
#
	def tlvRead(self,disp,df = None):
		#print("---tlvRead---")
		#ds = dos
		typeList = [6,7,8,9]
		idx = 0
		lstate = 'idle'
		sbuf = b""
		lenCount = 0
		unitByteCount = 0
		dataBytes = 0
		numOfPoints = 0
		tlvCount = 0
		pbyte = 16
		v6 = ([])
		v7 = ([])
		v8 = ([])
		v9 = ([])
		v6df = ([])
		v7df = ([])
		v8df = ([])
		v9df = ([])
	
		while True:
			try:
				ch = self.port.read()
			except:
				#return (False,v6,v7,v8,v9)
				return self.list2df(99,v6,v7,v8,v9) if (df == 'DataFrame') else (99,v6,v7,v8,v9)
			#print(str(ch))
			if lstate == 'idle':
				#print(self.magicWord)
				if ch == self.magicWord[idx]:
					#print("*** magicWord:"+ "{:02x}".format(ord(ch)) + ":" + str(idx))
					idx += 1
					if idx == 8:
						idx = 0
						lstate = 'header'
						rangeProfile = b""
						sbuf = b""
				else:
					#print("not: magicWord state:")
					idx = 0
					rangeProfile = b""
					#return (False,v6,v7,v8,v9)
					return self.list2df(10,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (10,v6,v7,v8,v9)
		
			elif lstate == 'header':
				sbuf += ch
				idx += 1
				if idx == 44: 
					#print("------header-----")
					#print(":".join("{:02x}".format(c) for c in sbuf)) 	 
					#print("len:{:d}".format(len(sbuf))) 
					# [header - Magicword]
					try: 
						(self.hdr.version,self.hdr.platform,self.hdr.timeStamp,self.hdr.totalPackLen,
						self.hdr.frameNumber,self.hdr.subFrameNumber,
						self.hdr.chirpMargin,self.hdr.frameMargin,self.hdr.trackProcessTime,self.hdr.uartSendTime,
						self.hdr.numTLVs,self.hdr.checksum) = struct.unpack('10I2H', sbuf)
						
					except:
						if self.dbg == True:
							print("(Header)Improper TLV structure found: ")
						#return (False,v6,v7,v8,v9)
						return self.list2df(99,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (99,v6,v7,v8,v9)
					
					if disp == True:  
						self.headerShow()
					
					tlvCount = self.hdr.numTLVs
					if self.hdr.numTLVs == 0:
						#return (False,v6,v7,v8,v9)
						#return self.list2df(False,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (False,v6,v7,v8,v9)
						return self.list2df(0,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (0,v6,v7,v8,v9)
						
					if self.sm == True:
						print("(Header)")
						
					sbuf = b""
					idx = 0
					lstate = 'TL'
					  
				elif idx > 48:
					idx = 0
					lstate = 'idle'
					#return (False,v6,v7,v8,v9)
					return self.list2df(99,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (99,v6,v7,v8,v9)
					
			elif lstate == 'TL': #TLV Header type/length
				sbuf += ch
				idx += 1
				if idx == 8:
					#print(":".join("{:02x}".format(c) for c in sbuf))
					try: 
						ttype,self.tlvLength = struct.unpack('2I', sbuf)
						#print("(TL)numTLVs({:d}): tlvCount({:d})-------ttype:tlvLength:{:d}:{:d}".format(self.hdr.numTLVs,tlvCount,ttype,self.tlvLength))
						
						if ttype not in typeList or self.tlvLength > 10000:
							if self.dbg == True:
								print("(TL)Improper TL Length(hex):(T){:d} (L){:x} numTLVs:{:d}".format(ttype,self.tlvLength,self.hdr.numTLVs))
							sbuf = b""
							idx = 0
							lstate = 'idle'
							self.port.flushInput()
							#return (False,v6,v7,v8,v9)
							return self.list2df(99,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (99,v6,v7,v8,v9)
							
					except:
						print("TL unpack Improper Data Found:")
						if self.dbg == True:
							print("TL unpack Improper Data Found:")
						self.port.flushInput()
						#return (False,v6,v7,v8,v9)
					
						return self.list2df(99,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (99,v6,v7,v8,v9)
					
					unitByteCount,lstate ,plen ,dataBytes,lenCount, numOfPoints = self.tlvTypeInfo(ttype,self.tlvLength,disp)
					#print("dataBytes={:d} lenCount={:d}".format(dataBytes , lenCount))
					if self.sm == True:
						print("(TL:{:d})=>({:})".format(tlvCount,lstate))
						
					tlvCount -= 1
					idx = 0  
					sbuf = b""
			
			elif lstate == 'V6': # count = Total Lentgh - 8
				sbuf += ch
				idx += 1
				if (idx%dataBytes == 0):
					try:
						#print(":".join("{:02x}".format(c) for c in sbuf))
						(r,a,e,d) = struct.unpack('4f', sbuf)
						#print("({:2d}:{:4d})(idx:({:4d}) elv:{:.4f} azimuth:{:.4f} doppler:{:.4f} range:{:.4f}".format(numOfPoints,lenCount,idx,e,a,d,r))
						sz  = r * np.sin(e)
						sx  = r * np.cos(e) * np.sin(a)
						sy  = r * np.cos(e) * np.cos(a)
						if (df == 'DataFrame'):
							
							#fieldNames = ['time','frameNum','type','range/px','azimuth/py','elv/vx','doppler/vy','sx/accX','sy/accY','sz/pz','na/vz','na/accZ','na/ID']
							v6df.append((self.hdr.frameNumber,'v6',r,a,e,d,sx,sy,sz))
						else:
							v6.append((r,a,e,d,sx,sy,sz))
							
						sbuf = b""
					except:
						if self.dbg == True:
							print("(6.1)Improper Type 6 Value structure found: ")
						#return (False,v6,v7,v8,v9)
						return self.list2df(99,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (99,v6,v7,v8,v9)
					
				if idx == lenCount:
					if disp == True:
						print("v6[{:d}]".format(len(v6)))
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle'
						if self.sm == True:
							print("(V6:tlvCnt={:d})=>(idle) :true".format(tlvCount))
						#return (True,v6,v7,v8,v9)
						print("(lib)v6=============SaveAppend==============")
						return self.list2df(1,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (1,v6,v7,v8,v9)
						
					else: # Go to TL to get others type value
						lstate = 'TL' #'tlTL'
						if self.sm == True:
							print("(V6:tlvCnt={:d})=>(TL)".format(tlvCount))
					
				elif idx > lenCount:
					idx = 0
					sbuf = b""
					lstate = 'idle'
					#return (False,v6,v7,v8,v9)
					return self.list2df(99,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (99,v6,v7,v8,v9)
					
			elif lstate == 'V9':  
				sbuf += ch
				idx += 1
				if (idx%dataBytes == 0):
					try:
						#print(":".join("{:02x}".format(c) for c in sbuf))
						(snr,noise) =  struct.unpack('2h', sbuf)
						#print("lenCnt = ({:d}) snr:{:.4f} noise:{:.4f}".format(lenCount,snr,noise))
						
						if (df == 'DataFrame'):
							v9df.append((self.hdr.frameNumber,'v9',snr,noise))
						else:
							v9.append((snr,noise))
							
						sbuf = b""
					except:
						if self.dbg == True:
							print("(7)Improper Type 9 Value structure found: ")
						#return (False,v6,v7,v8,v9)
						return self.list2df(99,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (99,v6,v7,v8,v9)
						
				if idx >= lenCount:
					if disp == True:
						print("count= v9[{:d}]".format(len(v9)))
						
					sbuf = b""
					if tlvCount == 0:
						lstate = 'idle'
						if self.sm == True:
							print("(V9)=>(idle) :true")
						#return (True,v6,v7,v8,v9)
						return self.list2df(1,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (1,v6,v7,v8,v9)
						
					else: # Go to TL to get others type value
						lstate = 'TL'
						idx = 0
						if self.sm == True:
							print("(V9)=>(TL)")
							
				if idx > lenCount:
					idx = 0 
					lstate = 'idle'
					sbuf = b""
					#return (False,v6,v7,v8,v9)
					return self.list2df(99,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (99,v6,v7,v8,v9)
					
			elif lstate == 'V7':
				sbuf += ch
				idx += 1
				if (idx % dataBytes == 0):
					
					#print("V7:dataBytes({:d}) lenCount({:d}) index:{:d}".format(dataBytes,lenCount,idx))
					try:
						
						(tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ,ec0,ec1,ec2,ec3,ec4,ec5,ec6,ec7,ec8,ec9,ec10,ec11,ec12,ec13,ec14,ec15,g,conf) = struct.unpack('I27f', sbuf) 
						if (df == 'DataFrame' ):
							v7df.append((self.hdr.frameNumber,'v7',posX,posY,posZ,velX,velY,velZ,accX,accY,accZ,tid))
						else:
							v7.append((posX,posY,posZ,velX,velY,velZ,accX,accY,accZ,tid))
							#print("tid = ({:d}) ,posX:{:.4f} posY:{:.4f} posZ:{:.4f}".format(tid,posX,posY,posZ))
						sbuf = b""
					except:
						if self.dbg == True:
							print("(7)Improper Type 7 Value structure found: ")
						#return (False,v6,v7,v8,v9)
						return self.list2df(99,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (99,v6,v7,v8,v9)
						
				if idx >= lenCount:
					if disp == True:
						print("v7[{:d}]".format(len(v7)))
					 
					sbuf = b""
					if tlvCount == 0:
						lstate = 'idle'
						if self.sm == True:
							print("(V7)=>(idle) :true")
						#return (True,v6,v7,v8,v9)
						return self.list2df(1,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (1,v6,v7,v8,v9)
						
					else: # Go to TL to get others type value
						lstate = 'TL'
						idx = 0
						if self.sm == True:
							print("(V7)=>(TL)")

				if idx > lenCount:
					idx = 0 
					lstate = 'idle'
					sbuf = b""
					#return (False,v6,v7,v8,v9)
					return self.list2df(99,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (99,v6,v7,v8,v9)
				
			elif lstate == 'V8':
				idx += 1
				v8.append(ord(ch))
				if idx == lenCount:
					if disp == True:
						print("=====V8 End====")
					sbuf = b""
					idx = 0
					lstate = 'idle'
					if self.sm == True:
						print("(V8:{:d})=>(idle)".format(tlvCount))
						
					if (df == 'DataFrame'):
						v8o = [self.hdr.frameNumber,'v8']
						v8df = v8o.extend(v8)
					#return (True,v6,v7,v8,v9)
					return self.list2df(1,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (1,v6,v7,v8,v9)
				
				if idx > lenCount:
					sbuf = b""
					idx = 0
					lstate = 'idle'
					#return (False,v6,v7,v8,v9)
					return self.list2df(99,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (99,v6,v7,v8,v9)

	
	############## for playback use #####################
	def readFile(self,fileName):
		with open(fileName, newline='') as csvfile:
			rows = csv.reader(csvfile)
			v6s = [];v7s = [];v8s = [];v9s = []
			for row in rows:
				if row[2] == 'v6':
					v6s.append(row)
				elif row[2] == 'v7':
					v7s.append(row)
				elif row[2] == 'v8':
					v8s.append(row)
				elif row[2] == 'v9':
					v9s.append(row)
					
		v6_col_names = ['time','fN','type','range','azimuth','elv' ,'doppler','sx', 'sy', 'sz']
		self.v6simo = pd.DataFrame(v6s,columns = v6_col_names).astype({'fN': 'int32','type':str,'range':float,'azimuth':float,'elv': float,'doppler':float,'sx':float,'sy':float,'sz':float},errors = 'raise') 
		
		if len(self.v6simo):
			#print(f"self.v6simo['fN'].values[0] = {self.v6simo['fN'].values[0]}")
			self.sim_startFN =  self.v6simo['fN'].values[0]
			self.sim_stopFN  =  self.v6simo['fN'].values[-1]
			
		v7_col_names = ['time','fN','type','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','tid'] 
		self.v7simo = pd.DataFrame(v7s,columns = v7_col_names )
		
		for item in v9s:
			hh = item[3].strip('[]').replace('(', "").replace(')','').split(',')
			self.v9simo[int(item[1])] = [(int(hh[i]),int(hh[i+1])) for i in range(0,len(hh),2)]
		
		for item in v8s:
			hh = item[3].strip('[]').split(',')
			self.v8simo[int(item[1])] = [int(hh[i]) for i in range(len(hh))] 
			

	def getRecordData(self,frameNum):
		s_fn = frameNum + self.sim_startFN
		v6d = self.v6simo.loc[self.v6simo['fN'] == s_fn]  #if (len(self.v6simo) > 0) else []
		v7d = self.v7simo.loc[self.v7simo['fN'] == s_fn]  #if (len(self.v7simo) > 0) else []
		try:
			v8d =  self.v8simo[s_fn]    
		except:
			v8d = {}
			
		try:
			v9d =  self.v9simo[s_fn] 
		except:
			v9d = {}
		 
		return(1,v6d,v7d,v8d,v9d)
	

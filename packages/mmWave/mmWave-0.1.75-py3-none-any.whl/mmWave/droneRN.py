# Drone Radar Navigation
# ver:0.0.2
# 2020/05/12
# parsing  Drone Radar Navigation Sensor
# hardware:(Batman-201)DRN IWR6843
# company: Joybien Technologies: www.joybien.com
# author: Zach Chen
#===========================================
# output: V1,V2,V3,V6,V7 Raw data
# v0.0.1 : 2020/05/12 release
# v0.0.2 : 2020/05/12 release

import serial
import time
import struct
#import numpy as np
from dataclasses import dataclass

class header:
	version = 0
	totalPackLen = 0
	platform = 0
	frameNumber = 0
	timeCpuCycles = 0
	numDetectedObj = 0
	numTLVs = 0
	subFrameIndex = 0
	
class v1Class:
	x = 0.0
	y = 0.0
	z = 0.0
	velocity = 0.0
	
@dataclass	
class statsInfo:
	interFrameProcessingTime = 0
	transmitOutputTime = 0
	interFrameProcessingMargin = 0
	interChirpProcessingMargin = 0
	activeFrameCPULoad = 0
	interFrameCPULoad = 0
	
class DroneRN:
	
	magicWord =  [b'\x02',b'\x01',b'\x04',b'\x03',b'\x06',b'\x05',b'\x08',b'\x07',b'\0x99']
	port = ""
	hdr = header
	
	dck = 0
	# add for VOD interal use
	tlvLength = 0
	
	# for debug use 
	dbg = False #Packet unpacket Check: True show message 
	sm = False #Observed StateMachine: True Show message
	check = False # Observe numTLV and v length
	
	def __init__(self,port):
		self.port = port
		print("(jb)Drone Radar Navigation Sensor")
		print("(jb)For Hardware:IWR1642")
		print("(jb)SW:0.0.1: HW:IWR-1642")
		print("(jb)Firmware: DRN")
		print("(jb)UART Baud Rate:921600*2")
		print("(jb)==================================")
		print("(jb)Output: V1,V2,V3,V6,V7 data:(RAW)")
		print("(jb)V1 :Point Cloud TLV")
		print("(jb)V2 :Range Profile TLV")
		print("(jb)V3 :Noise Profile TLV")
		print("(jb)V6 :Stats Information TLV")
		print("(jb)V7 :Point Cloud Side Info TLV")
		
	def checkTLV(self,ft):
		self.check = ft
		
	def useDebug(self,ft):
		self.dbg = ft
		
	def stateMachine(self,ft):
		self.sm = ft
		
	def getVitalSign(self):
		return self.vs
	
	def getHeader(self):
		return self.hdr
		
	def headerShow(self):
		print("***header***********") 
		print("Version:     \t%x "%(self.hdr.version))
		print("Platform:    \t%X "%(self.hdr.platform))
		print("TotalPackLen:\t%d "%(self.hdr.totalPackLen))
		print("PID(frame#): \t%d "%(self.hdr.frameNumber))
		print("timeCpuCycles: \t%d "%(self.hdr.timeCpuCycles))
		print("numDetectedObj: \t%d "%(self.hdr.numDetectedObj))
		print("numTLVs: \t%d "%(self.hdr.numTLVs))
		print("subFrameIndex: \t%d "%(self.hdr.subFrameIndex))
		print("***End Of Header***") 
		
		
		
	def tlvTypeInfo(self,dtype,count,dShow):
		
		dataByte = 0
		lenCount = count
		pString = ""
		stateString = "V1"
		if dtype == 1:
			dataByte= 16  
			pString = "(V1)Point Cloud"
			lenCount = count
			stateString = 'V1'
		elif dtype == 2:
			lenCount = count
			dataByte = 2  #target 2 bytes:(fft size)  
			pString = "(V2)Range Profile"
			stateString = "V2"
		elif dtype == 3:
			lenCount = count
			dataByte = 2  #target struct 2 bytes:(fft size)  
			pString = "(V3)Noise Profile"
			stateString = "V3"
			
		elif dtype == 6:
			lenCount = count
			dataByte = 24  #target struct 24 bytes:(ifpT,toT,ifpM,icpM,afcL,ifCL)  
			pString = "(V6)Stats Info"
			stateString = "V6"	
		elif dtype == 7:
			lenCount = count
			dataByte = 4  #target struct 4 bytes:(snr,noise)  
			pString = "(V7)Point Cloud Side Info"
			stateString = "V7"
	
		else:
			pString = "*** Type Error ***"
			stateString = 'idle'

		if dShow == True:
			print("-----[{:}] ----".format(pString))
			print("tlv Type :  \t{:d}".format(int(dtype)))
			print("tlv length:      \t{:d}".format(int(lenCount))) 
			#print("{:}      \t{:d}".format(nString,int(nPoint)))
			#print("value length:    \t{:d}".format(retCnt))  
		
		return stateString,dataByte,lenCount,pString
		
#
# TLV: Type-Length-Value
# read TLV data
# input:
#     disp: True:print message
#			False: hide printing message
# output:(return parameter)
# (pass_fail, v1, v2, v6,v7)
#  pass_fail: True: Data available    False: Data not available
#
#	Output: V1,V2,V6,V7 data:(RAW)")
#	V1 :Point Cloud TLV
#	V2 :Range Profile TLV
#   V3 :Noise Profile TLV
#	V6 :Stats Information TLV
#	V7 :Point Cloud Side Info TLV


	def tlvRead(self,disp):
		#print("---tlvRead---")
		
		typeList = [1,2,3,6,7] # zzzz
		idx = 0
		lstate = 'idle'
		sbuf = b""
		lenCount = 0
		unitByteCount = 0
		dataBytes = 0
		
		tlvCount = 0
		pbyte = 16
		v1 = []
		v2 = []
		v3 = []
		v6 = []
		v7 = []
		
		zone = 0
	
		while True:
			try:
				ch = self.port.read()
			except:
				return (False,v1,v2,v3,v6,v7)
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
					return (False,v1,v2,v3,v6,v7)
		
			elif lstate == 'header':
				sbuf += ch
				idx += 1
				if idx == 32: # 32 + 12  = 44
					#print("------header-----")
					#print(":".join("{:02x}".format(c) for c in sbuf)) 	 
					#print("len:{:d}".format(len(sbuf))) 
					# [header - Magicword]
					try: 
						(self.hdr.version,self.hdr.totalPackLen,self.hdr.platform,
						self.hdr.frameNumber,self.hdr.timeCpuCycles,self.hdr.numDetectedObj,
						self.hdr.numTLVs,self.hdr.subFrameIndex) = struct.unpack('8I', sbuf)
					
					except:
						if self.dbg == True:
							print("(Header)Improper TLV structure found: ")
						return (False,v1,v2,v3,v6,v7)
					
					if disp == True:  
						self.headerShow()
					
					tlvCount = self.hdr.numTLVs
						
					if self.hdr.numTLVs == 0 or self.hdr.numTLVs > 10:
						lstate = 'idle'
						return (False,v1,v2,v3,v6,v7)
						
					if self.sm == True:
						print("(Header)")
						
					sbuf = b""
					idx = 0
					lstate = 'TL'
					dck = 0
					  
				elif idx > 45:
					idx = 0
					lstate = 'idle'
					return (False,v1,v2,v3,v6,v7)
					
			elif lstate == 'TL': #TLV Header type/length
				sbuf += ch
				idx += 1
				if idx == 8:
					#print(":".join("{:02x}".format(c) for c in sbuf))
					try:
						ttype,self.tlvLength = struct.unpack('2I', sbuf)
						if self.check:
							print("(check) numTLVs({:d}): tlvCount({:d})---ttype:{:d} tlvLength:{:d}".format(self.hdr.numTLVs,tlvCount,ttype,self.tlvLength))
						if ttype not in typeList:
							if self.dbg == True:
								print("(TL)Improper TL Length(hex):(T){:d} (L){:x} numTLVs:{:d}".format(ttype,self.tlvLength,self.hdr.numTLVs))
							sbuf = b""
							idx = 0
							lstate = 'idle'
							self.port.flushInput()
							return (False,v1,v2,v3,v6,v7)
						if  self.tlvLength > self.hdr.totalPackLen:
							sbuf = b""
							idx = 0
							lstate = 'idle'
							self.port.flushInput()
							return (False,v1,v2,v3,v6,v7)
							
					except:
						if self.dbg == True:
							print("TL unpack Improper Data Found:")
						self.port.flushInput()
						return (False,v1,v2,v3,v6,v7)
					
					lstate,dataBytes,lenCount,pString = self.tlvTypeInfo(ttype,self.tlvLength,disp)
					if lstate == 'V10':
						self.zone = self.tlvLength
					 
					if self.sm == True:
						print("(TL:{:d})=>({:})".format(tlvCount,lstate))
						
					tlvCount -= 1
					idx = 0  
					sbuf = b""
					
			elif lstate == 'V1': #zzzz
				sbuf += ch
				idx += 1
				#print(".".join("{:02x}".format(c) for c in sbuf))
				if (idx%dataBytes == 0):
					try:
						#print(":".join("{:02x}".format(c) for c in sbuf))
						v1s = struct.unpack('4f', sbuf)
						v1.append(v1s)
						#print(v1)
						sbuf = b''
					except:
						if self.dbg == True:
							print("(V1)Improper Type V1 structure found: ")
						return (False,v1,v2,v3,v6,v7)
				
				if idx == lenCount:
					if disp == True:
						print("V1[{:d}]".format(len(v1)))
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle'
						dck += 1
						if self.sm == True:
							print("(V1:{:d})=>(idle) :true".format(tlvCount))
						return (False,v1,v2,v3,v6,v7)
						
					else: # Go to TL to get others type value
						lstate = 'TL' 
						dck += 1
						idx = 0
						sbuf = b""
						if self.sm == True:
							print("(V1:{:d})=>(TL)".format(tlvCount))
						
							
				elif idx > self.hdr.totalPackLen: #lenCount:
					print("V1 data over:{:d} totalPackLen:{:d}".format(idx,self.hdr.totalPackLen))
					idx = 0
					sbuf = b""
					lstate = 'idle'
					return (False,v1,v2,v3,v6,v7)
						 
			elif lstate == 'V7': # zzzz
				sbuf += ch
				idx += 1
				#print(":".join("{:02x}".format(c) for c in sbuf))
				if (idx%dataBytes == 0):
					#print(":".join("{:02x}".format(c) for c in sbuf))
					try:	
						v7s = struct.unpack('2h', sbuf)						
						v7.append(v7s)
						sbuf = b""
					except:
						if self.dbg == True:
							print("(6.1)Improper Type V7 structure found: ")
						return (False,v1,v2,v3,v6,v7)
					
				if idx == lenCount:
					if disp == True:
						print("v7[{:d}]".format(len(v7)))
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle'
						dck += 1
						if self.sm == True:
							print("(V7:{:d})=>(idle) :true".format(tlvCount))
						return (True,v1,v2,v3,v6,v7)
						
					else: # Go to TL to get others type value
						#print(v7)
						lstate = 'TL' 
						dck += 1
						idx = 0
						sbuf = b""
						#print("---------v7 ok ---------{:d}".format(len(v8)))
						if self.sm == True:
							print("(V7:{:d})=>(TL)".format(tlvCount))
					
				elif idx > self.hdr.totalPackLen: #lenCount:
					print("V8 data over:10")
					idx = 0
					sbuf = b""
					lstate = 'idle'
					return (False,v1,v2,v3,v6,v7)
			
			elif lstate == 'V2':
				sbuf += ch
				idx += 1
				#print(".".join("{:02x}".format(c) for c in sbuf))
				if (idx%dataBytes == 0):
					#print(":".join("{:02x}".format(c) for c in sbuf))
					try:	
						v2s = struct.unpack('<H', sbuf)	
						v2f = float(v2s[0]) / 512
						v2.append(v2f)
						sbuf = b""
					except:
						print("(6.1)Improper Type V2 structure found: ")
						if self.dbg == True:
							print("(6.1)Improper Type V2 structure found: ")
						return (False,v1,v2,v3,v6,v7)
					
				if idx == lenCount:
					if disp == True:
						print("v2[{:d}]".format(len(v2)))
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle'
						dck += 1
						if self.sm == True:
							print("(V2:{:d})=>(idle) :true".format(tlvCount))
						return (True,v1,v2,v3,v6,v7)
						
					else: # Go to TL to get others type value
						#print(v2)
						lstate = 'TL' 
						dck += 1
						idx = 0
						sbuf = b""
						#print("---------v7 ok ---------{:d}".format(len(v8)))
						if self.sm == True:
							print("(V2:{:d})=>(TL)".format(tlvCount))
					
				elif idx > self.hdr.totalPackLen: #lenCount:
					print("V2 data over:10")
					idx = 0
					sbuf = b""
					lstate = 'idle'
					return (False,v1,v2,v3,v6,v7)	
			
			elif lstate == 'V6': 
				sbuf += ch
				idx += 1
				#print(".".join("{:02x}".format(c) for c in sbuf))
				if (idx%dataBytes == 0):
					#print(":".join("{:02x}".format(c) for c in sbuf))
					try:		
						si = struct.unpack('<6I', sbuf)		
						v6.append(si)
						sbuf = b""
						#print(v6)
					except:
						print("(6.1)Improper Type V6 structure found: ")
						if self.dbg == True:
							print("(6.1)Improper Type V6 structure found: ")
						return (False,v1,v2,v3,v6,v7)
					
				if idx == lenCount:
					if disp == True:
						print("v6[{:d}]".format(len(v6)))
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle'
						dck += 1
						if self.sm == True:
							print("(V6:{:d})=>(idle) :true".format(tlvCount))
						return (True,v1,v2,v3,v6,v7)
						
					else: # Go to TL to get others type value
						#print(v6)
						lstate = 'TL' 
						dck += 1
						idx = 0
						sbuf = b""
						#print("---------v7 ok ---------{:d}".format(len(v8)))
						if self.sm == True:
							print("(V6:{:d})=>(TL)".format(tlvCount))
					
				elif idx > self.hdr.totalPackLen: #lenCount:
					print("V6 data over:10")
					idx = 0
					sbuf = b""
					lstate = 'idle'
					return (False,v1,v2,v3,v6,v7)				
					
			elif lstate == 'V3':
				sbuf += ch
				idx += 1
				#print(".".join("{:02x}".format(c) for c in sbuf))
				if (idx%dataBytes == 0):
					#print(":".join("{:02x}".format(c) for c in sbuf))
					try:	
						v3s = struct.unpack('<H', sbuf)	
						v3f = float(v3s[0]) / 512
						v3.append(v3f)
						sbuf = b""
					except:
						print("(6.1)Improper Type V3 structure found: ")
						if self.dbg == True:
							print("(6.1)Improper Type V3 structure found: ")
						return (False,v1,v2,v3,v6,v7)
					
				if idx == lenCount:
					if disp == True:
						print("v3[{:d}]".format(len(v3)))
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle'
						dck += 1
						if self.sm == True:
							print("(V3:{:d})=>(idle) :true".format(tlvCount))
						return (True,v1,v2,v3,v6,v7)
						
					else: # Go to TL to get others type value
						#print(v3)
						lstate = 'TL' 
						dck += 1
						idx = 0
						sbuf = b""
						#print("---------v3 ok ---------{:d}".format(len(v8)))
						if self.sm == True:
							print("(V3:{:d})=>(TL)".format(tlvCount))
			elif lstate == 'V9':
				idx += 1
				sbuf += ch
				 
				if idx == lenCount: 
					#avgPower1,avgPower2,powerRatio1,powerRatio1,crossCorr = struct.unpack('5f',sbuf)
					v9 =  struct.unpack('5f',sbuf)
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle'
						if self.sm == True:
							print("(V9:{:d})=>(idle) :true".format(tlvCount))
						return (True,v8,v9,v10,v11)
					else:
						if self.sm == True:
							print("(V9)=>(TL)")
						lstate = 'TL'
						
				if idx > lenCount:
					idx = 0 
					sbuf = b""
					lstate = 'idle'
					
			elif lstate == 'V10':
				idx += 1
				v10.append(ord(ch))
				if idx == lenCount:
					#print("V10:dataBytes({:d}) lenCount({:d}) index:{:d}".format(dataBytes,lenCount,idx))
					if disp == True:
						print("v10[{:d}]".format(len(v10)))
					 
					sbuf = b""
					if tlvCount <= 0:
						lstate = 'idle'
						if self.sm == True:
							print("(V10)=>(idle) :true")
						return (True,v8,v9,v10,v11)
						
					else: # Go to TL to get others type value
						lstate = 'TL'
						idx = 0
						sbuf = b""
						#print("(V10)=>(TL) len={:d}".format(len(v10)))
						if self.sm == True:
							print("(V10)=>(TL)")

				if idx > 10:
					print("V10 data over:10")
					idx = 0 
					lstate = 'idle'
					sbuf = b""
					if self.sm == True:
						print("(V10)=>(idle)")
					return (False,v8,v9,v10,v11)
			
			elif lstate == 'V11': 
				#print("dataBytes:{:d}  lenCount:{:d}   idx:{:d}".format(dataBytes,lenCount,idx))
				sbuf += ch
				idx += 1
				if idx%dataBytes == 0:
					#unwrapped,heart,breathing,heart_rate,breathing_rate = struct.unpack('5f',sbuf)
					#v11.append((unwrapped,heart,breathing,heart_rate,breathing_rate))
					self.vs = struct.unpack('5f',sbuf)
					v11.append(self.vs)
					#print("uw:{:f} heart:{:f} breathing:{:f}  hrate:{:f}  bRate:{:f} ".format(unwrapped,heart,breathing,heart_rate,breathing_rate))
					if disp == True:
						print("(V11)")
					sbuf = b"" 
				
				if idx == lenCount:
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle'
						if self.check:
							print("V11 ----> idle")
						#print("(V11)len = {:d}".format(len(v11)))
						dck += 8
						if self.sm == True:
							print("(V11:{:d})=>(idle) :true".format(tlvCount))
						return (True,v8,v9,v10,v11)
					else:
						lstate =  'TL'
						if self.sm == True:
							print("(V11)=>(TL)")
						 
						
				if idx > 60:
					print("V11 data over:60")
					if self.sm == True:
							print("(V11)=>(TL)")
					idx = 0 
					lstate = 'idle'
					sbuf = b""
					return (False,v8,v9,v10,v11)
			





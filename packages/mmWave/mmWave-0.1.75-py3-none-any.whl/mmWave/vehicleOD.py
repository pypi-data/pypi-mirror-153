# Vehicle Occupant Detection and Driver Vital Sign
# for only
# ver:0.0.1
# 2020/02/10
# parsing Vehicle Occupant Detection 3D data 
# hardware:(Batman-301)VOD IWR1642
# company: Joybien Technologies: www.joybien.com
# author: Zach Chen
#===========================================
# output: V6,V7,V8 Raw data
# v0.0.1 : 2019/10/26 release

import serial
import time
import struct
#import numpy as np

class header:
	version = 0
	totalPackLen = 0
	platform = 0
	frameNumber = 0
	timeCpuCycles = 0
	numDetectedObj = 0
	numTLVs = 0
	subFrameIndex = 0
	
class vitalSign:
	unwrapped = 0.0
	heart = 0.0
	breathing  = 0.0
	heart_rate = 0.0
	breathing_rate = 0.0

class VehicleOD:
	
	magicWord =  [b'\x02',b'\x01',b'\x04',b'\x03',b'\x06',b'\x05',b'\x08',b'\x07',b'\0x99']
	port = ""
	hdr = header
	vs  = vitalSign
	dck = 0
	# add for VOD interal use
	tlvLength = 0
	
	# for debug use 
	dbg = False #Packet unpacket Check: True show message 
	sm = False #Observed StateMachine: True Show message
	check = False # Observe numTLV and v length
	
	def __init__(self,port):
		self.port = port
		print("(jb)Vehicle Occupant Detection and Driver Vital Sign")
		print("(jb)For Hardware:IWR1642")
		print("(jb)SW:0.0.1: HW:IWR-1642")
		print("(jb)Firmware: VOD")
		print("(jb)UART Baud Rate:921600")
		print("(jb)==================================")
		print("(jb)Output: V8,V9,V10,V11 data:(RAW)")
		print("(jb)V8 :Range Azimuth Heatmap TLV")
		print("(jb)V9 :Feature Vector TLV")
		print("(jb)V10:Decision Vector TLV")
		print("(jb)V11:Vital Sign Vector TLV")
		
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
		stateString = "V8"
		if dtype == 8:
			dataByte= 2    #HeatMap Value Int
			pString = "Range-Azimuth Heat Map"
			lenCount = count
			stateString = 'V8'
		elif dtype == 9:
			lenCount = count
			dataByte = 20  #target struct 20 bytes:(avgPower1,avgPower2,powerRatio1,powerRatio2,crossCorr)  
			pString = "Feature Vector TLV"
			stateString = "V9"
		elif dtype == 10:
			lenCount = count
			dataByte = 1 #zone = 1 byte
			pString = "Decision Vector TLV"
			stateString = "V10"
			
		elif dtype == 11:
			lenCount = count
			dataByte = 20 #zone = 1 byte
			pString = "Vital Sign Vector TLV"
			stateString = "V11"
		else:
			pString = "*** Type Error ***"
			stateString = 'idle'

		if dShow == True:
			print("-----[{:}] ----".format(pString))
			print("tlv Type :  \t{:d}".format(dtype))
			print("tlv length:      \t{:d}".format(lenCount)) 
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
# (pass_fail, v8, v9, v10,v11)
#  pass_fail: True: Data available    False: Data not available
#
#	Output: V8,V9,V10,V11 data:(RAW)")
#	V8 :Range Azimuth Heatmap TLV 
#	V9 :Feature Vector TLV 
#	V10:Decision Vector TLV 
#	V11:Vital Sign Vector TLV 
#

	def tlvRead(self,disp):
		#print("---tlvRead---")
		#ds = dos
		typeList = [8,9,10,11]
		idx = 0
		lstate = 'idle'
		sbuf = b""
		lenCount = 0
		unitByteCount = 0
		dataBytes = 0
		
		tlvCount = 0
		pbyte = 16
		v8 = []
		v9 = ([])
		v10 = ([])
		v11 = ([])
		zone = 0
	
		while True:
			try:
				ch = self.port.read()
			except:
				return (False,v8,v9,v10,v11)
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
					return (False,v8,v9,v10,v11)
		
			elif lstate == 'header':
				sbuf += ch
				idx += 1
				if idx == 32: 
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
						return (False,v8,v9,v10,v11)
					
					if disp == True:  
						self.headerShow()
					
					tlvCount = self.hdr.numTLVs
					if self.hdr.numTLVs == 0:
						return (False,v8,v9,v10,v11)
						
					if self.sm == True:
						print("(Header)")
						
					sbuf = b""
					idx = 0
					lstate = 'TL'
					dck = 0
					  
				elif idx > 40:
					idx = 0
					lstate = 'idle'
					return (False,v8,v9,v10,v11)
					
			elif lstate == 'TL': #TLV Header type/length
				sbuf += ch
				idx += 1
				if idx == 8:
					#print(":".join("{:02x}".format(c) for c in sbuf))
					try:
						ttype,self.tlvLength = struct.unpack('2I', sbuf)
						if self.check:
							print("(check) numTLVs({:d}): tlvCount({:d})-------ttype:tlvLength:{:d}:{:d}".format(self.hdr.numTLVs,tlvCount,ttype,self.tlvLength))
						if ttype not in typeList or self.tlvLength > 10000:
							if self.dbg == True:
								print("(TL)Improper TL Length(hex):(T){:d} (L){:x} numTLVs:{:d}".format(ttype,self.tlvLength,self.hdr.numTLVs))
							sbuf = b""
							idx = 0
							lstate = 'idle'
							self.port.flushInput()
							return (False,v8,v9,v10,v11)
							
					except:
						if self.dbg == True:
							print("TL unpack Improper Data Found:")
						self.port.flushInput()
						return (False,v8,v9,v10,v11)
					
					lstate,dataBytes,lenCount,pString = self.tlvTypeInfo(ttype,self.tlvLength,disp)
					if lstate == 'V10':
						self.zone = self.tlvLength
					 
					if self.sm == True:
						print("(TL:{:d})=>({:})".format(tlvCount,lstate))
						
					tlvCount -= 1
					idx = 0  
					sbuf = b""
			
					
			elif lstate == 'V8': # count = Total Lentgh - 8
				sbuf += ch
				idx += 1
				if (idx%dataBytes == 0):
					try:
						#print(":".join("{:02x}".format(c) for c in sbuf))
						v8s = struct.unpack('h', sbuf)						
						v8.append(v8s[0])
						sbuf = b""
					except:
						if self.dbg == True:
							print("(6.1)Improper Type V8 structure found: ")
						return (False,v8,v9,v10,v11)
					
				if idx == lenCount:
					if disp == True:
						print("v8[{:d}]".format(len(v8)))
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle'
						dck += 1
						if self.sm == True:
							print("(V8:{:d})=>(idle) :true".format(tlvCount))
						return (True,v8,v9,v10,v11)
						
					else: # Go to TL to get others type value
						lstate = 'TL' 
						dck += 1
						idx = 0
						sbuf = b""
						#print("---------v8 ok ---------{:d}".format(len(v8)))
						if self.sm == True:
							print("(V8:{:d})=>(TL)".format(tlvCount))
					
				elif idx > 7000: #lenCount:
					print("V8 data over:10")
					idx = 0
					sbuf = b""
					lstate = 'idle'
					return (False,v8,v9,v10,v11)
					
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
			





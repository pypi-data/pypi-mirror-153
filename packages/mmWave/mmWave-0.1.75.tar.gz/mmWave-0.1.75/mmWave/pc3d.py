# 3D People Counting-OSD 3D Raw Data (pc3d)
# ver:0.0.1
# 2019/10/16
# parsing 3D People Overhead Counting data 
# hardware:(Batman-301)ODS IWR6843 ES2.0 only
# company: Joybien Technologies: www.joybien.com
# author: Zach Chen
#===========================================
# output: V6,V7,V8 Raw data
# v0.0.1 : 2019/10/26 release
# v0.0.2 : 2019/10/27 release



import serial
import time
import struct
#import numpy as np

class header:
	version = 0
	totalPackLen = 0
	platform = 0
	frameNumber = 0
	subframeNumber = 0
	chirpMargin = 0
	frameMargin = 0 
	trackProcessTime = 0
	uartSendTime = 0
	numTLVs = 0
	checksum = 0

class unitS:
	elevationUnit:float = 0.0
	azimuthUnit : float = 0.0
	dopplerUnit :float = 0.0
	rangeUnit :float = 0.0
	snrUnit :float = 0.0

class Pc3d:
	
	magicWord =  [b'\x02',b'\x01',b'\x04',b'\x03',b'\x06',b'\x05',b'\x08',b'\x07',b'\0x99']
	port = ""
	hdr = header
	u = unitS
	
	# add for PMB interal use
	tlvLength = 0
	numOfPoints = 0
	# for debug use 
	dbg = False #Packet unpacket Check: True show message 
	sm = False #Observed StateMachine: True Show message
	plen = 16 
	
	def __init__(self,port):
		self.port = port
		print("(jb)3D People Overhead Counting initial")
		print("(jb)For Hardware:Batman-301(ODS)")
		print("(jb)Hardware: IWR-6843 ES2.0")
		print("(jb)Firmware: FDS")
		print("(jb)UART Baud Rate:921600")
		print("Output: V6,V7,V8 data:(RAW)")
		
	def useDebug(self,ft):
		self.dbg = ft
		
	def stateMachine(self,ft):
		self.sm = ft
		
	def getHeader(self):
		return self.hdr
		
	def headerShow(self):
		print("***header***********") 
		print("Version:     \t%x "%(self.hdr.version))
		print("Platform:    \t%X "%(self.hdr.platform))
		print("TotalPackLen:\t%d "%(self.hdr.totalPackLen))
		print("PID(frame#): \t%d "%(self.hdr.frameNumber))
		print("subframe#  : \t%d "%(self.hdr.subframeNumber))
		print("Inter-frame Processing Time:\t{:d} us".format(self.hdr.trackProcessTime))
		print("UART Send Time:\t{:d} us".format(self.hdr.uartSendTime))
		print("Inter-chirp Processing Margin:\t{:d} us".format(self.hdr.chirpMargin))
		print("Inter-frame Processing Margin:\t{:d} us".format(self.hdr.frameMargin))
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
		stateString = "V6-unit"
		if dtype == 6:
			unitByte = 20  #pointUnit= 20bytes
			sbyte = 8      #tlvHeader Struct = 8 bytes
			dataByte= 8    #pointStruct 8bytes:(elevation,azimuth,doppler,range,snr)
			pString = "Point Cloud TLV"
			nString = ""
		elif dtype == 7:
			unitByte = 0   #pointUnit= 0bytes 
			sbyte = 8 	   #tlvHeader Struct = 8 bytes
			dataByte = 40  #target struct 40 bytes:(tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ)  
			pString = "Target Object TLV"
			nString = "numOfObjects:"
			stateString = "V7"
		elif dtype == 8:
			unitByte = 0 #pointUnit= 0bytes 
			sbyte = 8    #tlvHeader Struct = 8 bytes
			dataByte = 1 #targetID = 1 byte
			pString = "Target Index TLV"
			nString = "numOfIDs"
			stateString = "V8"
		else:
			unitByte = 0
			sbyte = 1
			pString = "*** Type Error ***"
			stateString = 'idle'
		 
		retCnt = count - unitByte -sbyte
		nPoint = retCnt / sbyte
		if dShow == True:
			print("-----[{:}] ----".format(pString))
			print("tlv Type({:2d}B):  \t{:d}".format(sbyte,dtype))
			print("tlv length:      \t{:d}".format(count)) 
			print("{:}      \t{:d}".format(nString,int(nPoint)))
			print("value length:    \t{:d}".format(retCnt))  
		
		return unitByte,stateString, sbyte, dataByte,retCnt, int(nPoint)
		
#
# TLV: Type-Length-Value
# read TLV data
# input:
#     disp: True:print message
#			False: hide printing message
# output:(return parameter)
# (pass_fail, v6, v7, v8)
#  pass_fail: True: Data available    False: Data not available
#  v6: point cloud infomation
#  v7: Target Object information
#  v8: Target Index information
#
	def tlvRead(self,disp):
		#print("---tlvRead---")
		#ds = dos
		typeList = [6,7,8]
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
	
		while True:
			try:
				ch = self.port.read()
			except:
				return (False,v6,v7,v8)
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
					return (False,v6,v7,v8)
		
			elif lstate == 'header':
				sbuf += ch
				idx += 1
				if idx == 40: 
					#print("------header-----")
					#print(":".join("{:02x}".format(c) for c in sbuf)) 	 
					#print("len:{:d}".format(len(sbuf))) 
					# [header - Magicword]
					try: 
						(self.hdr.version,self.hdr.totalPackLen,self.hdr.platform,
						self.hdr.frameNumber,self.hdr.subframeNumber,
						self.hdr.chirpMargin,self.hdr.frameMargin,self.hdr.trackProcessTime,self.hdr.uartSendTime,
						self.hdr.numTLVs,self.hdr.checksum) = struct.unpack('9I2H', sbuf)
						
					except:
						if self.dbg == True:
							print("(Header)Improper TLV structure found: ")
						return (False,v6,v7,v8)
					
					if disp == True:  
						self.headerShow()
					
					tlvCount = self.hdr.numTLVs
					if self.hdr.numTLVs == 0:
						return (True,v6,v7,v8)
						
					if self.sm == True:
						print("(Header)")
						
					sbuf = b""
					idx = 0
					lstate = 'TL'
					  
				elif idx > 44:
					idx = 0
					lstate = 'idle'
					return (False,v6,v7,v8)
					
			elif lstate == 'TL': #TLV Header type/length
				sbuf += ch
				idx += 1
				if idx == 8:
					#print(":".join("{:02x}".format(c) for c in sbuf))
					try:
						ttype,self.tlvLength = struct.unpack('2I', sbuf)
						#print("---{:d}: tlvCount({:d})-------ttype:tlvLength:{:d}:{:d}".format(self.hdr.numTLVs,tlvCount,ttype,self.tlvLength))
						if ttype not in typeList or self.tlvLength > 10000:
							if self.dbg == True:
								print("(TL)Improper TL Length(hex):(T){:d} (L){:x} numTLVs:{:d}".format(ttype,self.tlvLength,self.hdr.numTLVs))
							sbuf = b""
							idx = 0
							lstate = 'idle'
							self.port.flushInput()
							return (False,v6,v7,v8)
							
					except:
						if self.dbg == True:
							print("TL unpack Improper Data Found:")
						self.port.flushInput()
						return (False,v6,v7,v8)
					
					unitByteCount,lstate ,plen ,dataBytes,lenCount, numOfPoints = self.tlvTypeInfo(ttype,self.tlvLength,disp)
				
					if self.sm == True:
						print("(TL:{:d})=>({:})".format(tlvCount,lstate))
						
					tlvCount -= 1
					idx = 0  
					sbuf = b""
			
			elif lstate == 'V6-unit':
				sbuf += ch
				idx += 1
				if idx == unitByteCount :
					#print(":".join("{:02x}".format(c) for c in sbuf))
					#print("unitByte:{:d}".format(len(sbuf)))
					try:
						self.u.elevationUnit,self.u.azimuthUnit,self.u.dopplerUnit,self.u.rangeUnit,self.u.snrUnit = struct.unpack('5f', sbuf)
						#print("Unit  ==> elv:{:.4f} azimuth:{:.4f} doppler:{:.4f} range:{:.4f} snr:{:.4f}".format(self.u.elevationUnit,self.u.azimuthUnit,self.u.dopplerUnit,self.u.rangeUnit,self.u.snrUnit))
						sbuf = b""
						idx = 0
						lstate = 'V6'				
					except:
						if self.dbg == True:
							print("(6.0)Improper Type 6 unit Value structure found: ")
						return (False,v6,v7,v8)
					
					if self.sm == True:
						print("(V6-unit:{:d})=>({:})".format(tlvCount,lstate))
						#print("(V6-unit)=>({:})".format(lstate))
					
			elif lstate == 'V6': # count = Total Lentgh - 8
				sbuf += ch
				idx += 1
				if (idx%dataBytes == 0):
					try:
						#print(":".join("{:02x}".format(c) for c in sbuf))
						(e,a,d,r,s) = struct.unpack('2b3h', sbuf)
						elv = e * self.u.elevationUnit
						azi = a * self.u.azimuthUnit
						dop = d * self.u.dopplerUnit
						ran = r * self.u.rangeUnit
						snr = s * self.u.snrUnit
						#print("({:2d}:{:4d})(idx:({:4d}) elv:{:.4f} azimuth:{:.4f} doppler:{:.4f} range:{:.4f} snr:{:.4f}".format(numOfPoints,lenCount,idx,elv,azi,dop,ran,snr))
						
						v6.append((elv,azi,dop,ran,snr))
						#print("point_cloud_2d.append:[{:d}]".format(len(point_cloud_2d)))
						sbuf = b""
					except:
						if self.dbg == True:
							print("(6.1)Improper Type 6 Value structure found: ")
						return (False,v6,v7,v8)
					
				if idx == lenCount:
					if disp == True:
						print("v6[{:d}]".format(len(v6)))
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle'
						if self.sm == True:
							print("(V6:{:d})=>(idle) :true".format(tlvCount))
						return (True,v6,v7,v8)
						
					else: # Go to TL to get others type value
						lstate = 'TL' #'tlTL'
						if self.sm == True:
							print("(V6:{:d})=>(TL)".format(tlvCount))
					
				elif idx > lenCount:
					idx = 0
					sbuf = b""
					lstate = 'idle'
					return (False,v6,v7,v8)
				
			elif lstate == 'V7':
				sbuf += ch
				idx += 1
				if (idx%dataBytes == 0):
					#print("V7:dataBytes({:d}) lenCount({:d}) index:{:d}".format(dataBytes,lenCount,idx))
					try:
						(tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ) = struct.unpack('I9f', sbuf)
						v7.append((tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ))
						sbuf = b""
					except:
						if self.dbg == True:
							print("(7)Improper Type 7 Value structure found: ")
						return (False,v6,v7,v8)
						
				if idx >= lenCount:
					if disp == True:
						print("v7[{:d}]".format(len(v7)))
					 
					sbuf = b""
					if tlvCount == 0:
						lstate = 'idle'
						if self.sm == True:
							print("(V7)=>(idle) :true")		 
						return (True,v6,v7,v8)	
						
					else: # Go to TL to get others type value
						lstate = 'TL'
						idx = 0
						if self.sm == True:
							print("(V7)=>(TL)")

				if idx > lenCount:
					idx = 0 
					lstate = 'idle'
					sbuf = b""
					return (False,v6,v7,v8)
				
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
					return (True,v6,v7,v8)
				
				if idx > lenCount:
					sbuf = b""
					idx = 0
					lstate = 'idle'
					return (False,v6,v7,v8)





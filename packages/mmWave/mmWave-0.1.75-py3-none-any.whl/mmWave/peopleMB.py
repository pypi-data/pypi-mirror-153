# People Movement Behavior(PMB)
# ver:0.0.3
# 2019/02/21
#
# ver:0.0.4
# 2019/12/06
# ver:0.0.5
# 2020/04/21


import serial
import time
import struct
#import numpy as np

class header:
	version = 0
	platform = 0
	timestamp = 0
	totalPackLen = 0
	frameNumber = 0
	subframeNumber = 0
	chirpMargin = 0
	frameMargin = 0
	uartSendTime = 0
	trackProcessTime = 0
	numTLVs = 0
	checksum = 0
	

class PeopleMB:
	
	magicWord =  [b'\x02',b'\x01',b'\x04',b'\x03',b'\x06',b'\x05',b'\x08',b'\x07',b'\0x99']
	port = ""
	hdr = header
	
	# add for PMB interal use
	tlvLength = 0
	numOfPoints = 0
	# for debug use 
	dbg = False #Packet unpacket Check: True show message 
	sm = False #Observed StateMachine: True Show message
	plen = 16  #number bytes of per package type6:16 type7:68 type8:1
	
	def __init__(self,port):
		self.port = port
		print("***People Moving Behavior init***")
		
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
		print("Time Stamp:  \t%s "%(self.hdr.timestamp))
		print("TotalPackLen:\t%d "%(self.hdr.totalPackLen))
		print("PID(frame#): \t%d "%(self.hdr.frameNumber))
		print("subframe#  : \t%d "%(self.hdr.subframeNumber))
		print("Inter-frame Processing Time:\t{:d} us".format(self.hdr.trackProcessTime))
		print("UART Send Time:\t{:d} us".format(self.hdr.uartSendTime))
		print("Inter-chirp Processing Margin:\t{:d} us".format(self.hdr.chirpMargin))
		print("Inter-frame Processing Margin:\t{:d} us".format(self.hdr.frameMargin))
		print("numTLVs:     \t%d "%(self.hdr.numTLVs))
		print("Check Sum   :\t{:x}".format(self.hdr.checksum))
		
		
	#for class internal use
	def tlvTypeInfo(self,dtype,count,dShow):
		sbyte = 16
		pString = ""
		nString = "numOfPoints :"
		stateString = "V6"
		if dtype == 6:
			sbyte = 16
			pString = "Point Cloud TLV"
		elif dtype == 7:
			sbyte = 68
			pString = "Target Object TLV"
			nString = "numOfObjects:"
			stateString = "V7"
		elif dtype == 8:
			pString = "Target Index TLV"
			sbyte = 1
			stateString = "V8"
		else:
			sbyte = 1
			pString = "*** Type Error ***"
			stateString = 'idle'
		 
		retCnt = count - 8
		nPoint = retCnt / sbyte
		if dShow == True:
			print("-----[{:}] ----".format(pString))
			print("tlv Type({:2d}B):  \t{:d}".format(sbyte,dtype))
			print("tlv length:      \t{:d}".format(count)) 
			print("{:}      \t{:d}".format(nString,int(nPoint)))
			print("value length:    \t{:d}".format(retCnt))  
		
		return stateString, sbyte, retCnt, nPoint
		
#
# TLV: Type-Length-Value
# read TLV data
# input:
#     disp: True:print message
#			False: hide printing message
# output:(return parameter)
# (pass_fail, v6, v7, v8)
#  pass_fail: True: Data available    False: Data not available
#  v6: point cloud 2d infomation
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
					idx = 0
					rangeProfile = b""
					return (False,v6,v7,v8)
		
			elif lstate == 'header':
				sbuf += ch
				idx += 1
				if idx == 44:
					#print("------header-----")
					#print(":".join("{:02x}".format(c) for c in sbuf))  
					# [header - Magicword]
					try: 
						''' v0.0.3
						(self.hdr.version,self.hdr.platform,self.hdr.timestamp,
						self.hdr.totalPackLen,self.hdr.frameNumber,self.hdr.subframeNumber,
						self.hdr.chirpMargin, self.hdr.frameMargin,self.hdr.uartSendTime,
						self.hdr.trackProcessTime,self.hdr.numTLVs,
						self.hdr.checksum) = struct.unpack('6I4L2H', sbuf)
						'''
						# v0.0.4
						(self.hdr.version,self.hdr.platform,self.hdr.timestamp,
						self.hdr.totalPackLen,self.hdr.frameNumber,self.hdr.subframeNumber,
						self.hdr.chirpMargin, self.hdr.frameMargin,self.hdr.uartSendTime,
						self.hdr.trackProcessTime,self.hdr.numTLVs,
						self.hdr.checksum) = struct.unpack('10I2H', sbuf)
						
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
					
			elif lstate == 'TL':
				sbuf += ch
				idx += 1
				if idx == 8:
					#print(":".join("{:02x}".format(c) for c in sbuf))
					try:
						ttype,self.tlvLength = struct.unpack('2I', sbuf)
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
					
					lstate ,plen ,lenCount,self.numOfPoints = self.tlvTypeInfo(ttype,self.tlvLength,disp)
					
					if self.sm == True:
						print("(TL)=>({:})".format(lstate))
						
					tlvCount -= 1
					idx = 0  
					sbuf = b""
				
					 
			elif lstate == 'V6': # count = Total Lentgh - 8
				sbuf += ch
				idx += 1
				if (idx%plen == 0):
					try:
						#print(":".join("{:02x}".format(c) for c in sbuf))
						(range2d,azimuth,doppler,snr) = struct.unpack('4f', sbuf)
						#print("range2d:{:.4f} azimuth:{:.4f} doppler:{:.4f} snr:{:.4f}".format(range2d,azimuth,doppler,snr))
						v6.append((range2d,azimuth,doppler,snr))
						#print("point_cloud_2d.append:[{:d}]".format(len(point_cloud_2d)))
						sbuf = b""
					except:
						if self.dbg == True:
							print("(6)Improper Type 6 Value structure found: ")
						return (False,v6,v7,v8)
					
				if idx == lenCount:
					if disp == True:
						print("v6[{:d}]".format(len(v6)))
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle'
						return (True,v6,v7,v8)
						
					else: # Go to TL to get others type value
						lstate = 'TL' #'tlTL'
						if self.sm == True:
							print("(V6)=>(TL)")
					
				elif idx > lenCount:
					idx = 0
					sbuf = b""
					lstate = 'idle'
					return (False,v6,v7,v8)
				
			elif lstate == 'V7':
				sbuf += ch
				idx += 1
				if (idx%plen == 0):
					try:
						EC = [0,0,0,0,0,0,0,0,0]
						(tid,posX,posY,velX,velY,accX,accY,EC[0],EC[1],EC[2],EC[3],EC[4],EC[5],EC[6],EC[7],EC[8],G) = struct.unpack('1I16f', sbuf)
						v7.append((tid,posX,posY,velX,velY,accX,accY,EC,G))
						sbuf = b""
					except:
						if self.dbg == True:
							print("(7)Improper Type 7 Value structure found: ")
						return (False,v6,v7,v8)
						
				if idx == lenCount:
					if disp == True:
						print("v7[{:d}]".format(len(v7)))
					idx = 0 
					sbuf = b""
					if tlvCount <= 0:
						lstate = 'idle'
						return (True,v6,v7,v8)
						
					else: # Go to TL to get others type value
						lstate = 'TL' 
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
						print("v8:{:}".format(v8))
						print("=====V8 End====")
						
					sbuf = b""
					idx = 0
					lstate = 'idle'
					if self.sm == True:
						print("(V8)=>(idle)")
					return (True,v6,v7,v8)
				
				if idx > lenCount:
					sbuf = b""
					idx = 0
					lstate = 'idle'
					return (False,v6,v7,v8)





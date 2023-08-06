# Vehicle Occupancy Detection(VOD) and Child Presence Detection(CPD)
# for only
# ver:0.0.1
# 2020/02/10
# parsing Vehicle Occupancy Detection and Child Presence Detection(CPD) data 
# Use: HeatMap
# hardware:(Batman-301)VOD/CPD AWR6843
# company: Joybien Technologies: www.joybien.com
# author: Zach Chen
#===========================================
# output: V6,V7,V8 Raw data
# v0.0.1 : 2020/07/21 release

import serial
import time
import struct
#import numpy as np

class header:
	totalPackLen = 0
	platform = 0
	frameNumber = 0
	timeCpuCycles = 0
	numDetectedObj = 0
	numTLVs = 0


class VehicleODHeatMap:
	
	magicWord =  [b'\x02',b'\x01',b'\x04',b'\x03',b'\x06',b'\x05',b'\x08',b'\x07',b'\0x99']
	port = ""
	hdr = header
	 
	# add for VOD interal use
	tlvLength = 0
	
	# for debug use 
	dbg = False #Packet unpacket Check: True show message 
	sm = False  #Observed StateMachine: True Show message
	check = False # Observe numTLV and v length
	
	def __init__(self,port):
		self.port = port
		print("(jb)Vehicle Occupancy Detection(VOD) and Child Presence Detection(CPD)")
		print("(jb)For Hardware:AWR6843")
		print("(jb)SW:0.0.1: HW:IWR-1642")
		print("(jb)Firmware: VOD")
		print("(jb)UART Baud Rate:921600")
		print("(jb)==================================")
		print("(jb)Output: V8,V9,V10 data:(RAW)")
		print("(jb)V8 :Range Azimuth Heatmap TLV")
		print("(jb)V9 :Feature Vector TLV")
		print("(jb)V10:Decision Vector TLV")
		
		
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
		#print("Version:     \t%x "%(self.hdr.version))
		print("Platform:    \t%X "%(self.hdr.platform))
		print("TotalPackLen:\t%d "%(self.hdr.totalPackLen))
		print("PID(frame#): \t%d "%(self.hdr.frameNumber))
		print("timeCpuCycles: \t%d "%(self.hdr.timeCpuCycles))
		print("numDetectedObj: \t%d "%(self.hdr.numDetectedObj))
		print("numTLVs: \t%d "%(self.hdr.numTLVs))
		#print("subFrameIndex: \t%d "%(self.hdr.subFrameIndex))
		print("***End Of Header***") 
		
		
		
	def tlvTypeInfo(self,dtype,count,dShow):
		
		dataByte = 0
		lenCount = count
		pString = ""
		stateString = "V8"
		if dtype == 8:
			lenCount = count
			dataByte= 2    #HeatMap Value Int:2 bytes float:4 bytes
			pString = "Range-Azimuth Heat Map"
			stateString = 'V8'
			
		elif dtype == 9:
			lenCount = count
			dataByte = 20  #target struct 20 bytes:(avgPower1,avgPower2,powerRatio1,powerRatio2,crossCorr)  
			pString = "Feature Vector TLV"
			stateString = "V9"
			
		elif dtype == 10:
			lenCount = count
			dataByte = 12 #zone = 12 byte (%:4,power:4,rangeIdx:2,AzmuthIdx:2)
			pString = "Decision Vector TLV"
			stateString = "V10"
			
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
# (pass_fail, v8, v9, v10)
#  pass_fail: True: Data available    False: Data not available
#
#	Output: V8,V9,V10 data:(RAW)")
#	V8 :Range Azimuth Heatmap TLV 
#	V9 :Feature Vector TLV 
#	V10:Decision Vector TLV 
#

	def tlvRead(self,disp):
		#print("---tlvRead---")
		#ds = dos
		typeList = [8,9,10]
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
		
		zone = 0
	
		while True:
			try:
				ch = self.port.read()
			except:
				return (False,v8,v9,v10)
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
					return (False,v8,v9,v10)
		
			elif lstate == 'header':
				sbuf += ch
				idx += 1
				if idx == 24: 
					#print(":".join("{:02x}".format(c) for c in sbuf)) 	 
					#print("len:{:d}".format(len(sbuf))) 
					# [header - Magicword]
					try: 
						(self.hdr.totalPackLen,self.hdr.platform,
						self.hdr.frameNumber,self.hdr.timeCpuCycles,self.hdr.numDetectedObj,
						self.hdr.numTLVs) = struct.unpack('6I', sbuf)
					except:
						if self.dbg == True:
							print("(Header)Improper TLV structure found: ")
						return (False,v8,v9,v10)
					
					if disp == True:  
						self.headerShow()
					
					tlvCount = self.hdr.numTLVs
					if self.hdr.numTLVs == 0:
						return (False,v8,v9,v10)
						
					if self.sm == True:
						print("(Header)")
						
					sbuf = b""
					idx = 0
					lstate = 'TL'
					 
					  
				elif idx > 40:
					print("Header State over 40")
					idx = 0
					sbuf = b""
					lstate = 'idle'
					return (False,v8,v9,v10)
					
			elif lstate == 'TL': #TLV Header type/length
				sbuf += ch
				idx += 1
				if idx == 8:
					#print(":".join("{:02x}".format(c) for c in sbuf))
					try:
						ttype,self.tlvLength = struct.unpack('2I', sbuf)
						#if self.check:
						#	print("(check) numTLVs({:d}): tlvCount({:d})-------ttype:tlvLength:{:d}:{:d}".format(self.hdr.numTLVs,tlvCount,ttype,self.tlvLength))
						if ttype not in typeList or self.tlvLength > 10000:
							if self.dbg == True:
								print("(TL)Improper TL Length(hex):(T){:d} (L){:x} numTLVs:{:d}".format(ttype,self.tlvLength,self.hdr.numTLVs))
							sbuf = b""
							idx = 0
							lstate = 'idle'
							self.port.flushInput()
							return (False,v8,v9,v10)
							
					except:
						if self.dbg == True:
							print("TL unpack Improper Data Found:")
						self.port.flushInput()
						return (False,v8,v9,v10)
					
					lstate,dataBytes,lenCount,pString = self.tlvTypeInfo(ttype,self.tlvLength,disp)
					print()
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
						v8.append(v8s)
						sbuf = b""
					except: 
						if self.dbg == True:
							print("(6.1)Improper Type V8 structure found: ")
						return (False,v8,v9,v10)
					
				if idx == lenCount:
					if disp == True:
						print("v8[{:d}]".format(len(v8)))
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle' 
						if self.sm == True:
							print("(V8:{:d})=>(idle) :true".format(tlvCount))
						return (True,v8,v9,v10)
						
					else: # Go to TL to get others type value
						lstate = 'TL'  
						#print("---------v8 ok ---Goto:TL------{:d}".format(len(v8)))
						if self.sm == True:
							print("(V8:{:d})=>(TL)".format(tlvCount))
					
				elif idx > 10000: #lenCount:
					print("V8 data over:10")
					idx = 0
					sbuf = b""
					lstate = 'idle'
					return (False,v8,v9,v10)
					
			elif lstate == 'V9':
				idx += 1
				sbuf += ch 
				#print("V9: idx({:d} lenCount:{:d} tlvCount({:d}".format(idx,lenCount,tlvCount))
				if (idx%dataBytes == 0):
					#idx = 0
					#avgPower1,avgPower2,powerRatio1,powerRatio1,crossCorr = struct.unpack('5f',sbuf)
					v9s =  struct.unpack('5f',sbuf)
					v9.append(v9s)
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle'
						if self.sm == True:
							print("(V9:{:d})=>(idle) :true".format(tlvCount))
						return (True,v8,v9,v10) #zzzzz
					'''
					else:
						if self.sm == True:
							print("(V9)=>(TL)")
						lstate = 'TL'
					'''
				if idx == lenCount:
					if disp == True:
						print("v9[{:d}]".format(len(v9)))
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle' 
						if self.sm == True:
							print("(V9:{:d})=>(idle) :true".format(tlvCount))
						return (True,v8,v9,v10)
						
					else: # Go to TL to get others type value
						lstate = 'TL'  
						#print("---------v9 ok ---Goto:TL------{:d}".format(len(v9)))
						if self.sm == True:
							print("(V9:{:d})=>(TL)".format(tlvCount))
					
				if idx > lenCount:
					print("************** v9 idx > lenCount ******************  ")
					idx = 0 
					sbuf = b""
					lstate = 'idle'
					
			elif lstate == 'V10':
				idx += 1
				sbuf += ch
				#print("V10:idx={:d}".format(idx))
				#v10.append(ord(ch))
				if idx%dataBytes == 0:
					try:
						#print("V10:lenCount({:d})  idx:{:d}  dataBytes={:d}".format(lenCount,idx,dataBytes))
						#v10.append((percent,power,rangeIdx,azimuthIdx))
						v10s = struct.unpack('2f2H', sbuf)
						v10.append(v10s)
						'''
						print("************* v10s ************ v10.len({:d})".format(len(v10)))
						print(v10s)
						print("************* v10s end *********** ") 
						'''
						sbuf = b""
						if disp == True:
							print("v10[{:d}]".format(len(v10)))
					except:
						print("(V10)Improper Type 10 structure found")
						return (False,v8,v9,v10)
				
				if idx == lenCount:
					idx = 0
					sbuf = b""
					if tlvCount <= 0:
						lstate = 'idle'
						if self.sm == True:
							print("(V10)=>(idle) :true")
						return (True,v8,v9,v10)
					
					'''
					else: # Go to TL to get others type value
						lstate = 'TL'
						idx = 0
						sbuf = b""
						#print("(V10)=>(TL) len={:d}".format(len(v10)))
						if self.sm == True:
							print("(V10)=>(TL)")
					'''
				if idx > lenCount:
					print("V10 data over:lenCount:({:d})".format(lenCount))
					idx = 0 
					lstate = 'idle'
					sbuf = b""
					if self.sm == True:
						print("(V10)=>(idle)")
					return (False,v8,v9,v10)
			

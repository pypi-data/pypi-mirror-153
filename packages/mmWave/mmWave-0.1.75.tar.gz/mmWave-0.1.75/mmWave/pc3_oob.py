# People Counting 3D OOB
# 2022/03/01: alpha
# 
# parsing People Counting 3D + OOB  
# hardware: BM-601 
#     
# company: Joybien Technologies: www.joybien.com
# author: Zach Chen
# v0.0.3
#===========================================
# output: V1,V2,V3,V4,V5,V6,V7 and V9 
# 

import serial
import time
import struct
import pandas as pd
import numpy as np

class header:
	version = 0
	totalPackLen = 0
	platform = 0
	frameNumber = 0
	timeInCPUcycle = 0
	numDetectedObj = 0
	numTLVs = 0
	subframeNumber = 0
	
class statistics:
	interFrameProcessTime = 0.0
	transmitOutTime = 0.0
	interFrameProcessMargin = 0.0
	interChirpProcessMargin = 0.0
	activeFrameCPULoad = 0.0
	interFrameCPULoad = 0.0
	
class temperatureStatistics:
	tempReportValid  = 0
	timeRadarSS  	 = 0
	tmpRx0Sens 		 = 0
	tmpRx1Sens		 = 0
	tmpRx2Sens		 = 0
	tmpRx3Sens		 = 0
	tmpTx0Sens		 = 0
	tmpTx1Sens		 = 0
	tmpTx2Sens		 = 0
	tmpPmSens 		 = 0
	tmpDig0Sens 	 = 0
	tmpDig1Sens 	 = 0
	 
	 
class unitS:
	elevationUnit:float = 0.0
	azimuthUnit : float = 0.0
	dopplerUnit :float = 0.0
	rangeUnit :float = 0.0
	snrUnit :float = 0.0

class Pc3_OOB:
	
	Q9 = 1.0 / 2**9 
	#magicWord =  [b'\x01',b'\x02',b'\x03',b'\x04',b'\x05',b'\x06',b'\x07',b'\x08',b'\0x99']
	magicWord =  [b'\x02',b'\x01',b'\x04',b'\x03',b'\x06',b'\x05',b'\x08',b'\x07',b'\0x99']
	typeList = [1,2,3,4,5,6,7,9] 
	
	v2 = []
	v2df = []
	
	port = ""
	hdr = header
	u = unitS
	ss = statistics
	tss = temperatureStatistics
	
	# provide csv file dataframe
	# real-time 
	v1_col_names_rt = ['fN','type','X','Y','Z','doppler']
	v6_col_names_rt = ['fN','type','iFPT','xOutputT','iFPM','iCPM','aFCpu','iFCpu']
	v9_col_names_rt  = ['fN','type','tRValid','time','tmpRX0','tmpRX1','tmpRX2','tmpRX3','tmpTX0','tmpTX1','tmpTX2','tmpPm','tmpDig0','tmpDig1']
	
	 
	# read from file for trace point clouds
	fileName = ''
	
	sim_startFN = 0
	sim_stopFN  = 0 
	
	# add for interal use
	tlvLength = 0
	numOfPoints = 0
	# for debug use 
	dbg = False #Packet unpacket Check: True show message 
	sm  = False #Observed StateMachine: True Show message
	plen = 16 
	
	def __init__(self,port):
		self.port = port
		print("\n\n\n(jb)mmWave OOB initial")
		print("(jb)version:v0.1.0")
		print("(jb)For Hardware:BM-601/BM-501")
		print("(jb)Hardware: BM601/BM501")
		print("(jb)Firmware:")
		print("(jb)UART Baud Rate:921600")
		print("(jb)Output: V1,V2,V3,V4,V5,V6,V7 & V9 data:(RAW)\n")
		print('v1: Detected Points\t\nv2: Range Profile\t\nv3: Noise Floor Profile\t\nv4: Azimuth Static Heatmap\t\nv5: Range-Doppler Heatmap\t\nv6: Statistics\t\nv7: Side Info for Detected Points\t\nv9: Temperature Statistic')
		
	def useDebug(self,ft):
		self.dbg = ft
		
	def stateMachine(self,ft):
		self.sm = ft
		
	def getHeader(self):
		return self.hdr
		
	
	def headerShow(self):
		print("******* Header ********") 
		print("Version:     \t%x "%(self.hdr.version))
		print("TotalPackLen:\t%d "%(self.hdr.totalPackLen))
		print("Platform:    \t%X "%(self.hdr.platform))
		print("PID(frame#): \t%d "%(self.hdr.frameNumber))
		print("time in CPU cycles:\t{:d} us".format(self.hdr.timeInCPUcycle))
		print("number of Detected object:\t{:d}".format(self.hdr.numDetectedObj))
		print("numTLVs:     \t%d "%(self.hdr.numTLVs))
		print("subframe#  : \t%d "%(self.hdr.subframeNumber))
		print("***End Of Header***") 
			
			
			
	#for class internal use
	def tlvTypeInfo(self,dtype,count,dShow):
		
		sbyte = 8  #tlvHeader Struct = 8 bytes
		unitByte = 20 
		dataByte = 2
		pString = ""
		nString = "numOfPoints :"
		stateString = "V6-unit"
		retCnt = count
		nPoint = 0
		
		if dtype == 1: 
			unitByte = 0  
			dataByte= 16 #point bytes= 16bytes (X(4),Y(4),Z(4),doppler(4))
			pString = "Detected Points"
			stateString = "V1"
			nPoint = count/dataByte
			retCnt = count
			 
		elif dtype == 2: 
			unitByte = 0  
			dataByte= 2 #point bytes= 2bytes 
			pString = "Range Profile"
			stateString = "V2"
			nPoint = count/dataByte
			retCnt = count
			
		elif dtype == 3: 
			unitByte = 0  
			dataByte= 2 #point bytes= 2bytes
			pString = "Noise Floor Profile"
			nString = "1 set data"
			stateString = "V3"
			nPoint = count/dataByte
			retCnt = count
			
		elif dtype == 4: 
			unitByte = 0  
			dataByte= 2 #point bytes= 4bytes
			pString = "Azimuth Static Heatmap"
			nString = "1 set data"
			stateString = "V4"
			nPoint = count/dataByte
			retCnt = count
		
		elif dtype == 5: 
			unitByte = 0  
			dataByte= 2 #point bytes= 2bytes  (Range FFT size) * (Doppler FFT size) * 2 bytes (size of uint16_t)
			pString = "Range-Doppler Heatmap"
			nString = "1 set data"
			stateString = "V5"
			nPoint = count/dataByte
			retCnt = count
			
		elif dtype == 6:
			unitByte = 0   #pointUnit= 0bytes 
			sbyte = 8 	   #tlvHeader Struct = 8 bytes (type(4)/lenth(4))
			dataByte = 24  # 6 * 4 bytes
			pString = "Statistics"
			nString = "1 set data"
			nPoint = count/dataByte
			retCnt = count
			stateString = "V6"
		
		elif dtype == 7:  
			unitByte = 0  #pointUnit= 0
			sbyte = 8      #tlvHeader Struct = 8 bytes (type(4)/lenth(4))
			dataByte= 4    #pointStruct 8bytes:(snr(2),noise(2))
			pString = "Side Info for Detected Points"
			nPoint = count/dataByte
			retCnt = count
			stateString = "V7"
			
		elif dtype == 9: 
			unitByte = 0  
			sbyte = 8 #tlvHeader Struct = 8 bytes (type(4)/lenth(4))
			dataByte= 28 # 28 Bytes
			pString = "Temperature Statistics"
			stateString = "V9"
			nPoint = count/dataByte
			retCnt = count

		else:
			unitByte = 0
			sbyte = 1
			pString = "*** Type Error ***"
			stateString = 'idle'
		 

		#dShow = True
		if dShow == True:
			print("-----[{:}] ----".format(pString))
			print("tlv Type({:2d}Bytes):  \tv{:d}".format(sbyte,dtype))
			print("tlv length:      \t{:d}".format(count)) 
			print("{:}      \t{:d}".format(nString,int(nPoint)))
			print("value length:    \t{:d}".format(retCnt))
			print("StateString= {}".format(stateString))  
		
		return unitByte,stateString, sbyte, dataByte,retCnt, int(nPoint)
		
	def list2df(self,dck,l1,l6,l9):
		ll1 = pd.DataFrame(l1,columns=self.v1_col_names_rt)
		ll6 = pd.DataFrame(l6,columns=self.v6_col_names_rt) 
		ll9 = pd.DataFrame(l9,columns=self.v9_col_names_rt) 
		 
		return (dck,ll1,ll6,ll9)

	
#
# TLV: Type-Length-Value
# read TLV data
# Usuage:
# (dck,v1,v6,v9)  = radar.tlvRead(True,df = 'DataFrame')
# input:
#     disp: True:print message
#	  False: hide printing message
#  
# output:(return parameter)
# (pass_fail, v1, v6 & V9)
#  pass_fail: True: Data available    False: Data not available
#  v1: Detected Points
#  v2: Range Profile
#  v3: Noise Floor Profile
#  v4: Azimuth Static Heatmap
#  v5: Range-Doppler Heatmap
#  v6: Statistics
#  v7: Side Info for Detected Points
#  v8: Azimuth/Elevation Static Heatmap
#  v9: Temperature Statistic
#   
	def tlvRead(self,disp,df = None):
		
		
		idx = 0
		lstate = 'idle'
		sbuf = b""
		lenCount = 0
		unitByteCount = 0
		escapeCount = 0
		dataBytes = 0
		numOfPoints = 0
		tlvCount = 0
		pbyte = 16
		v1 = ([])
		self.v2 = ([])
		v3 = ([])
		v4 = ([])
		v5 = ([])
		v6 = ([])
		v7 = ([])
		v9 = ([])
		
		v1df = ([])
		self.v2df = ([])
		v3df = ([])
		v4df = ([])
		v5df = ([])
		v6df = ([])
		v7df = ([])
		v9df = ([])
		 
		
		while True:
			try:
				ch = self.port.read()
			except:
				return self.list2df(False,v1df,v6df,v9df) if (df == 'DataFrame') else (False,v1,v6,v9)
				
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
						self.escapeCount = 0
				else:
					#print("not: magicWord state:")
					idx = 0
					rangeProfile = b""
					return self.list2df(False,v1df,v6df,v9df) if (df == 'DataFrame') else (False,v1,v6,v9)
		
			elif lstate == 'header':
				sbuf += ch
				idx += 1
				escapeCount += 1
				if idx == 32: 
					#print("------header-----")
					#print(":".join("{:02x}".format(c) for c in sbuf)) 	 
					#print("len:{:d}".format(len(sbuf))) 
					# [header - Magicword]
					
					try: 
						(self.hdr.version,self.hdr.totalPackLen,
						self.hdr.platform,self.hdr.frameNumber,
						self.hdr.timeInCPUcycle,self.hdr.numDetectedObj,
						self.hdr.numTLVs,self.hdr.subframeNumber) = struct.unpack('8I', sbuf)
						self.frameNumber = self.hdr.frameNumber
					except:
						if self.dbg == True:
							print("(Header)Improper TLV structure found: ")
						return self.list2df(False,v1df,v6df,v9df) if (df == 'DataFrame') else (False,v1,v6,v9)
					
					if disp == True:  
						self.headerShow()
					
					tlvCount = self.hdr.numTLVs
					#print("tlvCount:{:}".format(tlvCount))
					if self.hdr.numTLVs == 0:
						return self.list2df(True,v1df,v6df,v9df) if (df == 'DataFrame') else (True,v1,v6,v9)
						
					if self.sm == True:
						print("(Header)")
						
					sbuf = b""
					idx = 0
					lstate = 'TL'
					  
				elif idx > 64: #44
					idx = 0
					sbuf = b''
					lstate = 'idle'
					return self.list2df(False,v1df,v6df,v9df) if (df == 'DataFrame') else (False,v1,v6,v9)
					
			elif lstate == 'TL': #TLV Header type/length
				sbuf += ch
				idx += 1
				self.escapeCount += 1
				
				if idx == 8:
					#print(":".join("{:02x}".format(c) for c in sbuf))
					try:
						ttype,self.tlvLength = struct.unpack('2I', sbuf)
						if self.dbg == True:
							print("(TL)--tlvNum:{:d}: tlvCount({:d})-------ttype:tlvLength:{:d}:{:d}".format(self.hdr.numTLVs,tlvCount,ttype,self.tlvLength))
						if ttype not in self.typeList or self.tlvLength > 20000:
							if self.dbg == True:
								print("(TL)Improper TL Length(hex):(T){:d} (L){:x} numTLVs:{:d}".format(ttype,self.tlvLength,self.hdr.numTLVs))
							sbuf = b""
							idx = 0
							lstate = 'idle'
							self.port.flushInput()
							return self.list2df(False,v1df,v6df,v9df) if (df == 'DataFrame') else (False,v1,v6,v9)
							
					except:
						if self.dbg == True:
							print("TL unpack Improper Data Found:")
						self.port.flushInput()
						return self.list2df(False,v1df,v6df,v9df) if (df == 'DataFrame') else (False,v1,v6,v9)
						
					
						
					unitByteCount,lstate ,plen ,dataBytes,lenCount, numOfPoints = self.tlvTypeInfo(ttype,self.tlvLength,disp)
					if self.dbg == True:
						print("unitByteCount={}  lstate ={} , bytes(type+len)={} dataBytes= {} lenCount ={} numOfPoint={}".format(unitByteCount,lstate ,plen ,dataBytes,lenCount, numOfPoints))
					#if ttype == 10:
					#	print("--pointCloud:((tlvLength({:d})-pointUnit(20)-tlvStruct(8))/8={:d}".format(self.tlvLength,numOfPoints))
					if self.sm == True:
						print("(TL:tlvCount:{:d})=>({:})".format(tlvCount,lstate))
					
					tlvCount -= 1
					#print("(TL->type:{:})--tlvNum:{:d}: tlvCount({:d})".format(ttype,self.hdr.numTLVs,tlvCount))
					idx = 0  
					sbuf = b""
					
					if ttype == 1 and self.tlvLength == 0 and tlvCount != 0:
						if self.dbg == True:
							print("========type=1 lenth = 0 ===========================================")
						idx = 0
						lstate = 'idle'
						
					if self.escapeCount > self.hdr.totalPackLen:
						if self.dbg == True:
							print("(ESC)========type={:} ========self.escapeCount > self.hdr.totoalPackLen==============================".format(lstate))
						idx = 0
						sbuf = b''
						lstate = 'idle'
					
			elif lstate == 'V1':
				sbuf += ch
				idx += 1
				self.escapeCount += 1
				if (idx%dataBytes == 0):
					try:
						#print(":".join("{:02x}".format(c) for c in sbuf))
						(x,y,z,d) = struct.unpack('4f', sbuf)
						if self.dbg == True:
							print("({:2d}:{:4d})(idx:({:4d}) x:{:.4f} y:{:.4f} z:{:.4f} d:{:.4f}".format(numOfPoints,lenCount,idx,x,y,z,d))
						
						if (df == 'DataFrame'):
							v1df.append((self.hdr.frameNumber,'v1',x,y,z,d)) 
						else:
							v1.append((x,y,z,d))
						
						#print("point_cloud_2d.append:[{:d}]".format(len(point_cloud_2d)))
						sbuf = b""
						
					except:
						if self.dbg == True:
							print("(6.1)Improper Type 1 Value structure found: ")
						
						return self.list2df(False,v1df,v6df,v9df) if (df == 'DataFrame') else (False,v1,v6,v9)
				
				if idx == lenCount:
					if disp == True:
						print("v1[{:d}]".format(len(v1)))
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle'
						if self.sm == True:
							print("(V1:{:d})=>(idle) :true".format(tlvCount))
						
						return self.list2df(True,v1df,v6df,v9df) if (df == 'DataFrame') else (True,v1,v6,v9)
						
					else: # Go to TL to get others type value
						lstate = 'TL'
						if self.sm == True:
							print("(V1:{:d})=>(TL)".format(tlvCount))
					
				elif idx > lenCount or self.escapeCount > self.hdr.totalPackLen:
					idx = 0
					sbuf = b""
					lstate = 'idle'
					return self.list2df(False,v1df,v6df,v9df) if (df == 'DataFrame') else (False,v1,v6,v9)
				
				
			
			elif lstate == 'V2' or lstate == 'V3' or lstate == 'V4' or lstate == 'V5' or lstate == 'V6' or lstate == 'V9':
				sbuf += ch
				idx += 1
				self.escapeCount += 1
				#if (idx%dataBytes == 0):
				
				if lenCount == 0:
					idx = 0
					sbuf = b""
					lstate = 'idle'
					return self.list2df(False,v1df,v6df,v9df) if (df == 'DataFrame') else (False,v1,v6,v9)
				
				if (idx%lenCount == 0):
					try:
						#print(":".join("{:02x}".format(c) for c in sbuf))
						if lstate == 'V2':
							rp = struct.unpack('256H', sbuf)
							rpf = [float(i) * self.Q9 for i in rp] 
							#print("V2:(Range Profile) (points:{:2d}:lenCount:{:4d})(idx:({:4d}) len(rpf)= {:}".format(numOfPoints,lenCount,idx,len(rpf)))
							self.v2 = rpf
							'''
							self.v2.append(rpf)
							
							if (df == 'DataFrame'):
								self.v2df.append((self.hdr.frameNumber,'v2',rpf)) 
							else:
								self.v2 = rpf
							'''
						elif lstate == 'V3':
							nf = struct.unpack('256H', sbuf)
							nff = [float(i) * self.Q9 for i in nf] 
							#print("V3:(Noise Floor Profile ({:2d}:{:4d})(idx:({:4d}) len(nff)= {:}".format(numOfPoints,lenCount,idx,len(nff)))
							 
							if (df == 'DataFrame'):
								v3df.append((self.hdr.frameNumber,'v3',nff)) 
							else:
								v3.append(nff)
						elif lstate == 'V4':
							ash = struct.unpack('4096h', sbuf)
							if self.dbg == True:
								print("V4:(Azimuth Static HeatMap ({:2d}:{:4d})(idx:({:4d}) len(azimuth-static ash)= {:}".format(numOfPoints,lenCount,idx,len(ash)))
							if (df == 'DataFrame'):
								v4df.append((self.hdr.frameNumber,'v4',ash)) 
							else:
								v4.append(ash)
								
						elif lstate == 'V5':
							rdh = struct.unpack('4096h', sbuf)
							rdhf = [float(i) * self.Q9 for i in rdh]
							if self.dbg == True: 
								print("V5:(Range-Doppler HeatMap ({:2d}:{:4d})(idx:({:4d}) len(range-doppler rd)= {:}".format(numOfPoints,lenCount,idx,len(rdhf)))
							#print(rdhf)
							if (df == 'DataFrame'):
								v5df.append((self.hdr.frameNumber,'v5',rdhf)) 
							else:
								v5.append(rdh)
								
						elif lstate == 'V6':
							#print("V6----lenCount:{:}".format(lenCount)) 
							
							(self.ss.interFrameProcessTime,  self.ss.transmitOutTime,
							self.ss.interFrameProcessMargin,self.ss.interChirpProcessMargin,
							self.ss.activeFrameCPULoad,      self.ss.interFrameProcessTime) = struct.unpack('6I', sbuf)
							#print("v6 usec:{:}".format(self.ss.interFrameProcessTime)) 
							
							if (df == 'DataFrame'):
								v6df.append((self.hdr.frameNumber,'v6',self.ss.interFrameProcessTime,  
								self.ss.transmitOutTime, self.ss.interFrameProcessMargin,
								self.ss.interChirpProcessMargin, self.ss.activeFrameCPULoad, self.ss.interFrameProcessTime) )
							else:
								v6.append((self.ss.interFrameProcessTime,  
								self.ss.transmitOutTime, self.ss.interFrameProcessMargin,
								self.ss.interChirpProcessMargin, self.ss.activeFrameCPULoad, self.ss.interFrameProcessTime))
						
						elif lstate == 'V9':
							#print("V9----lenCount:{:}".format(lenCount)) 
							
							(self.tss.tempReportValid,self.tss.timeRadarSS,
							self.tss.tmpRx0Sens,self.tss.tmpRx1Sens,self.tss.tmpRx2Sens,self.tss.tmpRx3Sens,
							self.tss.tmpTx0Sens,self.tss.tmpTx1Sens,self.tss.tmpTx2Sens,
							self.tss.tmpPmSens,
							self.tss.tmpDig0Sens,self.tss.tmpDig1Sens ) = struct.unpack('2I10H', sbuf)
							
							if (df == 'DataFrame'):
								v9df.append((self.hdr.frameNumber,'v9',self.tss.tempReportValid,self.tss.timeRadarSS,
								self.tss.tmpRx0Sens,self.tss.tmpRx1Sens,self.tss.tmpRx2Sens,self.tss.tmpRx3Sens,
								self.tss.tmpTx0Sens,self.tss.tmpTx1Sens,self.tss.tmpTx2Sens,
								self.tss.tmpPmSens,
								self.tss.tmpDig0Sens,self.tss.tmpDig1Sens )) 
							else:
								v9.append((self.tss.tempReportValid,self.tss.timeRadarSS,
								self.tss.tmpRx0Sens,self.tss.tmpRx1Sens,self.tss.tmpRx2Sens,self.tss.tmpRx3Sens,
								self.tss.tmpTx0Sens,self.tss.tmpTx1Sens,self.tss.tmpTx2Sens,
								self.tss.tmpPmSens,
								self.tss.tmpDig0Sens,self.tss.tmpDig1Sens))
								
							
							
						
						#print("point_cloud_2d.append:[{:d}]".format(len(point_cloud_2d)))
						sbuf = b""
						#lstate = 'TL'
						
					except:
						if self.dbg == True:
							print("Improper Type {} Value structure found: ".format(lstate))
						return self.list2df(False,v1df,v6df,v9df) if (df == 'DataFrame') else (False,v1,v6,v9)
				
				if idx == lenCount:
					'''
					if disp == True:
						if lstate == 'V2':
							print("v2[{:d}]".format(len(v2)))
						else:
							print("v3[{:d}]".format(len(v3)))
					'''
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						if self.sm == True:
							print("({}:tlvCount({:d})) lenCount:{}=>(idle)".format(lstate,tlvCount,lenCount))
						lstate = 'idle'
						
						return self.list2df(True,v1df,v6df,v9df) if (df == 'DataFrame') else (True,v1,v6,v9)
						
					else: # Go to TL to get others type value
						if self.sm == True:
							print("({}:tlvCount({:d})) lenCount:{}=>(TL)".format(lstate,tlvCount,lenCount))
						lstate = 'TL'
											
				elif idx > lenCount or self.escapeCount > self.hdr.totalPackLen:
					print("(ESC)========type={:} lenth = 0 =============self.escapeCount > self.hdr.totoalPackLen==============================".format(lstate))
					idx = 0
					sbuf = b""
					lstate = 'idle'
					return self.list2df(False,v1df,v6df,v9df) if (df == 'DataFrame') else (False,v1,v6,v9)
				
					
			elif lstate == 'V7': 
				sbuf += ch
				idx += 1
				self.escapeCount += 1
				if (idx%dataBytes == 0):
					try:
						#print(":".join("{:02x}".format(c) for c in sbuf))
						(snr,noise) = struct.unpack('2H', sbuf)
						v7.append((snr,noise))
						sbuf = b""
						
					except:
						if self.dbg == True:
							print("(6.1)Improper Type 6 Value structure found: ")
						
						return self.list2df(False,v1df,v6df,v9df) if (df == 'DataFrame') else (False,v1,v6,v9)
					
				if idx == lenCount:
					if disp == True:
						print("v7[len:{:d}]".format(len(v7)))
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle'
						if self.sm == True:
							print("(V7:{:d})=>(idle) :true".format(tlvCount))
						
						return self.list2df(True,v1df,v6df,v9df) if (df == 'DataFrame') else (True,v1,v6,v9)
						
					else: # Go to TL to get others type value
						lstate = 'TL'
						if self.sm == True:
							print("(V7:{:d})=>(TL)".format(tlvCount))
							
					
				elif idx > lenCount or self.escapeCount > self.hdr.totalPackLen:
					print("(ESC)========type={:} lenth = 0 =============self.escapeCount > self.hdr.totoalPackLen==============================".format(lstate))
					idx = 0
					sbuf = b""
					lstate = 'idle'
					return self.list2df(False,v1df,v6df,v9df) if (df == 'DataFrame') else (False,v1,v6,v9)
					
		
				
	def v67Simlog(frameNum):
		global sim_startFN,sim_stopFN
		s_fn = frameNum + sim_startFN
		#print("frame number:{:}".format(s_fn))
		v6d = v6sim[v6sim['fN'] == s_fn]
		#v6d =  v6dd[v6dd['doppler'] < 0.0]
		#print(v6d)
		v7d = v7sim[v7sim['fN'] == s_fn]
		chk = 0
		if v6d.count != 0:
			chk = 1
		return (chk,v6d,v7d)
		
	def getRecordData(self,frameNum):
		s_fn = frameNum + self.sim_startFN
		#print("frame number:{:}".format(s_fn))
		v6d = self.v6simo[self.v6simo['fN'] == s_fn]
		#v6d =  v6dd[v6dd['doppler'] < 0.0]
		#print(v6d)
		v7d = self.v7simo[self.v7simo['fN'] == s_fn]
		v8d = self.v8simo[self.v8simo['fN'] == s_fn]
		chk = 0
		if v6d.count != 0:
			chk = 1
		return (chk,v6d,v7d,v8d)
		
	def readFile(self,fileName):
		#fileName = "pc32021-03-19-10-02-17.csv"  
		#df = pd.read_csv(fileName, error_bad_lines=False, warn_bad_lines=False) 
		self.fileName = fileName 
		#          ['time','fN','type','elv','azimuth','range' ,'doppler','snr','sx', 'sy', 'sz']
		df = pd.read_csv(self.fileName, names = self.v6_col_names, skiprows = [0,11,12]) 
		df.dropna()
		#print("------------------- df --------------------shape:{:}".format(df.shape))
		print(df.info())
		print(df.info(memory_usage="deep")) 
		
		v6simOri = df[(df.type == 'v6')]
		#print("-------------------v6sim------------:{:}".format(v6simOri.shape))
		#self.v6simo = v6simOri.loc[:,['fN','elv','azimuth','range','doppler','snr']]
		self.v6simo = v6simOri.loc[:,['fN','type','elv','azimuth','range' ,'doppler','snr','sx', 'sy', 'sz']]
		self.v6simo['elv'] = self.v6simo['elv'].astype(float, errors = 'raise') 
		
		df7 = pd.read_csv(self.fileName, names = self.v7_col_names, skiprows = [0])  
		
		v7simc = df7[df7['type'] == 'v7']
		self.v7simo  = v7simc.loc[:,['fN','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','ec0','ec1','ec2','ec3','ec4','ec5','ec6','ec7','ec8','ec9','ec10','ec11','ec12','ec13','ec14','ec15','g','confi','tid']]
		self.sim_startFN = df['fN'].values[0]
		self.sim_stopFN  = df['fN'].values[-1]
		'''
		print("---------start frame number---------:{:}".format(self.sim_startFN))
		print("---------stop  frame number---------:{:}".format(self.sim_stopFN))
		print(self.v7simo)
		print("-----v8sim data lib-----")
		'''
		v8simc = df[df['type'] == 'v8']
		self.v8simo  = v8simc.loc[:,['fN','type','elv']]
		self.v8simo.columns = ['fN','type','targetID']
		#print(self.v8simo)
		return (self.v6simo,self.v7simo,self.v8simo)



# People Counting 3D + VSD   
# 2022/02/15: alpha
# 2022/03/10: beta
# v0.0.1
# parsing People Counting 3D + VSD data use AOP 
# hardware: BM-501 AOP
#     
# company: Joybien Technologies: www.joybien.com
# author: Zach Chen
#===========================================
# output: V6,V7,V8,V10,V12 Raw data
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

class vsos:
	unwrapped_waveform  = [float(0.0)] * 2 
	heart_waveform 		= [float(0.0)] * 2
	breathing_waveform  = [float(0.0)] * 2
	heart_rate 			= [float(0.0)] * 2
	breathing_rate		= [float(0.0)] * 2
	x                   = [float(0.0)] * 2
	y                   = [float(0.0)] * 2
	z                   = [float(0.0)] * 2
	tid					= [float(0.0)] * 2
	rangeTarget			= [float(0.0)] * 2
	angle				= [float(0.0)] * 2 
	rangeIdx			= [int(0)] * 2
	angleIdx			= [int(0)] * 2
	wave				= [float(0.0)] * 200

class Pc3_VSD:
	
	 
	magicWord =  [b'\x01',b'\x02',b'\x03',b'\x04',b'\x05',b'\x06',b'\x07',b'\x08',b'\0x99']
	port = ""
	hdr = header
	u = unitS
	vs = vsos()
	
	# provide csv file dataframe
	# real-time 
	v6_col_names_rt = ['fN','type','elv','azimuth','range','doppler','snr','sx', 'sy', 'sz'] 
	v7_col_names_rt = ['fN','type','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','ec0','ec1','ec2','ec3','ec4','ec5','ec6','ec7','ec8','ec9','ec10','ec11','ec12','ec13','ec14','ec15','g','confi','tid']
	v8_col_names_rt = ['fN','type','targetID']
	
	# read from file for trace point clouds
	fileName = ''
	v6_col_names = ['time','fN','type','elv','azimuth','range','doppler','snr','sx', 'sy', 'sz']
	#v7_col_names = ['time','fN','type','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','ec0','ec1','ec2','ec3','ec4','ec5','ec6','ec7','ec8','ec9','ec10','ec11','ec12','ec13','ec14','ec15','g','confi','tid']
	v7_col_names = ['time','fN','type','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','tid','ec0','ec1','ec2','ec3','ec4','ec5','ec6','ec7','ec8','ec9','ec10','ec11','ec12','ec13','ec14','ec15','g','confi'] #v0.1.2
	v8_col_names = ['time','fN','type','targetID']
	
	sim_startFN = 0
	sim_stopFN  = 0 
	
	# add for interal use
	tlvLength = 0
	numOfPoints = 0
	# for debug use 
	dbg = False #Packet unpacket Check: True show message 
	sm  = False #Observed StateMachine: True Show message
	plen = 16 
	vitalSign_len = (8 * 11 + 2 * 4)
	def __init__(self,port):
		self.port = port
		print("\n\n\n(jb)People Counting 3D + VSD initial")
		print("(jb)vsersion:v0.1.0")
		print("(jb)For Hardware:BM-501 (AOP)")
		print("(jb)Hardware: BM501-AOP")
		print("(jb)Firmware:")
		print("(jb)UART Baud Rate:921600")
		print("(jb)Output: V6,V7,V8,V10 & V12 data:(RAW)\n\n\n\n")
		
	def useDebug(self,ft):
		self.dbg = ft
		
	def stateMachine(self,ft):
		self.sm = ft
		
	def getHeader(self):
		return self.hdr
		
	def headerShow(self):
		print("******* Header ********") 
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
			unitByte = 20  #pointUnit= 20bytes (elvUnit(4),aziUnit(4),dopplerUnit(4),rangeUnit(4),snrUnit(4))
			unitByte = 20  #pointUnit= 20bytes (elvUnit(4),aziUnit(4),dopplerUnit(4),rangeUnit(4),snrUnit(4))
			sbyte = 8      #tlvHeader Struct = 8 bytes (type(4)/lenth(4))
			dataByte= 8    #pointStruct 8bytes:(elevation(1),azimuth(1),doppler(2),range(2),snr(2))
			pString = "Point Cloud TLV and pointUnit"
			 
		elif dtype == 7:
			unitByte = 0   #pointUnit= 0bytes 
			sbyte = 8 	   #tlvHeader Struct = 8 bytes (type(4)/lenth(4))
			dataByte = 112  #target struct 112 bytes:(tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ,ec0,ec1,ec2,ec3,ec4,ec5,ec6,ec7,ec8,ec9,ec10,ec11,ec12,ec13,ec14,ec15,g,confi)  
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
		elif dtype == 10:
			unitByte = 0   #pointUnit= 0bytes 
			sbyte = 8    #tlvHeader Struct = 8 bytes
			dataByte =  2802 - 8  #(674 * 4 + 96 + 2 )  #896 # (11 * 4 * 2) + ((2 * 2) * 2) + 4 * 674 = 88 + 8 + 800 = 896 
			pString = "Vital Sign Info"
			nString = "Vital Sign Info"
			stateString = "V10"
		
		elif dtype == 12: #12
			unitByte = 0   #pointUnit= 0bytes 
			sbyte = 8    #tlvHeader Struct = 8 bytes
			dataByte = 4 #
			pString = "Presence Indication TLV"
			nString = "Presence Indication TLV"
			stateString = "V12"
		else:
			unitByte = 0
			sbyte = 1
			pString = "*** Type Error ***"
			stateString = 'idle'
		 
		retCnt = count - unitByte -sbyte
		dataByte = 1 if dataByte == 0 else dataByte
		nPoint = retCnt / dataByte #sbyte
		#dShow = True
		if dShow == True:
			print("-----[{:}] ----".format(pString))
			print("tlv Type({:2d}Bytes):  \tv{:d}".format(sbyte,dtype))
			print("tlv length:      \t{:d}".format(count)) 
			print("{:}      \t{:d}".format(nString,int(nPoint)))
			print("value length:    \t{:d}".format(retCnt))  
		
		return unitByte,stateString, sbyte, dataByte,retCnt, int(nPoint)
		
	def list2df(self,dck,l6,l7,l8,l10,l12):
		ll6 = pd.DataFrame(l6,columns=self.v6_col_names_rt)
		ll7 = pd.DataFrame(l7,columns=self.v7_col_names_rt)
		ll8 = l8 #pd.DataFrame(l8,columns=self.v8_col_names_rt)
		ll10 = l10
		ll12 = l12
		return (dck,ll6,ll7,ll8,ll10,ll12)


#
# TLV: Type-Length-Value
# read TLV data
# input:
#     disp: True:print message
#			False: hide printing message
#     df: 
# output:(return parameter)
# (pass_fail, v6, v7, v8, V10 & V12)
#  pass_fail: True: Data available    False: Data not available
#  v6: point cloud infomation
#  v7: Target Object information
#  v8: Target Index information
#  v10: Vital Sign information
#  v12: Presence Indication information
#  
# 
	def tlvRead(self,disp,df = None):
		
		typeList = [6,7,8,10,12]
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
		v10 = ([])
		v12 = ([])
		v6df = ([])
		v7df = ([])
		v8df = ([])
		v10df = ([])
		v12df = ([])
		
		while True:
			try:
				ch = self.port.read()
			except:
				return self.list2df(False,v6df,v7df,v8df,v10df,v12df) if (df == 'DataFrame') else (False,v6,v7,v8,v10,v12)
				
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
					return self.list2df(False,v6df,v7df,v8df,v10df,v12df) if (df == 'DataFrame') else (False,v6,v7,v8,v10,v12)
		
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
						self.frameNumber = self.hdr.frameNumber
					except:
						if self.dbg == True:
							print("(Header)Improper TLV structure found: ")
						return self.list2df(False,v6df,v7df,v8df,v10df,v12df) if (df == 'DataFrame') else (False,v6,v7,v8,v10,v12)
					
					if disp == True:  
						self.headerShow()
					
					tlvCount = self.hdr.numTLVs
					#print("tlvCount:{:}".format(tlvCount))
					if self.hdr.numTLVs == 0:
						return self.list2df(True,v6df,v7df,v8df,v10df,v12df) if (df == 'DataFrame') else (True,v6,v7,v8,v10,v12)
						
					if self.sm == True:
						print("(Header)")
						
					sbuf = b""
					idx = 0
					lstate = 'TL'
					  
				elif idx > 44:
					idx = 0
					lstate = 'idle'
					return self.list2df(False,v6df,v7df,v8df,v10df,v12df) if (df == 'DataFrame') else (False,v6,v7,v8,v10,v12)
					
			elif lstate == 'TL': #TLV Header type/length
				sbuf += ch
				idx += 1
				if idx == 8:
					#print(":".join("{:02x}".format(c) for c in sbuf))
					try:
						ttype,self.tlvLength = struct.unpack('2I', sbuf)
						#print("(TL)--tlvNum:{:d}: tlvCount({:d})-------ttype:tlvLength:{:d}:{:d}".format(self.hdr.numTLVs,tlvCount,ttype,self.tlvLength))
						if ttype not in typeList or self.tlvLength > 10000:
							if self.dbg == True:
								print("(TL)Improper TL Length(hex):(T){:d} (L){:x} numTLVs:{:d}".format(ttype,self.tlvLength,self.hdr.numTLVs))
							sbuf = b""
							idx = 0
							lstate = 'idle'
							self.port.flushInput()
							return self.list2df(False,v6df,v7df,v8df,v10df,v12df) if (df == 'DataFrame') else (False,v6,v7,v8,v10,v12)
							
					except:
						if self.dbg == True:
							print("TL unpack Improper Data Found:")
						self.port.flushInput()
						return self.list2df(False,v6df,v7df,v8df,v10df,v12df) if (df == 'DataFrame') else (False,v6,v7,v8,v10,v12)
					
					unitByteCount,lstate ,plen ,dataBytes,lenCount, numOfPoints = self.tlvTypeInfo(ttype,self.tlvLength,disp)
					#if ttype == 10:
					#	print("--pointCloud:((tlvLength({:d})-pointUnit(20)-tlvStruct(8))/8={:d}".format(self.tlvLength,numOfPoints))
					if self.sm == True:
						print("(TL:{:d})=>({:})".format(tlvCount,lstate))
					
					tlvCount -= 1
					#print("(TL->type:{:})--tlvNum:{:d}: tlvCount({:d})".format(ttype,self.hdr.numTLVs,tlvCount))
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
						
						return self.list2df(False,v6df,v7df,v8df,v10df,v12df) if (df == 'DataFrame') else (False,v6,v7,v8,v10,v12)
					
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
						
						if (df == 'DataFrame'):
							sz  = ran * np.sin(elv)
							sx  = ran * np.cos(elv) * np.sin(azi)
							sy  = ran * np.cos(elv) * np.cos(azi)
							v6df.append((self.hdr.frameNumber,'v6',elv,azi,ran,dop,snr,sx,sy,sz)) #v0.1.1
							 
						else:
							v6.append((elv,azi,dop,ran,snr))
						
						#print("point_cloud_2d.append:[{:d}]".format(len(point_cloud_2d)))
						sbuf = b""
						
					except:
						if self.dbg == True:
							print("(6.1)Improper Type 6 Value structure found: ")
						
						return self.list2df(False,v6df,v7df,v8df,v10df,v12df) if (df == 'DataFrame') else (False,v6,v7,v8,v10,v12)
					
				if idx == lenCount:
					if disp == True:
						print("v6[{:d}]".format(len(v6)))
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle'
						if self.sm == True:
							print("(V6:{:d})=>(idle) :true".format(tlvCount))
						
						return self.list2df(True,v6df,v7df,v8df,v10df,v12df) if (df == 'DataFrame') else (True,v6,v7,v8,v10,v12)
						
					else: # Go to TL to get others type value
						lstate = 'TL'
						if self.sm == True:
							print("(V6:{:d})=>(TL)".format(tlvCount))
					
				elif idx > lenCount:
					idx = 0
					sbuf = b""
					lstate = 'idle'
					return self.list2df(False,v6df,v7df,v8df,v10df,v12df) if (df == 'DataFrame') else (False,v6,v7,v8,v10,v12)
				
			elif lstate == 'V7':
				sbuf += ch
				idx += 1
				if (idx%dataBytes == 0):
					#print("V7:dataBytes({:d}) lenCount({:d}) index:{:d}".format(dataBytes,lenCount,idx))
					try:
						#(tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ) = struct.unpack('I9f', sbuf)
						(tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ,ec0,ec1,ec2,ec3,ec4,ec5,ec6,ec7,ec8,ec9,ec10,ec11,ec12,ec13,ec14,ec15,g,confi) = struct.unpack('I27f', sbuf)
						
						if (df == 'DataFrame'): 
							v7df.append((self.hdr.frameNumber,'v7',posX,posY,posZ,velX,velY,velZ,accX,accY,accZ,ec0,ec1,ec2,ec3,ec4,ec5,ec6,ec7,ec8,ec9,ec10,ec11,ec12,ec13,ec14,ec15,g,confi,tid))
							
						else:
							v7.append((tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ,ec0,ec1,ec2,ec3,ec4,ec5,ec6,ec7,ec8,ec9,ec10,ec11,ec12,ec13,ec14,ec15,g,confi))
						
						sbuf = b""
					except:
						if self.dbg == True:
							print("(7)Improper Type 7 Value structure found: ")
						
						return self.list2df(False,v6df,v7df,v8df,v10df,v12df) if (df == 'DataFrame') else (False,v6,v7,v8,v10,v12)
						
				if idx >= lenCount:
					if disp == True:
						print("v7[{:d}]".format(len(v7)))
					 
					sbuf = b""
					if tlvCount == 0:
						lstate = 'idle'
						if self.sm == True:
							print("(V7)=>(idle) :true")
						
						return self.list2df(True,v6df,v7df,v8df,v10df,v12df) if (df == 'DataFrame') else (True,v6,v7,v8,v10,v12)
						
					else: # Go to TL to get others type value
						lstate = 'TL'
						idx = 0
						if self.sm == True:
							print("(V7)=>(TL)")

				if idx > lenCount:
					idx = 0 
					lstate = 'idle'
					sbuf = b""
					
					return self.list2df(False,v6df,v7df,v8df,v10df,v12df) if (df == 'DataFrame') else (False,v6,v7,v8,v10,v12)
				
			elif lstate == 'V8':
				idx += 1
				v8.append(ord(ch))
				
				if idx == lenCount:
					if disp == True:
						print("(V8)=>(idle)")
					sbuf = b""
					
					if (df == 'DataFrame'):
						v8df = [self.hdr.frameNumber,'v8']
						v8df.extend(v8)
						
					if tlvCount == 0:
						sbuf = b''
						idx = 0
						lstate = 'idle'
						if self.sm == True:
							print("(V7)=>(idle)")
						return self.list2df(True,v6df,v7df,v8df,v10df,v12df) if (df == 'DataFrame') else (True,v6,v7,v8,v10,v12)
					else:
						sbuf = b""
						idx = 0
						lstate = 'TL'
						if self.sm == True:
							print("(V8)=>(TL)")
						 
					
				if idx > lenCount:
					idx = 0 
					lstate = 'idle'
					sbuf = b""
					
					
			elif lstate == 'V10':
					
				sbuf += ch
				idx += 1
				if (idx%dataBytes == 0):
					#print("V10============================+++++++++++++++++")
					#print("V10:dataBytes({:d}) lenCount({:d}) index:{:d}".format(dataBytes,lenCount,idx))
					try:
						pdata = sbuf[0:self.vitalSign_len]  # 96 = (8 * 11 + 2 * 4)
						#print("pdata len({:}) pdata={:}\n\n".format(len(pdata),pdata))
						temp = struct.unpack('22f4h', pdata)
						vsdic = {}
						for i in range(0,2):
							self.vs.unwrapped_waveform[i] 	=  temp[i+0] 
							self.vs.heart_waveform[i]     	=  temp[i+2]
							self.vs.breathing_waveform[i]  	=  temp[i+4] 
							self.vs.heart_rate[i] 			=  temp[i+6]  
							self.vs.breathing_rate[i]		=  temp[i+8] 
							self.vs.x[i]                   	=  temp[i+10] 
							self.vs.y[i]                   	=  temp[i+12] 
							self.vs.z[i]                  	=  temp[i+14] 
							self.vs.tid[i]					=  temp[i+16] 
							self.vs.rangeTarget[i]			=  temp[i+18] 
							self.vs.angle[i]				=  temp[i+20] 
							self.vs.rangeIdx[i]				=  temp[i+22] 
							self.vs.angleIdx[i]				=  temp[i+24] 
						
						vsdic['fN']   = self.hdr.frameNumber
						vsdic['type'] = 'v10'
						vsdic['uww']  = self.vs.unwrapped_waveform
						vsdic['hw']   = self.vs.heart_waveform
						vsdic['bw']   = self.vs.breathing_waveform
						vsdic['hr']   = self.vs.heart_rate
						vsdic['br']   = self.vs.breathing_rate
						vsdic['x'] 	  = self.vs.x
						vsdic['y']    = self.vs.y
						vsdic['z']    = self.vs.z
						vsdic['tid']  = self.vs.tid
						vsdic['rangeT']   = self.vs.rangeTarget
						vsdic['angle']    = self.vs.angle
						vsdic['rangeIdx'] = self.vs.rangeIdx
						vsdic['angleIdx'] = self.vs.angleIdx
						
						pdata = sbuf[self.vitalSign_len: -2] #forget CRC 2 bytes
						fmt = '{:}f'.format(int(len(pdata) / 4))
						#print("dataLenth:{:} format:{:}".format(len(pdata),fmt))
						wave = struct.unpack(fmt, pdata)
						vsdic['wave'] = wave
						
						pd.options.display.float_format = '{:,.2f}'.format
						v10df = vsdic    #pd.DataFrame([vsdic])
						v10   = vsdic
						
						sbuf = b""
					except:
						print("(7)Improper Type 10 Value structure found: ")
						if self.dbg == True:
							print("(7)Improper Type 10 Value structure found: ")
						return self.list2df(False,v6df,v7df,v8df,v10df,v12df) if (df == 'DataFrame') else (False,v6,v7,v8,v10,v12)

					return self.list2df(False,v6df,v7df,v8df,v10df,v12df) if (df == 'DataFrame') else (False,v6,v7,v8,v10,v12)
				
				if idx >= lenCount:
					if tlvCount == 0:
						lstate = 'idle'
						if self.sm == True:
							print("(V10)=>(idle) :true")
						return self.list2df(True,v6df,v7df,v8df,v10df,v12df) if (df == 'DataFrame') else (True,v6,v7,v8,v10,v12)
					else: # Go to TL to get others type value
						lstate = 'TL'
						idx = 0
						if self.sm == True:
							print("(V10)=>(TL)")
				
				if idx > lenCount:
					idx = 0 
					lstate = 'idle'
					sbuf = b""
					return self.list2df(False,v6df,v7df,v8df,v10df,v12df) if (df == 'DataFrame') else (False,v6,v7,v8,v10,v12)
				
						
			elif lstate == 'V12':
				
				sbuf += ch
				idx += 1
				if (idx%dataBytes == 0):
					#print("V12:dataBytes({:d}) lenCount({:d}) index:{:d}".format(dataBytes,lenCount,idx))
					try:
						bound = struct.unpack('I', sbuf)
						#print("v12=====sbuf:{:}".format(sbuf))
						#print("V12 Bound: ----:{:}".format(bound))
						v12 = (self.hdr.frameNumber, bound)
						v12df = (self.hdr.frameNumber, bound)
						sbuf = b""
					except:
						if self.dbg == True:
							print("(7)Improper Type 12 Value structure found: ")
							return self.list2df(False,v6df,v7df,v8df,v10df,v12df) if (df == 'DataFrame') else (False,v6,v7,v8,v10,v12)
	
				if idx >= lenCount:
					if tlvCount == 0:
						lstate = 'idle'
						if self.sm == True:
							print("(V12)=>(idle) :true")
						return self.list2df(True,v6df,v7df,v8df,v10df,v12df) if (df == 'DataFrame') else (True,v6,v7,v8,v10,v12)
						
					else: # Go to TL to get others type value
						lstate = 'TL'
						idx = 0
						if self.sm == True:
							print("(V12)=>(TL)")

				if idx > lenCount:
					idx = 0 
					lstate = 'idle'
					sbuf = b""
					return self.list2df(False,v6df,v7df,v8df,v10df,v12df) if (df == 'DataFrame') else (False,v6,v7,v8,v10,v12)
				
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



# Traffic Monitor Detector Raw Data (TMD)
# modify from LPD
# ver:0.0.2
# 2021/04/24
# parsing Traffic Monitor Detector
# hardware:(Batman-201): ISK IWR6843 ES2.0
# company: Joybien Technologies: www.joybien.com
# author: Zach Chen
#===========================================
# output: V6,V7,V8,v9 Raw data
# v0.0.1 : 2020/04/30 release
# v0.1.0 : 2021/04/24 release
#    added DataFrame 

import serial
import time
import struct
import pandas as pd
import numpy as np

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


class TrafficMD:
	
	magicWord =  [b'\x02',b'\x01',b'\x04',b'\x03',b'\x06',b'\x05',b'\x08',b'\x07',b'\0x99']
	port = ""
	hdr = header

	# provide csv file dataframe
	# real-time 
	v6_col_names_rt = ['fN','type','range','azimuth','elv' ,'doppler','sx', 'sy', 'sz'] #ok
	v7_col_names_rt = ['fN','type','posX','posY','velX','velY','accX','accY','posZ','velZ','accZ','tid']
	v8_col_names_rt = ['fN','type','targetID']
	v9_col_names_rt = ['fN','type','snr','noise']
	
	# read from file for trace point clouds
	fileName = ''
	v6_col_names = ['time','fN','type','range','azimuth','elv' ,'doppler','sx', 'sy', 'sz']
	v7_col_names = ['time','fN','type','posX','posY','velX','velY','accX','accY','posZ','velZ','accZ','tid']
	v8_col_names = ['time','fN','type','targetID']
	v9_col_names = ['fN','type','snr','noise']
	sim_startFN = 0
	sim_stopFN  = 0 
	
	v6simo = []
	v7simo = []
	v8simo = []
	v9simo = []
	
	# add for interal use
	tlvLength = 0
	numOfPoints = 0
	# for debug use 
	dbg = False #Packet unpacket Check: True show message 
	sm = False #Observed StateMachine: True Show message
	plen = 16 
	
	def __init__(self,port):
		self.port = port
		print("(jb)Traffic Monitor Detector(TMD) raw Data lib initial")
		print("(jb)For Hardware:Batman-201(ISK)")
		print("(jb)Version: v0.1.0")
		print("(jb)Hardware: IWR-6843 ES2.0")
		print("(jb)Firmware: TMD")
		print("(jb)UART Baud Rate:921600")
		print("==============Info=================")
		print("Output: V6,V7,V8,V9 data:(RAW)")
		print("V6: Point Cloud Spherical")
		print("v6 structure: [(range,azimuth,elevation,doppler),......]")
		print("V7: Target Object List")
		print("V7 structure: [(tid,posX,posY,velX,velY,accX,accY,posZ,velZ,accZ),....]")
		print("V8: Target Index")
		print("V8 structure: [id1,id2....]")
		print("V9: Point Cloud Side Info")
		print("V9 [(snr,noise),....]")
		print("===================================")
	 
		
	def useDebug(self,ft):
		self.dbg = ft
		
	def stateMachine(self,ft):
		self.sm = ft
		
	def getHeader(self):
		return self.hdr
		
	def headerShow(self):
		print("***Header***********") 
		print("Version:     \t%x "%(self.hdr.version))
		print("Platform:    \t%X "%(self.hdr.platform))
		#print("TimeStamp:   \t%s "%(self.hdr.timeStamp))
		print("TotalPackLen:\t%d "%(self.hdr.totalPackLen))
		print("PID(frame#): \t%d "%(self.hdr.frameNumber))
		print("subframe#  : \t%d "%(self.hdr.subFrameNumber))
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
			dataByte = 40  #target struct 40 bytes:(tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ)  
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
				return self.list2df(False,v6,v7,v8,v9) if (df == 'DataFrame') else (False,v6,v7,v8,v9)
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
					return self.list2df(False,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (False,v6,v7,v8,v9)
		
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
						return self.list2df(False,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (False,v6,v7,v8,v9)
					
					if disp == True:  
						self.headerShow()
					
					tlvCount = self.hdr.numTLVs
					if self.hdr.numTLVs == 0:
						#return (False,v6,v7,v8,v9)
						return self.list2df(False,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (False,v6,v7,v8,v9)
						
					if self.sm == True:
						print("(Header)")
						
					sbuf = b""
					idx = 0
					lstate = 'TL'
					  
				elif idx > 48:
					idx = 0
					lstate = 'idle'
					#return (False,v6,v7,v8,v9)
					return self.list2df(False,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (False,v6,v7,v8,v9)
					
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
							return self.list2df(False,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (False,v6,v7,v8,v9)
							
					except:
						print("TL unpack Improper Data Found:")
						if self.dbg == True:
							print("TL unpack Improper Data Found:")
						self.port.flushInput()
						#return (False,v6,v7,v8,v9)
					
						return self.list2df(False,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (False,v6,v7,v8,v9)
					
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
						if (df == 'DataFrame'):
							sz  = r * np.sin(e)
							sx  = r * np.cos(e) * np.sin(a)
							sy  = r * np.cos(e) * np.cos(a)
							#fieldNames = ['time','frameNum','type','range/px','azimuth/py','elv/vx','doppler/vy','sx/accX','sy/accY','sz/pz','na/vz','na/accZ','na/ID']
							v6df.append((self.hdr.frameNumber,'v6',r,a,e,d,sx,sy,sz))
						else:
							v6.append((r,a,e,d))
							
						sbuf = b""
					except:
						if self.dbg == True:
							print("(6.1)Improper Type 6 Value structure found: ")
						#return (False,v6,v7,v8,v9)
						return self.list2df(False,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (False,v6,v7,v8,v9)
					
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
						return self.list2df(True,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (True,v6,v7,v8,v9)
						
					else: # Go to TL to get others type value
						lstate = 'TL' #'tlTL'
						if self.sm == True:
							print("(V6:tlvCnt={:d})=>(TL)".format(tlvCount))
					
				elif idx > lenCount:
					idx = 0
					sbuf = b""
					lstate = 'idle'
					#return (False,v6,v7,v8,v9)
					return self.list2df(False,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (False,v6,v7,v8,v9)
					
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
						return self.list2df(False,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (False,v6,v7,v8,v9)
						
				if idx >= lenCount:
					if disp == True:
						print("count= v9[{:d}]".format(len(v9)))
						
					sbuf = b""
					if tlvCount == 0:
						lstate = 'idle'
						if self.sm == True:
							print("(V9)=>(idle) :true")
						#return (True,v6,v7,v8,v9)
						return self.list2df(True,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (True,v6,v7,v8,v9)
						
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
					return self.list2df(False,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (False,v6,v7,v8,v9)
					
			elif lstate == 'V7':
				sbuf += ch
				idx += 1
				if (idx%dataBytes == 0):
					#print("V7:dataBytes({:d}) lenCount({:d}) index:{:d}".format(dataBytes,lenCount,idx))
					try:
						(tid,posX,posY,velX,velY,accX,accY,posZ,velZ,accZ) = struct.unpack('I9f', sbuf) 
						#fieldNames = ['time','frameNum','type','range/px','azimuth/py','elv/vx','doppler/vy','sx/accX','sy/accY','sz/pz','na/vz','na/accZ','na/ID']
						if (df == 'DataFrame' ):
							v7df.append((self.hdr.frameNumber,'v7',posX,posY,velX,velY,accX,accY,posZ,velZ,accZ,tid))
						else:
							v7.append((tid,posX,posY,velX,velY,accX,accY,posZ,velZ,accZ))
							#print("tid = ({:d}) ,posX:{:.4f} posY:{:.4f} posZ:{:.4f}".format(tid,posX,posY,posZ))
						sbuf = b""
					except:
						if self.dbg == True:
							print("(7)Improper Type 7 Value structure found: ")
						#return (False,v6,v7,v8,v9)
						return self.list2df(False,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (False,v6,v7,v8,v9)
						
				if idx >= lenCount:
					if disp == True:
						print("v7[{:d}]".format(len(v7)))
					 
					sbuf = b""
					if tlvCount == 0:
						lstate = 'idle'
						if self.sm == True:
							print("(V7)=>(idle) :true")
						#return (True,v6,v7,v8,v9)
						return self.list2df(True,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (True,v6,v7,v8,v9)
						
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
					return self.list2df(False,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (False,v6,v7,v8,v9)
				
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
					return self.list2df(True,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (True,v6,v7,v8,v9)
				
				if idx > lenCount:
					sbuf = b""
					idx = 0
					lstate = 'idle'
					#return (False,v6,v7,v8,v9)
					return self.list2df(False,v6df,v7df,v8df,v9df) if (df == 'DataFrame') else (False,v6,v7,v8,v9)

	def getRecordData(self,frameNum):
		s_fn = frameNum + self.sim_startFN
		#print("frame number:{:}".format(s_fn))
		v6d = self.v6simo[self.v6simo['fN'] == s_fn]
		#v6d =  v6dd[v6dd['doppler'] < 0.0]
		#print(v6d)
		v7d = self.v7simo[self.v7simo['fN'] == s_fn]
		v8d = self.v8simo[self.v8simo['fN'] == s_fn]
		v9d = self.v9simo[self.v9simo['fN'] == s_fn]
		chk = 0
		if v6d.count != 0:
			chk = 1
		return (chk,v6d,v7d,v8d,v9d)
		
		
	'''
		v6_col_names_rt = ['fN','type','range','azimuth','elv' ,'doppler','sx', 'sy', 'sz'] #ok
	v7_col_names_rt = ['fN','type','posX','posY','velX','velY','accX','accY','posZ','velZ','accZ','tid']
	v8_col_names_rt = ['fN','type','targetID']
	v9_col_names_rt = ['fN','type','snr','noise']
	
	# read from file for trace point clouds
	fileName = ''
	v6_col_names = ['time','fN','type','range','azimuth','elv' ,'doppler','sx', 'sy', 'sz']
	v7_col_names = ['time','fN','type','posX','posY','velX','velY','accX','accY','posZ','velZ','accZ','tid']
	v8_col_names = ['time','fN','type','targetID']
	v9_col_names = ['fN','type','snr','noise']
	'''
	def readFile(self,fileName):
		#fileName = "pc32021-03-19-10-02-17.csv"  
		#df = pd.read_csv(fileName, error_bad_lines=False, warn_bad_lines=False) 
		self.fileName = fileName 
		#          ['time','fN','type','elv','azimuth','range' ,'doppler','sx', 'sy', 'sz']
		df = pd.read_csv(self.fileName, names = self.v6_col_names, skiprows = [0,10,11,12],dtype={'fN': int,'elv': float,'azimuth':float,'range':float,'doppler':float,'sx':float,'sy':float,'sz':float}) 
		df.dropna()
		#print("------------------- df --------------------shape:{:}".format(df.shape))
		print(df)
		print(df.info())
		#print(df.info(memory_usage="deep")) 
		
		v6simOri = df[(df.type == 'v6')]
		#print("-------------------v6simo------------:{:}".format(v6simOri.shape))
									 
		self.v6simo = v6simOri.loc[:,['fN','type','range','azimuth','elv' ,'doppler','sx', 'sy', 'sz']]
		
		if len(self.v6simo):
			self.sim_startFN = df['fN'].values[0]
			self.sim_stopFN  = df['fN'].values[-1]
		#print(self.v6simo)
		
		self.v6simo['elv'] = self.v6simo['elv'].astype(float, errors = 'raise') 
		
		df7 = pd.read_csv(self.fileName, names = self.v7_col_names, skiprows = [0])  
		
		v7simc = df7[df7['type'] == 'v7']
		self.v7simo  = v7simc.loc[:,['fN','posX','posY','velX','velY','accX','accY','posZ','velZ','accZ','tid']]
		
		v8simc = df[df['type'] == 'v8']
		self.v8simo  = v8simc.loc[:,['fN','elv']]
		#print(self.v8simo)
		
		v9simc = df[df['type'] == 'v9']
		self.v9simo  = v9simc.loc[:,['fN','type','range','azimuth']]
		self.v9simo.columns = ['fN','type','snr','noise']
	
		return (self.v6simo,self.v7simo,self.v8simo,self.v9simo)



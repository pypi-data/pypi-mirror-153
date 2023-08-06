# Medium Range Radar Raw Data (MRR)
# ver:0.0.1
# 2021/12/31
# parsing Medium Range Radar
# hardware:(Batman-601):  
# company: Joybien Technologies: www.joybien.com
# author: Zach Chen
#===========================================
# output: V1,V2,V3,v4 Raw data
# v0.0.1 : 2021/12/31 release
# v0.0.2 : 2022/02/07 format revised
# v0.1.0 : 2022/06/01 tune to fit v3
 

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
	cpuProcessTime = 0
	numOBJs = 0
	numTLVs = 0
	subFrameNumber = 0


class MRR:
    
	magicWord =  [b'\x01',b'\x02',b'\x03',b'\x04',b'\x05',b'\x06',b'\x07',b'\x08',b'\0x99']
	port = ''
	hdr = header
	clearQBuf = True
	# provide csv file dataframe
	# real-time 
	v1_col_names_rt = ['fN','type','doppler','peakVal','X' ,'Y','Z']  
	v2_col_names_rt = ['fN','type','ccX','ccY','csX','csY']
	v3_col_names_rt = ['fN','type', 'tX','tY','velX','velY','csX','csY']
	v4_col_names_rt = ['fN','type','parkingA']  
	
	# read from file for trace point clouds
	fileName = ''
	v1_col_names = ['time','fN','type','doppler','peakVal','X' ,'Y','Z']
	v2_col_names = ['time','fN','type','ccX','ccY','csX','csY']
	v3_col_names = ['time','fN','type', 'tX','tY','velX','velY','csX','csY']
	v4_col_names = ['time','fN','parkingA']  
	sim_startFN = 0
	sim_stopFN  = 0 
	
	v1simo = []
	v2simo = []
	v3simo = []
	v4simo = []
	
	v1 = ([])
	v2 = ([])
	v3 = ([])
	v4 = ([])
	v1df = ([])
	v2df = ([])
	v3df = ([])
	v4df = ([])
	
	def clearBuffer_v124(self):
		if self.clearQBuf == True:
			self.v1 = ([])
			self.v2 = ([])
			#self.v3 = ([])
			self.v4 = ([])
			self.v1df = ([])
			self.v2df = ([])
			#self.v3df = ([])
			self.v4df = ([])
			
	def clearBuffer_v3(self):
		if self.clearQBuf == True:
			self.v3 = ([])
			self.v3df = ([])

	# add for interal use
	tlvLength = 0

	# for debug use 
	dbg = False #Packet unpacket Check: True show message 
	sm = True #Observed StateMachine: True Show message
	 
	
	def __init__(self,port):
		self.port = port
		print("(jb)Medium Range Radar(MRR) raw Data lib initial")
		print("(jb)For Hardware:Batman-601(ISK)")
		print("(jb)Version: v0.1.0")
		print("(jb)Hardware: IWR-6843 ES2.0")
		print("(jb)Firmware: MRR")
		print("(jb)UART Baud Rate:921600")
		print("==============Info=================")
		print("Output: V1,V2,V3,V4 data:(RAW)")
		print("V1: Detected Object")
		print("V1 structure: [(hdr,Doppler,peakVal,X,Y,Z),......]")
		print("V2: Cluster")
		print("V2 structure: [(hdr,ClusterX,ClusterY,ClusterSizeX,ClusterSizeY),....]")
		print("V3: Tracking Object")
		print("V3 structure: [(hdr,TrackingX,TrackingY,velX,velY,ClusterSizeX,ClusterSizeY)....]")
		print("V4: Parking Assist")
		print("V4 [hdr,....] length:32")
		print("===================================")
	 
		
	def useDebug(self,ft):
		self.dbg = ft
		
	def stateMachine(self,ft):
		self.sm = ft
		
	def getHeader(self):
		return self.hdr
		
	def headerShow(self):
		print("***Header***********")  # 32 bytes
		print("Version:     \t%x "%(self.hdr.version))
		print("TotalPackLen:\t%d "%(self.hdr.totalPackLen))
		print("Platform:    \t%X "%(self.hdr.platform))
		print("PID(frame#): \t%d "%(self.hdr.frameNumber))
		print("Inter-frame Processing Time:\t{:d} us".format(self.hdr.cpuProcessTime))
		print("number of Objects:     \t%d "%(self.hdr.numOBJs))
		print("numTLVs:     \t%d "%(self.hdr.numTLVs))
		print("subframe#  : \t%d "%(self.hdr.subFrameNumber))
		print("***End Of Header***") 
		
	
	def list2df(self,l1,l2,l3,l4):
		#print("---------------list2df: v1----------------")
		#print(l1)
		
		ll1 = pd.DataFrame(l1,columns=self.v1_col_names_rt)
		ll2 = pd.DataFrame(l2,columns=self.v2_col_names_rt)
		ll3 = pd.DataFrame(l3,columns=self.v3_col_names_rt)
		ll4 = pd.DataFrame(l4,columns=self.v4_col_names_rt)
		#print("------ll1---------list2df: v1----------------")
		#print(ll1)
		return (ll1,ll2,ll3,ll4)

#
# TLV: Type-Length-Value
# read TLV data
# input:
#     disp: True:print message
#			False: hide printing message
# output:(return parameter)
# (chk, v1, v2, v3, v4)
#  chk:return data status 
#   0: empty: tlv = 0
#   1: data output
#  
#   10: idle
#   99: error
# 
#
#  v1: Detected Object List infomation
#  v2: Cluster Output information
#  v3: Tracking Output information
#  v4: Parking Assist Infomation
#
#
	def tlvRead(self,disp,df = None):
		#print("---tlvRead---")
		#ds = dos
		typeList   = [1,2,3,4]
		typeString = ['HDR','V1','V2','V3','V4']
		msgString  = {'HDR':"",'V1':'V1 Detected Object','V2':'V2 Cluster','V3':'V3 Tracking Object','V4':'V4 Parking Assist'}
		idx = 0
		lstate = 'idle'
		sbuf = b""
		tlvCount = 0
		pbyte = 16
		
		typeCnt = 0 # for check with tlvCount, if typeCnt equal to tlvCcount the process will completed 
		
		while True:
			try:
				ch = self.port.read()
			except:
				#return (False,v6,v7,v8,v9)
				return self.list2df(99,self.v1df,self.v2df,self.v3df,self.v4df) if (df == 'DataFrame') else (99,self.v1,self.v2,self.v3,self.v4)
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
					return self.list2df(10,self.v1df,self.v2df,self.v3df,self.v4df) if (df == 'DataFrame') else (10,self.v1,self.v2,self.v3,self.v4)
		
			elif lstate == 'header':
				sbuf += ch
				idx += 1
				if idx == 32:   
					# print(":".join("{:02x}".format(c) for c in sbuf))  
					# [header - Magicword]
					try: 
						(self.hdr.version,self.hdr.totalPackLen,self.hdr.platform,self.hdr.frameNumber,self.hdr.cpuProcessTime,self.hdr.numOBJs,self.hdr.numTLVs,self.hdr.subFrameNumber
						) = struct.unpack('8I', sbuf)
						if self.dbg == True:
							print("\n================= header({:}) ===========numTLVs:{:}".format(self.hdr.frameNumber,self.hdr.numTLVs))
					except:
						if self.dbg == True:
							print("(Header)Improper TLV structure found: ")
						return self.list2df(99,self.v1,self.v2,self.v3,self.v4) if (df == 'DataFrame') else (99,self.v1,self.v2,self.v3,self.v4)
					
					if disp == True:  
						self.headerShow()
					
					tlvCount = self.hdr.numTLVs
					sbuf = b""
					idx = 0
					lstate = 'TL'
					typeCnt = 0
					self.clearBuffer_v124()
					if self.sm == True:
						print("(Header)")
					if self.hdr.numTLVs == 0:
						lstate = 'idle'
						return self.list2df(0,self.v1df,self.v2df,self.v3df,self.v4df) if (df == 'DataFrame') else (0,self.v1,self.v2,self.v3,self.v4)
						
					

				elif idx > 48:
					idx = 0
					lstate = 'idle'
					return self.list2df(10,self.v1df,self.v2df,self.v3df,self.v4df) if (df == 'DataFrame') else (10,self.v1,self.v2,self.v3,self.v4)
					
			elif lstate == 'TL': #TLV Header type/length
				sbuf += ch
				idx += 1
				if idx == 8:
					#print(":".join("{:02x}".format(c) for c in sbuf))
					try: 
						ttype,self.tlvLength = struct.unpack('2I', sbuf)
						#print("(TL)numTLVs({:d}): tlvCount({:d})-------ttype:tlvLength:v{:d}:{:d}".format(self.hdr.numTLVs,tlvCount,ttype,self.tlvLength))
						if ttype not in typeList or self.tlvLength > self.hdr.totalPackLen:
							if self.dbg == True:
								print("(TL)Improper TL Length(hex):(T){:d} (L){:x} numTLVs:{:d}".format(ttype,self.tlvLength,self.hdr.numTLVs))
							sbuf = b""
							idx = 0
							lstate = 'idle'
							self.port.flushInput()
							return self.list2df(99,self.v1df,self.v2df,self.v3df,self.v4df) if (df == 'DataFrame') else (s99elf.v1,self.v2,self.v3,self.v4)
					except:
						 
						if self.dbg == True:
							print("TL unpack Improper Data Found:")
						self.port.flushInput()
						return self.list2df(99,self.v1df,self.v2df,self.v3df,self.v4df) if (df == 'DataFrame') else (99,self.v1,self.v2,self.v3,self.v4)
					
					lstate = typeString[ttype] 
					#print("(TL)lstate:{:}".format(lstate))
					
					if self.sm == True:
						print("(TL:{:d})=>({:})".format(tlvCount,lstate))
						
					tlvCount -= 1
					idx = 0  
					sbuf = b""
					
			elif lstate == 'V1' or lstate == 'V2' or lstate == 'V3': 
				sbuf += ch
				idx += 1
				if (idx%self.tlvLength == 0):
					typeCnt += 1
					try:
						if self.dbg == True:
							print("========== {} =============:tlvLength={:}  idx={:}".format(msgString[lstate],self.tlvLength,idx))
						#print(":".join("{:02x}".format(c) for c in sbuf))
						objs, xyzQFormat = struct.unpack('2H', sbuf[0:4])
						vUnit = 1 / 2**xyzQFormat
						if self.dbg == True:
							print("objs= {} xzQFormat= {} vUnit= {:.4f}".format(objs,xyzQFormat,vUnit))
							#print(":".join("{:02x}".format(c) for c in sbuf[4:]))
							
						self.typeFunc(typeT = lstate,vUnit= vUnit ,objs=objs,ldata = sbuf[4:], df = df)
						
						if typeCnt != self.hdr.numTLVs:
							if self.dbg == True:
								print("({:}) -> (TL): typeCnt:{:} subFrame:{:}".format(lstate,typeCnt,self.hdr.subFrameNumber))
							lstate = 'TL'
						else:
							if self.sm == True:
								print(f"type Cnt: {typeCnt}   {lstate}")
								print("({:}) -> (idle): typeCnt:{:}".format(lstate,typeCnt))
							#lstate = 'idle'
						sbuf = b""
						idx = 0
						
					except:
						if self.dbg == True:
							print("({:})Improper Type {:} Value structure found: ".format(lstate,lstate))
						return self.list2df(99,self.v1df,self.v2df,self.v3df,self.v4df) if (df == 'DataFrame') else (99,self.v1,self.v2,self.v3,self.v4)
						
					if tlvCount == 0:
						#print(f"==================== tlvCnt == 0  lstate = {lstate}    ===================")
						lstate = 'idle'
						if self.hdr.subFrameNumber == 1:
							return self.list2df(1,self.v1df,self.v2df,self.v3df,self.v4df) if (df == 'DataFrame') else (1,self.v1,self.v2,self.v3,self.v4)
						
						
			elif lstate == 'V4': # parking assist  
				sbuf += ch
				idx += 1
				if (idx%self.tlvLength == 0):
					typeCnt += 1
					try:
						if self.dbg == True:
							print("========== {} ==============:lengthCnt={:}  idx={:}".format(msgString[lstate],self.tlvLength,idx))
						#print(":".join("{:02x}".format(c) for c in sbuf))
						objs, xyzQFormat = struct.unpack('2H', sbuf[0:4])
						vUnit = 1 / 2**xyzQFormat
						if self.dbg == True:
							print("(V4)objs= {} xzQFormat= {} v4Unit= {:.4f} typeCnt:{:}".format(objs,xyzQFormat,vUnit,typeCnt))
						ldata = sbuf[4:]
						astA = [] 
						for i in range(objs):
							start = i * 2
							end   = (i+1) * 2
							ast, = struct.unpack('H', ldata[start:end]) 
							astA.append(ast * vUnit)
							
						if self.dbg == True: 
							print("V4 astA lenth:{:}".format(len(astA)))
						
						if (df == 'DataFrame'):
							self.v4df.append((self.hdr.frameNumber,'v4',astA))
						else:
							self.v4.append((self.hdr.frameNumber,astA))
						
							#print("tid = ({:d}) ,posX:{:.4f} posY:{:.4f} posZ:{:.4f}".format(tid,posX,posY,posZ))
						if typeCnt == self.hdr.numTLVs:
							if self.dbg == True:
								print("(V4) -> (idle): typeCnt:{:}".format(typeCnt))
							lstate = 'idle'	
							return self.list2df(1,self.v1df,self.v2df,self.v3df,self.v4df) if (df == 'DataFrame') else (1,self.v1,self.v2,self.v3,self.v4)
						else:
							if self.dbg == True:
								print("(V4) -> (TL): typeCnt:{:}".format(typeCnt))
							lstate = 'TL'
						
						sbuf = b""
						idx = 0
						 
						 
					except:
						if self.dbg == True:
							print("(V4)Improper Type 4 Value structure found: ")
						
						return self.list2df(99,self.v1df,self.v2df,self.v3df,self.v4df) if (df == 'DataFrame') else (99,self.v1,self.v2,self.v3,self.v4)
						
					
			
	def typeFunc(self,typeT = None ,vUnit= None,objs= None,ldata = None, df = None):
		#print('typeFunc===> {}  vUnit:{:}'.format(typeT,vUnit))
		#print(":".join("{:02x}".format(c) for c in ldata))
		
		if typeT == 'V1':
			for i in range(objs):
				start = i * 10
				end   = (i+1) * 10
				(dt,pt,xt,yt,zt) = struct.unpack('hH3h', ldata[start:end]) # ori 5h
				d = dt * vUnit
				p = pt * vUnit
				x = xt * vUnit
				y = yt * vUnit
				z = zt * vUnit
				if self.dbg == True:
					print("V1 =>  d:{:.4f} p: {:.4f} x:{:.4f} y:{:.4f} z:{:.4f}".format(d,p,x,y,z))
				#v1_col_names_rt = ['fN','type','doppler','peakVal','X','Y','Z']
				if (df == 'DataFrame'):
					self.v1df.append((self.hdr.frameNumber,'v1',d,p,x,y,z))
					
				else:
					self.v1.append((self.hdr.frameNumber,d,p,x,y,z))
				
		if typeT == 'V2':
			for i in range(objs):
				start = i * 8
				end   = (i+1) * 8
				(ccXt,ccYt,csXt,csYt) = struct.unpack('4h', ldata[start:end])  # ori 4h
				ccX  =  vUnit * ccXt
				ccY  =  vUnit * ccYt
				csX  =  vUnit * csXt
				csY  =  vUnit * csYt
				if self.dbg == True:
					print("v2 => X:{:.4f} Y:{:.4f}  XD:{:.4f}  YD:{:.4f}".format(ccX,ccY,csX,csY))
				if (df == 'DataFrame'):
					self.v2df.append((self.hdr.frameNumber,'v2',ccX,ccY,csX,csY))
				else:
					self.v2.append((self.hdr.frameNumber,ccX,ccY,csX,csY)) 
					
		if typeT == 'V3':
			self.clearBuffer_v3()
			for i in range(objs):
				start = i * 12
				end   = (i+1) * 12
				(Xt,Yt,XDt,YDt,Xsizet,Ysizet) = struct.unpack('6h', ldata[start:end]) # ori 6h
				X 	  =  vUnit * Xt
				Y     =  vUnit * Yt
				XD    =  vUnit * XDt
				YD    =  vUnit * YDt
				Xsize =  vUnit * Xsizet
				Ysize =  vUnit * Ysizet
				if self.dbg == True:
					print("v3 => X:{:.4f} Y:{:.4f}  XD:{:.4f}  YD:{:.4f} Xsize:{:.4f} Ysize:{:.4f}".format(X,Y,XD,YD,Xsize,Ysize))
				if (df == 'DataFrame' ):
					self.v3df.append((self.hdr.frameNumber,'v3',X,Y,XD,YD,Xsize,Ysize))
				else:
					 
					self.v3.append((self.hdr.frameNumber,X,Y,XD,YD,Xsize,Ysize))
					


	def getRecordData(self,frameNum):
		s_fn = frameNum + self.sim_startFN
		#print("frame number:{:}".format(s_fn))
		v1d = self.v1simo[self.v1simo['fN'] == s_fn]
		
		v2d = self.v2simo[self.v2simo['fN'] == s_fn]
		v3d = self.v3simo[self.v3simo['fN'] == s_fn]
		v4d = self.v4simo[self.v4simo['fN'] == s_fn]
		return (v6d,v7d,v8d,v9d)
		
		
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
		
		v1simOri = df[(df.type == 'v1')]
		#print("-------------------v1simo------------:{:}".format(v6simOri.shape))
									 
		self.v1simo = v1simOri.loc[:,['fN','type','range','azimuth','elv' ,'doppler','sx', 'sy', 'sz']]
		
		if len(self.v1simo):
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
	'''



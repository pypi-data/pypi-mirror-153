#
# Short Range Radar (SRR)
# ver:0.0.1
# date: 2019/10/03 release
# 
import numpy as np
import struct
import serial

#Frame Header
class header:
	version = "0.0"
	totalPackLen =0
	platform = ""
	frameNumber = 0
	timeCpuCycles = 0
	numDetectedObj = 0
	numTLVs = 0
	tvlHeaderLen = 8
	subFrameNumber = 0


class SRR:
	magicWord =  [b'\x02',b'\x01',b'\x04',b'\x03',b'\x06',b'\x05',b'\x08',b'\x07',b'\0x99']
	port  = ""
	hdr = header

	version = "0.0"
	platform = "iwr1642" 
	sm = False
	checkPort = False
	
	def __init__(self,port):
		self.port = port
		print("*******************************************")
		print("***Short Range Radar init")
		print("***Check TLV state: Call stateMachine(True)")
		print("***Check header: Call getHeader()")
		print("***print info:  tlvRead(True)")
		print("*** More information check Github")
		print("*******************************************")
	
	def srr_test(self):
		print("*********SRR Called**********")
	
	def getHeader(self):
		return self.hdr
		
	def stateMachine(self,ft):
		self.sm = ft
	
	def checkUARTPort(self,ft):
		self.checkPort = ft
	
	def headerShow(self):
		print("***header***********") 
		print("Version:     \t%x "%(self.hdr.version))
		print("TotalPackLen:\t%d "%(self.hdr.totalPackLen))
		print("Platform:    \t%X "%(self.hdr.platform))
		#print("Time Stamp:  \t%d "%(self.hdr.timestamp))
		print("PID(frame#): \t%d "%(self.hdr.frameNumber))
		print("timeCpuCycles#  : \t%d "%(self.hdr.timeCpuCycles))
		print("numDetectedObjs:     \t%d "%(self.hdr.numDetectedObj))
		print("numTLVs:     \t%d "%(self.hdr.numTLVs))
		print("subframe#  : \t%d "%(self.hdr.subFrameNumber))
		#print("Check Sum   :\t{:x}".format(self.hdr.checksum))
		 
		
#TLV: Type-Length-Value
#read TLV data
	
	def tlvRead(self,disp):
		typeDesc = ["idel","V1","V2","V3","V4"]
		#print("---tlvRead---")
		idx = 0
		#version = ""
		lstate = 'idle'
		sbuf = b""
		#tlvLength = 0
		numTLVsCnt = 0

		#*******Message TLV Header 1 *******
		tlvNDO = 0
		tlvNDOCnt = 0
		xyzQFormat = 0
		devParaQ = 0
		 
		#V1
		jb_doppler_v1 = 0
		jb_peakValue = 0
		jb_range_v1 = 0
		jb_x = 0
		jb_y = 0
		#V2
		jb_xc = 0.0
		jb_yc = 0.0
		jb_xcSize = 0.0
		jb_ycSize = 0.0
		#V3
		jb_xt = 0.0  #for Range
		jb_yt = 0.0  #for Range
		jb_vxt = 0.0 #for Doppler
		jb_vyt = 0.0 #for Doppler
		jb_xtSize = 0.0
		jb_ytSize = 0.0
		jb_tRange = 0.0    #sqrt(jb_xt^2+jb_yt^2)
		jb_tDoppler = 0.0  #
		
		#V4
		jb_val = 0.0
		
		v1 = () #objectDet
		v2 = () #ClusterData
		v3 = () #TRACK Data
		v4 = () #PARK Data"
		v6 = () #statsInfo
	
		while True:
			ch = self.port.read()
			if self.checkPort:
				print(str(ch))
				
			if lstate == 'idle':
			#print("state:" + lstate)
				if ch == self.magicWord[idx]:
					#print("*** magicWord:"+ "{:02x}".format(ord(ch)))
					#GPIO.output(21, True)
					idx += 1
					if idx == 8:
						idx = 0
						lstate = 'header'
						sbuf = b""
				else:
					idx = 0
					return (0,v1,v2,v3,v4)
		
			elif lstate == 'header': #header
				sbuf += ch
				idx += 1
				#print(str(ch))
				if idx == 32: #32 + 12 = 44
					# print(":".join("{:02x}".format(c) for c in sbuf))
					#print("------header end -----")
					# [header - Magicword] + [Message TLV header] 
					try:   		  
						(self.hdr.version , self.hdr.totalPackLen, self.hdr.platform , self.hdr.frameNumber, self.hdr.timeCpuCycles,
						 self.hdr.numDetectedObj, self.hdr.numTLVs, self.hdr.subFrameNumber) = struct.unpack('8I', sbuf) 
						
					except:
						print("Improper TLV structure found: ")
						return (0,v1,v2,v3,v4)
						break
					
					if disp == True:
						self.headerShow()
					
					numTLVsCnt = self.hdr.numTLVs 
					if self.hdr.numTLVs == 0:
						lstate = 'idle'
						return (0,v1,v2,v3,v4)
					
					sbuf = b""
					idx = 0
					v1=[]
					v2=[]
					v3=[]
					v4=[]
					lstate = 'TL'
					if self.sm:
						print("------------(header)-numTLVs:{:d} ---subFrame:{:d} --->(TL)".format(self.hdr.numTLVs ,self.hdr.subFrameNumber))
					
				elif idx > 44: # not use
					idx = 0
					lstate = 'idle'
			
			elif lstate == 'TL':
				sbuf += ch
				idx += 1
				if idx == 12: #
					#print(":".join("{:02x}".format(c) for c in sbuf))
					try:
						ttype,self.tlvLength , tlvNDO ,xyzQFormat = struct.unpack('2Ihh',sbuf)
						if self.sm:
							print("(TL) type: {:d} length: {:d} numDetectedObj: {:d}  Qformat:{:d} ".format(ttype,self.tlvLength,tlvNDO,xyzQFormat))
						devParaQ = 2**xyzQFormat
						
					except:
						print("Improper TLV:TL structure found:")
						return (0,v1,v2,v3,v4)
					if ttype < 5 :
						lstate = typeDesc[ttype]

					if ttype == 6:
						lstate = 'V6'
						
					if ttype > 7:
						return (0,v1,v2,v3,v4)
					
					if self.sm:	
						print("From (TL) ==> ({:})".format(lstate))
						
					numTLVsCnt -= 1
					tlvNDOCnt = 0
					sbuf = b""
					idx = 0
					
			elif lstate == "V1": #Object Detected
				sbuf += ch
				idx += 1
				if idx == 8:
					#print("(V1)numTLV:{:d} numTLVsCnt:{:d} tlvNDO:{:d}  getObject:{:d}".format(self.hdr.numTLVs,numTLVsCnt,tlvNDO,tlvNDOCnt))
					try:
						jb_doppler_v1,jb_peakValue,jb_x,jb_y = struct.unpack('hHhh' , sbuf)
						jb_x = float(jb_x)/devParaQ
						jb_y = float(jb_y)/devParaQ
						jb_doppler_v1 = float(jb_doppler_v1)/devParaQ
						jb_range_v1 = np.sqrt(jb_x * jb_x + jb_y * jb_y)
						jb_peakValue = float(jb_peakValue)/devParaQ
						v1.append((tlvNDOCnt,jb_x,jb_y,jb_doppler_v1,jb_range_v1,jb_peakValue))
						
					except:
						print("Improper TLV:V1 structure found:")
						return (0,v1,v2,v3,v4)
						
					tlvNDOCnt += 1
					sbuf = b''
					idx = 0
					 
					if tlvNDOCnt >= tlvNDO:
						if self.sm:
							print("(V1) completed ==> (TL)")
						lstate = 'TL'
						if numTLVsCnt == 0:
							lstate = 'idle'
							return (1,v1,v2,v3,v4)
					else:
						lstate = 'V1'
					
			elif lstate == "V2": #Cluster
				sbuf += ch
				idx += 1
				if idx == 8:
					#print("(V2)numTLV:{:d} numTLVsCnt:{:d} tlvNDO:{:d}  getObject:{:d}".format(self.hdr.numTLVs,numTLVsCnt,tlvNDO,tlvNDOCnt))
					#print(":".join("{:02x}".format(c) for c in sbuf))
					try:
						jb_xc,jb_yc,jb_xcSize,jb_ycSize = struct.unpack('4h' , sbuf)
						v2.append((tlvNDOCnt,float(jb_xc)/devParaQ,float(jb_yc)/devParaQ,float(jb_xcSize)/devParaQ,float(jb_ycSize)/devParaQ))
						#print("(V2)x:{:f} y:{:f} xSize:{:f} ySize:{:f}".format(float(jb_xc)/devParaQ,float(jb_yc)/devParaQ,float(jb_xcSize)/devParaQ,float(jb_ycSize)/devParaQ))
					except:
						print("Improper TLV structure found:")
						return (0,v1,v2,v3,v4)
						
					tlvNDOCnt += 1
					sbuf = b''
					idx = 0
					 
					if tlvNDOCnt >= tlvNDO:
						if self.sm:
							print("(V2) completed ==> (TL)")
						lstate = 'TL'
						if numTLVsCnt == 0:
							lstate = 'idle'
							return (1,v1,v2,v3,v4)
					else:
						lstate = 'V2'
					
			elif lstate == "V3": #Track
				sbuf += ch
				idx += 1
				if idx == 12:
					#print("(V3)numTLV:{:d} numTLVsCnt:{:d} tlvNDO:{:d}  getObject:{:d}".format(self.hdr.numTLVs,numTLVsCnt,tlvNDO,tlvNDOCnt))
					#print(":".join("{:02x}".format(c) for c in sbuf))
					try:
						x0,y0,vx0,vy0,xs0,ys0 = struct.unpack('6h' , sbuf)
						jb_xt = float(x0)/devParaQ
						jb_yt = float(y0)/devParaQ
						jb_vxt = float(vx0)/devParaQ
						jb_vyt = float(vy0)/devParaQ
						jb_xtSize =  float(xs0)/devParaQ
						jb_ytSize =  float(ys0)/devParaQ
						jb_tRange = np.sqrt(jb_xt * jb_xt + jb_yt * jb_yt)
						jb_tDoppler = (jb_xt * jb_vxt + jb_yt * jb_vyt) / jb_tRange
						v3.append((tlvNDOCnt,jb_xt,jb_yt,jb_xtSize,jb_ytSize,jb_vxt,jb_vyt,jb_tRange,jb_tDoppler))
						#print("devParaQ:{:f}".format(devParaQ))
						#print("(V3)x:{:f} y:{:f} xSize:{:f} ySize:{:f} range:{:f} dpler:{:f}".format(jb_xt,jb_yt,jb_xtSize,jb_ytSize,jb_tRange,jb_tDoppler))
					except:
						print("Improper TLV:V3 structure found or Operation Error:")
						return (0,v1,v2,v3,v4)
						
					tlvNDOCnt += 1
					sbuf = b''
					idx = 0
					 
					if tlvNDOCnt >= tlvNDO:
						if self.sm:
							print("(V3) completed ==> (TL)")
						#print("----V3---")
						#print(v3)
						lstate = 'TL'
						if numTLVsCnt == 0:
							lstate = 'idle'
							return (1,v1,v2,v3,v4)
					else:
						lstate = 'V3'
				
			elif lstate == "V4": #Parking_assist
				sbuf += ch
				idx += 1
				if idx == 2:
					#print("(V4)numTLV:{:d} numTLVsCnt:{:d} tlvNDO:{:d}  getObject:{:d}".format(self.hdr.numTLVs,numTLVsCnt,tlvNDO,tlvNDOCnt))
					#print(":".join("{:02x}".format(c) for c in sbuf))
					try:
						pv, = struct.unpack('h' , sbuf)
						jb_val = float(pv)/devParaQ
						v4.append(jb_val)
					except:
						print("Improper TLV:V4 structure found or Operation Error:")
						return (0,v1,v2,v3,v4)
						
					tlvNDOCnt += 1
					sbuf = b''
					idx = 0
					 
					if tlvNDOCnt >= tlvNDO:
						if self.sm:
							print("(V4) completed ==> (TL)")
						#print("----V4---")
						#print(v4)
						lstate = 'TL'
						if numTLVsCnt == 0:
							lstate = 'idle'
							
							
							
							
							
							return (1,v1,v2,v3,v4)
					else:
						lstate = 'V4'
			'''			
			elif lstate == "V6":
				print("--------V6---------")
				lstate = 'idle'
				return (1,v1,v2,v3,v4)
			'''	
			
	 


# High Accuracy Measurement
# ver:0.0.4
#modify:
# print("Descriptor Q Format:\t%d "%(self.ds.descriptor_q))
# modify to fit Jetson nano
#

import serial
import time
import struct
#import numpy as np

class header:
	version = ""
	totalPackLen =0
	tvlHeaderLen = 8
	platform = ""
	frameNumber = 0
	timeCpuCycles = 0
	numDetectedObj = 0
	numTLVs = 0

# Detected Objects
class dos:
	structureTag = 0
	lengthOfStruct  = 0 
	descriptor_val = 0
	descriptor_q = 0
	rangeEst_low = 0
	padding0_low = 0
	padding1_low = 0
	rangeEst_high = 0
	padding0_high = 0
	padding1_high = 0
	rangeValue = 0.0 #for range value
	
#Range Profile Infomation
class rangeProfileInfo:
	structureTag = 0
	lengthOfStruct = 0

#States Info
class stats:
	stt = 0
	los = 0
	ifpt = 0.0
	tot = 0.0
	ifpm = 0.0
	icpm = 0.0
	afcl = 0.0
	icl = .0

class HighAccuracy:
	magicWord =  [b'\x02',b'\x01',b'\x04',b'\x03',b'\x06',b'\x05',b'\x08',b'\x07',b'\0x99']
	port = ""
	#header
	hdr = header
	#detected objects
	ds = dos()
	#range Profile
	rp = rangeProfileInfo
	#stats information
	st = stats

	#--add
	mmWaveType1 = 0 
	length1 = 0
	#descriptor_val = 0
	#descriptor_q = 0
	length2 =0
	mmWaveType6 = 0
	type6Cnt = 0
	
 
	def __init__(self,port):
		self.port = port
		print("***High Accuracy Measurement init***")
		
	
	def detectedObjectRange(self, buf):
		try:
			(self.ds.structureTag,
			self.ds.lengthOfStruct,
			self.ds.descriptor_val,
			self.ds.descriptor_q,
			self.ds.rangeEst_low,
			self.ds.padding0_low,
			self.ds.padding1_low,
			self.ds.rangeEst_high,
			self.ds.padding0_high,
			self.ds.padding1_high) = struct.unpack('2I8H', buf)
			
			self.ds.rangeValue = 0.0
		except:
			print("range error found:")
			return (False,self.ds)
		
		try:
			self.ds.rangeValue = float(int(self.ds.rangeEst_low) + int(self.ds.rangeEst_high) * 2**16) / float(2**self.ds.descriptor_q)
		except:
			print("---divide Error----")
			return (False, self.ds)
			
		#print("val={:.4f}".format(ds.rangeValue))
		return (True,self.ds)


	def getHeader(self):
		return self.hdr
		
	def getDetectedObject(self):
		return self.ds
		
	def getStatsInfo(self):
		return self.st
		
	def getRangeProfileInfo(self):
		return self.rp

	def tlvRead(self, disp):
		#print("---tlvRead---")
		 
		idx = 0
		lstate = 'idle'
		sbuf = b""
		xd = b""
		#*******Message TLV Header 1 *******
		#mmWaveType1 = 0
		#length1 = 0
		#********Message TLV Header 2******
		mmWaveType2 = 0
		length2 = 0
		length3 = 0
		mmWaveType6 = 0
		rangeProfile = b""
	
		while True:
			ch = self.port.read()
			#print(str(ch))
			if lstate == 'idle':
				#print(self.magicWord)
				if ch == self.magicWord[idx]:
					#print("*** magicWord:"+ "{:02x}".format(ord(ch)) + ":" + str(idx))
					#GPIO.output(21, True)	
					idx += 1
					if idx == 8:			
						idx = 0
						lstate = 'header'
						rangeProfile = b""
						sbuf = b""		
						#print("--vital header")
				else:
					idx = 0
					return (False,self.ds, xd)
		
			elif lstate == 'header':
				sbuf += ch
				idx += 1
				if idx == 28:	
					#print("------header-----")
					#print(":".join("{:02x}".format(c) for c in sbuf))
					#print("------header end -----")  
					# [header - Magicword]
					try:   		  
						(self.hdr.version , self.hdr.totalPackLen, 
						self.hdr.platform , self.hdr.frameNumber, 
						self.hdr.timeCpuCycles, self.hdr.numDetectedObj , 
						self.hdr.numTLVs) = struct.unpack('7I', sbuf)
						
					except:
						print("Improper TLV structure found: ")
						rangeProfile = b""
						return (False,self.ds, list(xd))
						
					if disp == True:  
						print("***header***********") 
						print("PID(frame#): \t%d "%(self.hdr.frameNumber))
						print("Version:     \t%x "%(self.hdr.version))
						print("TLV:         \t%d "%(self.hdr.numTLVs))
						print("Detect Obj:  \t%d "%(self.hdr.numDetectedObj))
						print("Platform:    \t%X "%(self.hdr.platform))
						print("TotalPackLen:\t%d "%(self.hdr.totalPackLen))
						
					sbuf = b""
					idx = 0
					lstate = 'dos'
					#if length1 > 288: 
					length1 = 128 
					#print("header=>data1=>length:"%(length1))
					  
				elif idx > 28:
					idx = 0
					lstate = 'idle'
					return (False, self.ds ,list(xd))
				
			elif lstate == 'dos':
				sbuf += ch
				idx += 1
				if idx == 24:
					(tf, self.ds) = self.detectedObjectRange(sbuf)
					if disp == True:
						print("-----[Detected Objects(dos)] ----")
						print("mmWave Type 1:      \t%d "%(self.ds.structureTag))
						print("Data 1 Len:         \t%d "%(self.ds.lengthOfStruct,)) 
						print("Descriptor Value:   \t%d "%(self.ds.descriptor_val))
						print("Descriptor Q Format:\t%d "%(self.ds.descriptor_q)) 
						print("range hi:{:x}".format(self.ds.rangeEst_high))
						print("range lo:{:x}".format(self.ds.rangeEst_low))
						print("range:{:.4f}".format(self.ds.rangeValue))
						
					idx = 0
					sbuf = b""
					
					lstate = 'rpInfo'
					if not tf:
						lstate = 'idle'
						self.port.flushInput()
						return (False,self.ds, list(xd))
						 
			elif lstate == 'rpInfo':
				sbuf += ch
				idx += 1
				if idx == 8:
					#print(":".join("{:02x}".format(c) for c in sbuf))
					idx = 0 
					length2 = 0
					try:   		  
						mmWaveType2 , length2 = struct.unpack('2I',sbuf) 
						self.rp.structureTag = mmWaveType2
						self.rp.lengthOfStruct = length2
						
					except:
						print("Improper Type2, length structure found: ")
						return (False,self.ds, list(xd))
					
					lstate = 'rangeProfile'
					rangeProfile = b""
					if disp == True:
						print("[Range Profile Header] = 8 bytes")
						print("mmWave Type 2:\t%d "%(mmWaveType2))
						print("Data 2 Len:\t%d "%(length2))
						
					sbuf = b""
				  
				elif idx > 8:
					idx = 0
					lstste = 'idle'
				  
			elif lstate == 'rangeProfile':
				
				rangeProfile += ch
				idx += 1
				if idx == length2: #length2 * 8:
					#print(":".join("{:02x}".format(c) for c in rangeProfile))
					if disp == True:
						print("---------rangeProfile:" + str(len(rangeProfile)))
					try:
						#xd = struct.unpack('1024f',rangeProfile)
						xd = struct.unpack("{:d}f".format(int(length2/4)),rangeProfile)
					except:
						print("Improper rangeProfile data found: ")
						return (False,self.ds, list(xd))
        
					#GPIO.output(21, False)
					#print(list(xd))
					idx = 0 
					sbuf = b""
					lstate = "statsInfo"
					if self.type6Cnt > 2:
						lstate = 'idle'
						self.type6Cnt = 0
						if disp == True:
							print("----------re start ----------")
						self.port.flushInput()
						return (False,self.ds, list(xd))
						
				elif length2 > 4096:
					idx = 0
					sbuf = b""
					lstate = 'idle'
					print("Improper range length2 data found: ")
					return (False,self.ds, list(xd))
					
				elif idx > length2:
					idx = 0
					lstate = 'idle'
					sbuf = b""
					return (False,self.ds, list(xd))
					
			elif lstate == 'statsInfo':
				idx += 1
				sbuf += ch
				#print("statsInfo:{:d}".format(idx))
				if idx == 32:
					try:
						
						#mmWaveType6 , length3 , ifpt,tot,ifpm,icpm,afcl,icl = struct.unpack('2L6L',sbuf) 
						# For Jetson Nano => is unsigned int(I)
						mmWaveType6 , length3 , self.st.ifpt,self.st.tot,self.st.ifpm,self.st.icpm,self.st.afcl,self.st.icl = struct.unpack('2I6I',sbuf)
						self.st.stt = mmWaveType6
						self.st.los = length3
					except:
						print("Improper stats data found: ")
						return (False,self.ds, list(xd))
					
					if mmWaveType6 != 6:
						self.type6Cnt += 1
						return (False,self.ds, list(xd))
						
					if disp == True:
						print("[stats Tag/Length]")
						#print(":".join("{:02x}".format(c) for c in sbuf))
						print("mmWave Type 6:\t{:d}".format(mmWaveType6))
						print("Data 3 Len:\t{:d}".format(length3))
						print("Inter-frame Processing Time:\t{:f}".format(self.st.ifpt))
						print("Transmit Output Time:\t{:f}".format(self.st.tot))
						print("Inter-frame Processing Margin:\t{:f}".format(self.st.ifpm))
						print("Inter-chirp Processing Margin:\t{:f}".format(self.st.icpm))
						print("Active frame CPU Load:\t{:f}".format(self.st.icpm))
							
					#print(xd)
					idx = 0
					sbuf = b""
					lstate = 'idle'
					return (True, self.ds, list(xd))
					
			elif idx > 32:
					idx = 0
					lstate = 'idle'
					sbuf = b""
					return (False,self.ds, list(xd))



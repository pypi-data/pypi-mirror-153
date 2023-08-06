#)Traffic Monitor Detect(TMD) key Value data
# ver:0.0.2
# date: 2020/04/30
# parsing Traffic Monitor Detect 
# hardware:(Batman-201): ISK IWR6843 ES2.0
# company: Joybien Technologies: www.joybien.com
# author: Zach Chen
#===========================================
# output: objPoint: [(tidx,posX,posY,velX,velY,iten,Tid),....]
# v0.0.1 : 2020/03/09 release
# v0.0.2 : 2020/04/30 change name to trafficMD_kv

import serial
import time
import struct
from dataclasses import dataclass

#import numpy as np

@dataclass
class subHeader:
	frame: int = 0 #unsign Long
	target: int = 0 #unsign Int
	pcNum : int = 0 #unsign Int Point Cloud Number

@dataclass
class objPoint:
	idx: int = 0
	x: float = 0.0
	y: float = 0.0
	vx: float = 0.0
	vy: float = 0.0
	iten : int = 0
	tid : int = 0


class tmdISK_kv:
	#				{        }        ,      ;
	magicWord =  [b'\x5B',b'\x5D',b'\x3C',b'\x3E']
	
	port = ""
	clen = 20 #exclude: delimeter
	
	def __init__(self,port):
		self.port = port
		print("(jb)Traffic Monit Detect(TMD) lib initial")
		print("(jb)For Hardware:Batman-201(ISK)")
		print("(jb)Hardware: IWR-6843 ES2.0")
		print("(jb)Firmware: TMD")
		print("(jb)UART Baud Rate:921600")
		print("(jb)Data type: kv (key/Value)")
		print("==============Info=================")
		print("Output: frameNum,TargetNum,pcNum")
		print("Output: [(tidx,posX,posY,velX,velY,intensity,Tid),....]")
		print("===================================")
	
	def tmdRead(self,disp):
		target = 0
		targetCnt = 0
		ops = []
		sh = []
		frameNum = 0
		targetCnt = 0
		objMax = 0
		idx = 0
		lstate = 'idle'
		sbuf = b""
		while True:
			try:
				ch = self.port.read()
			except:
				print("(TMD)---port.read() Exception---")
				return (False, [])
			#print(str(ch))
			if lstate == 'idle':
				#print(self.magicWord)
				if ch == self.magicWord[0]:
					#if disp:
					#print("*** magicWord:"+ "{:02x}".format(ord(ch)) + ":" + str(idx))
					idx = 0
					lstate = 'iData'
					ops = [] #Object Point Set
					sbuf = ch
					target = 0 
					#if disp:
					#	print("-----------------------")
					#	print("(jb) idle-> idata")
					
				else:
					idx = 0
					sbuf = b""
					ops = [] 
					return (False,[],[])
					
			elif lstate == 'iTarget':
				sbuf += ch
				idx += 1
				if self.magicWord[2] == ch:
					#print("(jb)iTarget -> iTarget_end")
					lstate = 'iTarget_end'
					idx = 0
					
				else:
					lstate = 'idle'
					sbuf = 0
					return (False,[],[])
					
			elif lstate == 'iTarget_end':
				sbuf += ch
				idx += 1
				#print(":".join("{:02x}".format(c) for c in sbuf))  
				if idx == 21 and self.magicWord[3] == ch:
					#print(":".join("{:02x}".format(c) for c in sbuf))   
					#print("(jb)iTarget_end state:")
					try: 
						(h,idx,x,y,vx,vy,tar,iten,t) = struct.unpack('<cB4fBHc', sbuf) 
						ops.append(objPoint(idx,x,y,vx,vy,tar,iten))
						lstate = 'iTarget'
						idx = 0
						sbuf = b""
						
					except:
						lstate = 'idle'
						print("(jb)Exception ==> iTarget_end -> idle state ")
						return (False,sh,ops)
					
					target -= 1
					if target == 0:
						lstate = 'idle'
						shdr = []
						idx = 0
						sbuf = b""
						return (True,sh,ops)
				
				elif idx > 23:
					lstate = 'idle'
					sbuf = b""
					print("*********data over(iTarget_end)*********")
		
			elif lstate == 'iData':
				sbuf += ch
				#print(":".join("{:02x}".format(c) for c in sbuf))  
				idx += 1
				if idx == 21 and self.magicWord[1] == ch:  
					if disp:
						print("------rx data(iData)-----")
						print(":".join("{:02x}".format(c) for c in sbuf))  
					try: 
						frame = struct.unpack('<i', sbuf[7:11])
						target = int(sbuf[18])
						pcNum = struct.unpack('<H',sbuf[19:21])
						
						sh = subHeader(frame[0],target,pcNum[0])
						#if disp:
						#print(sh)
						lstate = 'idle'
						sbuf = b""
						idx = 0
						if disp:
							print("(jb)iData(1) -> idle state")
						if target == 0:
							return (True,sh,[])
						else:
							lstate = 'iTarget'
							#print('iData -> iTarget')
			
					except:
						lstate = 'idle'
						self.ops = []
						self.shrd = []
						
						if disp:
							print("(jb)---iData Exception---")
					
				elif idx > 23:
					lstate = 'idle'
					sbuf = b""
					print("*********data over(iData)*********")
					if disp:
						print("data over {:d} back to idle state".format(idx))
					frameNum = 0
					objMax = 0
					idx = 0
					ops = []
					return (False,[],[]) 
					
			

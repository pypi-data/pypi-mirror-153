# Long range People Detect Raw Data (LPD)
# ver:0.0.1
# 2019/12/02
# parsing Long range People Detect 
# hardware:(Batman-201): ISK IWR6843 ES2.0
# company: Joybien Technologies: www.joybien.com
# author: Zach Chen
#===========================================
# output: objPoint: [(tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ,state),....]
# v0.0.1 : 2019/12/06 release

import serial
import time
import struct
from dataclasses import dataclass

#import numpy as np

@dataclass
class objPoint:
	tid: int = 0
	x: float = 0.0
	y: float = 0.0
	z: float = 0.0
	vx: float = 0.0
	vy: float = 0.0
	vz : float = 0.0
	accX : float = 0.0
	accY : float = 0.0
	accZ : float = 0.0
	state : int = 0

@dataclass
class objSets:
	frameNum: int
	numObjs: int
	op: [objPoint]

#
# input data: { 32 bytes },{ 32 bytes }...{ 32 bytes };
# ; is end of data
# , is continue data
#

class LpdISK_kv:
	#				{        }        ,      ;
	magicWord =  [b'\x7B',b'\x7D',b'\x2C',b'\x3B']
	port = ""
	clen = 47 #exclude: delimeter
	
	def __init__(self,port):
		self.port = port
		print("(jb)Long range People Detect(LPD) lib initial")
		print("(jb)For Hardware:Batman-201(ISK)")
		print("(jb)Hardware: IWR-6843 ES2.0")
		print("(jb)Firmware: LPD")
		print("(jb)UART Baud Rate:921600")
		print("(jb)Data type: kv (key/Value)")
		print("==============Info=================")
		print("Output: [(tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ,state),....]")
		print("state = 0x00, N/A")
		print("===================================")
	
	def lpdRead(self,disp):
		ops = []
		frameNum = 0
		objMax = 0
		idx = 0
		lstate = 'idle'
		sbuf = b""
		while True:
			try:
				ch = self.port.read()
			except:
				print("(PC3D)---port.read() Exception---")
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
					if disp:
						print("-----------------------")
						print("(jb) idle-> idata")
				else:
					idx = 0
					sbuf = b""
					ops = [] 
					return (False,[])
					
			elif lstate == 'dataConti':
				if ch == self.magicWord[0]:
					sbuf = b""
					sbuf += ch
					idx = 0
					lstate = 'iData'
					if disp:
						print("(jb) dataConti-> iData: {}".format(sbuf))
				else:
					lstate = 'idle'
					if disp:
						print("(jb) dataConti-> idle")
					return (False,[])
		
			elif lstate == 'iData':
				sbuf += ch
				#print(":".join("{:02x}".format(c) for c in sbuf))  
				idx += 1
				if idx == self.clen and self.magicWord[1] == ch: #idxx = 31 + 12(ax,ay,az) + 3(fr) + 1 check=0x7d
					if disp:
						print("------rx data-----")
						print(":".join("{:02x}".format(c) for c in sbuf))  
					
					try: 
						#(h,f,fr,om,oi,tid,x,y,z,vx,vy,vz,ax,ay,az,state,c,t) = struct.unpack('<6c9f3c', sbuf)
						(h,f,fr,om,oi,tid,x,y,z,vx,vy,vz,ax,ay,az,state,c,t) = struct.unpack('<2cL3c9f3c', sbuf)
						op = objPoint(ord(tid),x,y,z,vx,vy,vz,ax,ay,az,ord(state))
						objMax = ord(om)
						frameNum = fr
						if disp:
							print("flowNum:{:d} frameNum:{:d} objMax:{:d} objIdx:{:d} tid:{:d}".format(ord(f)-ord('0'),frameNum,objMax,ord(oi),ord(tid)))
						lstate = 'eodCheck'
						ops.append(op)
						
						if objMax == 0:
							idx = 0
							lstate = 'idle'
							if disp:
								print("(jb)iData(0) -> idle state")
							return (True, objSets(frameNum,objMax,ops))
							
						sbuf = b""
						idx = 0
						if disp:
							print("(jb)iData(1) -> eodCheck state")
					except:
						lstate = 'idle'
						self.ops = []
						if disp:
							print("(PC3D)---iData Exception---")
					
				elif idx > self.clen + 3: #34 - 31= 3 -> 31+13+3 + [3] = 50
					lstate = 'idle'
					sbuf = b""
					print("*********data over*********")
					if disp:
						print("data over {:d} back to idle state".format(idx))
					frameNum = 0
					objMax = 0
					idx = 0
					ops = []
					return (False,[]) 
					
			elif lstate == 'eodCheck':
					if self.magicWord[2] == ch: # check ,
						lstate = 'dataConti'
						if disp:
							print("(jb(,))eodCheck-> dataCont (contiune read): length op count:{:d}".format(len(ops)))
					
					if self.magicWord[3] == ch: # check ;
						lstate = 'idle'
						idx = 0
						if disp:
							print("(jb(;))eodCheck->idle: length op count:{:d}".format(len(ops)))
						return (True, objSets(frameNum,objMax,ops))


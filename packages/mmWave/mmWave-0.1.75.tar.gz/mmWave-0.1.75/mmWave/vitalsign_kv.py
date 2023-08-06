# Vital Sign Detect(VSD) key/value data
# ver:0.0.1
# date: 2020/10/20
# parsing Vital Sign Detect(VSD) key/value data
# hardware:(Batman-201): ISK IWR6843 ES2.0
# company: Joybien Technologies: www.joybien.com
# author: Zach Chen
#===========================================
# output: (header,h,flow,BR,HR,BP,HP,status,tail)
# v0.0.1 : 2020/10/20

import serial
import time
import struct
from dataclasses import dataclass

#import numpy as np

@dataclass
class info:
	h: chr = '{'
	f: chr = '0'
	BR: float = 0.0
	HR: float = 0.0
	BP: float = 0.0
	HP: float = 0.0
	s : chr = '0'
	t:chr = '}'


class VitalSign_kv:
	#				{        }  
	magicWord = [b'\x7b',b'\x7d'] 
	idata = info
	port = ""
	clen = 20
	
	def __init__(self,port):
		self.port = port
		print("(jb)Vital Sign Detect (VSD) key/value lib initial")
		print("(jb)For Hardware:Batman-201(ISK)")
		print("(jb)Hardware: IWR-6843 ES2.0")
		print("(jb)Firmware: VSD")
		print("(jb)UART Baud Rate:115200")
		print("(jb)Data type: kv (key/Value)")
		print("==============Info=================")
		print("Output: (header,h,flow,BR,HR,BP,HP,status,tail)")
		print("===================================")
	
	def tlvRead(self,disp):
		idx = 0
		lstate = 'idle'
		sbuf = b""
		while True:
			try:
				ch = self.port.read()
			except:
				print("(VSD)---port.read() Exception---")
				return (False, [])
			#print(str(ch))
			if lstate == 'idle':
				#print(self.magicWord)
				if ch == self.magicWord[0]:
					
					#print("*** magicWord:"+ "{:02x}".format(ord(ch)) + ":" + str(idx))
					idx = 0
					lstate = 'iData'
					sbuf = ch
					if disp:
						print("(jb) idle-> idata")
					
				else:
					idx = 0
					sbuf = b""
					return (False,[])
					
			elif lstate == 'iData':
				sbuf += ch
				#print(":".join("{:02x}".format(c) for c in sbuf))  
				idx += 1
				#print("ch: idx = {:02x} : {:d}    mg:{:02x}   bool:{:}".format(ord(ch),idx ,ord(self.magicWord[1]) , idx == 19 and self.magicWord[1] == ch))
				if idx == 19: # and self.magicWord[1] == ch:  #wierd 
					#print(":".join("{:02x}".format(c) for c in sbuf))  
					#idata = struct.unpack('<2b4f2b',sbuf) #(h,f,BR,HR,BP,HP,s,t)
					idata = struct.unpack('<cB4fBc',sbuf) #(h,f,BR,HR,BP,HP,s,t)
					if disp:
						print("(jb) iData-> idle")
					lstate = 'idle'
					sbuf = b""
					idx = 0
					return (True,idata) 
				if idx > 20:
					lstate = 'idle'
					sbuf = b""
					idx = 0
			

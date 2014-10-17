# NOTE: to access the raw controller data (which is necessary for tis program), 
# use "sudo apt-get install joystick" to get the right package. 
#
# ANOTHER NOTE: different controllers may use different systems for indexing/
# communicating values. Your location and mileage may vary.

from time import sleep
#from array import array
#import serial

class LogitechRumblePad2()
	self.rawdata = []
	self.smallframe = str('')
	self.recentlyupdated = 0
	self.index = 0
	
	def __init__(self):
		self.pipe = open('/dev/input/js0','r')

	# reads the raw characters coming from the USB controller	
	def getRawData(self)
		# the RumblePad 2 outputs an 8 character frame on every input
		#self.rawdata = []
		self.rawdata = self.pipe.read(8)
		
	# processes the raw characters coming from the USB controller and 
	# puts it into a small frame structure consisting of three characters:  
	#   -smallframe(0): header character (described below)
	#   -smallframe(1): most significant character of button/axis value 
	#   -smallframe(2): least significant character of button/axis value
	# button/axis values are in the form of a 16-bit 2's complement short integer.
	#
	# Bitwise description of the header, following the indexing system below:
	# [ 7 | 6 | 5 | 4 | 3 | 2 | 1 | 0 ]
	#   - bit 7: reserved
	#   - bit 6: reserved
	#   - bit 5: flag for heartbeat frames. 1 = heartbeat, 0 = actual frame
	#   - bit 4: flag for axis values (instead of buttons). 1 = axis, 0 = button
	#   - bits 3 through 0: the index (or "address") of the button/axis that was updated
	def getSmallFrame(self)
		self.smallframe = str('')
		
		self.index = self.rawdata[7]
		isInitVal = ord(self.rawdata[6]) & 0b1000000 # MSB of [6] indicates initialization value
		isButton = ord(self.action[6]) & 0b1 # LSB indicates it's a button, next bit indicates it's an axis
		
		valueMSC = self.rawdata[5] # most significant character
		valueLSC = self.rawdata[4] # least significant character
		
		if(isButton):
			self.smallframe += self.index

			# initialization doesn't cause problems with buttons, so no need to check it here
			self.smallframe += valueMSC;
			self.smallframe += valueLSC;
			
		else:
			self.smallframe += chr(0b00010000 | ord(self.index)) # sets axis flag and puts in index
			
			# initialization wreaks havoc on the axis values (sets them to the lowest negative values
			# possible), so we'll override this.
			if(isInitVal):
				self.smallframe += '\x00'
				self.smallframe += '\x00'
			else:
				self.smallframe += valueMSC
				self.smallframe += valueLSC
				
		self.recentlyupdated = 1;
		return self.smallframe
		
	def getHeartbeat(self)
		heartbeat = chr(0b00100000) + '\x00' + '\x00'
		
		# checks every 20 ms to see if there's been an update; if not,
		# return heartbeat. If so, keep waiting.
		while(recentlyupdated)
			recentlyupdated = 0
			sleep(0.02)
			
		return heartbeat
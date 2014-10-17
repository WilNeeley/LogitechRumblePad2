from time import sleep
import serial
#import signal
import sys
import threading
from Controller import LogitechRumblePad2


#################################
## SERIAL AND CONTROLLER SETUP ##
#################################

# sets up a serial connection to an Arduino over the Raspberry Pi's
# GPIO serial port
ser = serial.Serial(
	port="/devttyAMA0",\
	baudrate=115200,\
	parity=serial.PARITY_NONE,\
	stopbits=serial.STOPBITS_ONE,\
	bytesize=serial.EIGHTBITS,\
	timeout=0)
print("connected to: " + ser.portstr)

# sets up the controller class
controller = LogitechRumblePad2()


################################
## MULTITHREADING DEFINITIONS ##
################################

# sets up a continuous loop to read data from the controller
def updateLoop():
	controller.getRawData() # hangs until it gets a new value, hence the multithreading
	frame = controller.getSmallFrame()
	ser.write(frame)
	print 'U'
	
# sets up a continuous loop that grabs a heartbeat frame if data has not been received
# from the controller recently
def heartbeatLoop():
	hbframe = controller.getHeartbeat()
	ser.write(hbframe)
	print 'H'
	sleep(0.020)
	
# creates a class to safely handle the multithreading
class safeThreading(threading.Thread):
	def __init__(self, function)
		self.function = function
		threading.Thread.__init__(self)
#		threading.Thread.daemon = True # lets the thread close when the program closes
		self.quit = False
		
	def run(self):
		while not self.quit:
			if self.function == 1:
				updateLoop()
			else:
				heartbeatLoop()
				
	def stop(self):
		self.quit = True
		

######################
## CTRL + C HANDLER ##
######################
# may not be necessary now that the threads are set as daemons

# safely flags the threads to close on their own time
def signal_handler(signal, frame):
	print 'You quit out of the program with Ctrl+C!'
	updateThread.stop()
	heartbeatThread.stop()
	sys.exit(0)
	
# initializes the signal handler
signal.signal(signal.SIGINT, signal_handler)


##########################
## STARTING THE THREADS ##
##########################

try:
	print "Starting update thread..."
	updateThread = safeThreading(1)
	updateThread.start()
	print "Started update thread"
except:
	print "Error: unable to start update thread"
	
try: 
	print "Starting heartbeat thread..."
	heartbeatThread = safeThreading(0)
	heartbeatThread.start()
	print "Started heartbeat thread"
except: 
	print "Error: unable to start heartbeat thread"

# lets the program idle while the threads run	
while 1:
	pass


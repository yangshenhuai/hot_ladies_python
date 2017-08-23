import serial
import logging
import time
import re

logging.basicConfig(filename='wechat_bot.log',level=logging.INFO)
logger = logging.getLogger(__name__)


def start():
	ser = serial.Serial('/dev/ttyACM0') #in order to get updated data
	while True:
		ser.flushInput()
		for i in range(10):
			data = ser.readline()
			handled = handleData(data)
			if handled:
				break;
		time.sleep(3)

def handleData(data):
	#TODO handle data from arduino
	print('start to handle ',data)

	return False
		

if __name__ == '__main__':
	#for test
	start()


import serial
import logging
import time
import re

logging.basicConfig(filename='wechat_bot.log',level=logging.INFO)
logger = logging.getLogger(__name__)
gas_re = re.compile('gs(\d+\.\d+)ge')
gas_threadhold = 300
m=None
def start(master):
	global m 
	m = master	
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
	str_data = data.decode('utf-8')
	gas_match = gas_re.search(str_data)
	if(gas_match):
		gas_val = gas_match.group(1)
		current_gas = float(gas_val)
		print(current_gas)
		if(current_gas >= gas_threadhold):
			m.send('ALERT:GAS LEAK!!')
			print('Alert')	
		return True
	return False
		

if __name__ == '__main__':
	#for test
	start()


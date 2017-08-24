import serial
import logging
import time
import re

logging.basicConfig(filename='wechat_bot.log',level=logging.INFO)
logger = logging.getLogger(__name__)
gas_re = re.compile('gs(\d+\.\d+)ge')
th_re = re.compile('hts(\d+\.\d+\-\d+\.\d+)hte')
flame_re = re.compile('NoF|Fire')
gas_threadhold = 300
m=None
currentTemp = None
currentHum = None
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
		time.sleep(1)

def handleData(data):
	#TODO handle data from arduino
	str_data = data.decode('utf-8')
	gas_match = gas_re.search(str_data)
	if(gas_match):
		gas_val = gas_match.group(1)
		current_gas = float(gas_val)
		print('gas ',current_gas)
		if(current_gas >= gas_threadhold):
			if m is not None:
				m.send('ALERT:GAS LEAK!!')
			print('GAS Alert')	
		return True
	th_match = th_re.search(str_data)
	if(th_match):
		global currentTemp
		global currentHum
		th_val = th_match.group(1)
		hum_and_temp = th_val.split("-")
		currentHum = hum_and_temp[0]
		currentTemp = hum_and_temp[1]
		print('hum ',currentHum , ' temp', currentTemp)
		return True
	flame_match = flame_re.search(str_data)
	if(flame_match):
		flame_val = flame_match.group(0)
		if(flame_val == 'Fire'):
			print('Fire!Fire!')
			if m is not None:
				m.send('ALERT:FIRE!FIRE!')
		return True
	return False
		

if __name__ == '__main__':
	#for test
	start(None)


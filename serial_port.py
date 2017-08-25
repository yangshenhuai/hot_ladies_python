import serial
import logging
import time
import re

logging.basicConfig(filename='wechat_bot.log',level=logging.INFO)
logger = logging.getLogger(__name__)
gas_re = re.compile('gs(\d+\.\d+)ge')
th_re = re.compile('hts(\d+\.\d+\-\d+\.\d+)hte')
flame_re = re.compile('NoF|Fire')
light_re = re.compile('ls(\d+)le')
gas_threadhold = 300
m=None
currentTemp = None
currentHum = None
currentLight = None
gas_last_notify_time = 0 
fire_last_notify_time = 0
notify_interval = 60
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
		global gas_last_notify_time
		gas_val = gas_match.group(1)
		current_gas = float(gas_val)
		logger.info('gas {}'.format(current_gas))
	
		if(current_gas >= gas_threadhold  ):
			current_time = int(time.time())
			if m is not None and (current_time - gas_last_notify_time) > notify_interval:
				m.send('ALERT:GAS LEAK!!')
				gas_last_notify_time = current_time
			logger.info('GAS Alert')	
		return True
	th_match = th_re.search(str_data)
	if(th_match):
		global currentTemp
		global currentHum
		th_val = th_match.group(1)
		hum_and_temp = th_val.split("-")
		currentHum = hum_and_temp[0]
		currentTemp = hum_and_temp[1]
		logger.info('hum {0} , temp {1}'.format(currentHum , currentTemp))
		return True
	flame_match = flame_re.search(str_data)
	if(flame_match):
		global fire_last_notify_time
		flame_val = flame_match.group(0)
		if(flame_val == 'Fire'):
			logger.info('Fire!Fire!')
			current_time = int(time.time())
			if m is not None and (current_time - fire_last_notify_time) > notify_interval:
				fire_last_notify_time = current_time
				m.send('ALERT:FIRE!FIRE!')
		return True
	light_match = light_re.search(str_data)
	if(light_match):
		global currentLight
		currentLight = light_match.group(1)
		logger.info('currentLight {}'.format(currentLight))
		return True

	return False
		

if __name__ == '__main__':
	#for test
	start(None)


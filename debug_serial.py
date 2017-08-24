import serial


if __name__ == '__main__':
	ser = serial.Serial("/dev/ttyACM0")
	while(1):
		print(ser.readline())

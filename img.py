import os
import time
from PIL import Image,ImageDraw,ImageFont
import re

ISOTIMEFORMAT='%Y%m%d%H%M%S'
image_folder = "static/capture_img/"
default_resolution = "1024*768"

def capture_new_pic():
	now_str = time.strftime(ISOTIMEFORMAT,time.localtime())
	pic_name = image_folder + now_str  + ".png"
	os.system('raspistill -w 1024 -h 768 -q 75 -o ' + pic_name)
	#https://www.raspberrypi.org/documentation/raspbian/applications/camera.md
	return pic_name


def get_image_with_resolution(image_id,resolution):
	img_location = image_folder + image_id + ".png"
	img = Image.open(img_location)
	if resolution == '' :
		return img_location
	width_height = resolution.split('*')	
	new_img = img.resize((int(width_height[0]),int(width_height[1])),Image.ANTIALIAS)
	
	resolution_img = image_folder + image_id + "_" + resolution + ".png" 
	new_img.save(resolution_img)
	return resolution_img
def get_all_existing_images():
	pattern = re.compile('\d{14}\.png')
	result = []
	for file_name in os.listdir(image_folder):
		m = pattern.match(file_name)
		if m:
			time_str = file_name[0:14]
			result.append(time_str)	
	result = sorted(result,reverse=True)
	return result

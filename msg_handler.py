#!/usr/bin/env python3.6
# coding: utf-8
from wxpy import *
import img



class MsgHandler:
	def handle(self,msg) : pass
	def match(self,msg):
		return True


class TakePicutreHandler(MsgHandler):
	def handle(self,msg):
		try:
			img_name = img.capture_new_pic()
			msg.reply_image(img_name)
		except:
			msg.reply('Time out...Try again.')
			
	def match(self,msg):
		try:
			return msg.text == 'pic'
		except:
			return False
	

class TulingHandler(MsgHandler):
	def __init__(self):
		self.tuling = Tuling(api_key='43132241d9524efc897bbf0129b23fd8')			
	def handle(self,msg):
		self.tuling.do_reply(msg)
	def match(self,msg):
		return True

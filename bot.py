#!/usr/bin/env python3.6
# coding: utf-8
from wxpy import *
import img
import logging
import msg_handler
logging.basicConfig(filename='wechat_bot.log',level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(console_qr=True)
bot.enable_puid()
handlers = [msg_handler.TakePicutreHandler(),msg_handler.TulingHandler()]

@bot.register(msg_types=TEXT, except_self=False)
def auto_reply_all(msg):
	logger.info('received text message : %s',msg)
	#msg.chat.send('Hello!')
	#msg.reply('World!')
	#tuling.do_reply(msg)
	for handler in handlers:
		if handler.match(msg):
			handler.handle(msg)
			break

bot.join()
import bot
import logging
logging.basicConfig(filename='wechat_bot.log',level=logging.INFO)
logger = logging.getLogger(__name__)

def notify(msg):
	logger.info('will notify message to master: ' , msg)
	bot.master.send(msg)

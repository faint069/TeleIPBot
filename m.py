import telebot
import requests
import json
import logging

def getip():
	try:
		r = requests.post("http://ip-api.com/json/?fields=status,message,query")
	except:
		message = "Could not retrieve JSON data"
		logging.log(logging.ERROR, message)
		return message
	try:
		ip_info = json.loads(r.text)
	except:
		message = "Bad JSON format" + r.text
		logging.log(logging.ERROR, message)
		return message
	if ip_info["status"] == "success":
		ip = ip_info["query"]
		logging.log(logging.INFO, "Получил IP: " + ip)
	else:
		ip = "ip-api error: " + ip_info["message"]
		logging.log(logging.ERROR, ip)
	return ip

logging.basicConfig(filename="log.log",level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

token_file = open('personal_data/token')
token = token_file.read()
bot = telebot.TeleBot(token)
token_file.close()

subscriber_id_file = open('personal_data/subscriber_id')
subscriber_id = int(subscriber_id_file.read())
subscriber_id_file.close()

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	logging.log(logging.INFO,"Получено сообщение от "+ message.from_user.first_name + " " + message.from_user.last_name + " ID: " + str(message.from_user.id))
	logging.log(logging.INFO,"Текст: " + message.text)
	if message.from_user.id == subscriber_id:
		bot.send_message(message.chat.id, getip())
	else:
		bot.send_message(message.chat.id,
					 "You are not authorized to use this bot, sorry.\nYou can configure Your own IP reporter using github repository https://github.com/faint069/TeleIPBot")
bot.polling(none_stop=True, interval=1)

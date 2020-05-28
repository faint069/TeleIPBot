import telebot
import requests
import json
import logging

def getip():
	try:
		r = requests.post("http://ip-api.com/json/?fields=status,message,query")
	except:
		return "Could not retrieve JSON data"
	try:
		ip_info = json.loads(r.text)
	except:
		return "Bad JSON format" + r.text
	if ip_info["status"] == "success":
		ip = ip_info["query"]
	else:
		ip = "ip-api error: " + ip_info["message"]
	return ip

logging.basicConfig(filename="log.log",level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

token_file = open('token')
token = token_file.read()
bot = telebot.TeleBot(token)
token_file.close()

subscriber_id_file = open('subscriber_id')
subscriber_id = int(subscriber_id_file.read())
subscriber_id_file.close()

@bot.message_handler(func=lambda m: True)
def echo_all(message):
	logging.log(logging.INFO,"Получено сообщение от "+ message.from_user.first_name + " " + message.from_user.last_name)
	logging.log(logging.INFO,"Текст: " + message.text)
	if message.from_user.id == subscriber_id:
		bot.reply_to(message, getip())

bot.polling(none_stop=True, interval=1)

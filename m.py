import telebot
import requests
import json
import logging
from apscheduler.schedulers.background import BackgroundScheduler

def get_ip():
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


def ip_check_job():
	current_ip = get_ip()

	ip_store_file = open("ip_store.json", "r")
	ip_store = json.load(ip_store_file)
	ip_store_file.close()

	last_ip = ip_store[-1]
	if current_ip != last_ip:
		logging.log(logging.INFO, "IP адрес изменился. Текущий адресс: " + current_ip)
		bot.send_message(subscriber_id, "IP адрес изменился. Текущий адресс: " + current_ip)

		ip_store.append(current_ip)
		ip_store_file = open("ip_store.json", "w")
		json.dump(ip_store, ip_store_file)
		ip_store_file.close()


logging.basicConfig(filename="log.log",level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(ip_check_job, "interval", minutes=15)


token_file = open("personal_data/token", "r")
token = token_file.read()
bot = telebot.TeleBot(token)
token_file.close()

subscriber_id_file = open("personal_data/subscriber_id", "r")
subscriber_id = int(subscriber_id_file.read())
subscriber_id_file.close()


@bot.message_handler(func=lambda m: True)
def echo_all(message):
	logging.log(logging.INFO,"Получено сообщение от "+ message.from_user.first_name + " " + message.from_user.last_name + " ID: " + str(message.from_user.id))
	logging.log(logging.INFO,"Текст: " + message.text)
	if message.from_user.id == subscriber_id:
		bot.send_message(message.chat.id, get_ip())
	else:
		bot.send_message(message.chat.id,
					 "You are not authorized to use this bot, sorry.\nYou can configure Your own IP reporter using github repository https://github.com/faint069/TeleIPBot")


bot.polling(none_stop=True, interval=1)

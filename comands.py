import os
import main
from datetime import datetime
import random
import subprocess


def speak(text):
	main.voice.say(text)
	main.voice.runAndWait()


def ctime():
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	speak(f'сейчас: {current_time}')


def hau():
	answer = random.choice(main.hau_answer)
	print("[Log] Ответ сформулирован: " + answer)
	speak(answer)


def waud():
	answer = random.choice(main.waud_answer)
	print("[Log] Ответ сформулирован: " + answer)
	speak(answer)


def speak_hello():
	answer = random.choice(main.hello_answer)
	print("[Log] Ответ сформулирован: " + answer)
	speak(answer)


def speak_goodbye():
	answer = random.choice(main.goodbye_answer)
	print("[Log] Ответ сформулирован: " + answer)
	speak(answer)


def about_me():
	speak('я - Вероника. бета версия голосового ассистента. сейчас я умею не многое, но благодоря опытной команде разработчиков быстро пополняюсь новыми функциями.\
			 моя задача - как то облегчить жизнь простому пользователю. мои функции на текущий момент: могу открыть блокнот, сказать текущие \
			 погодные условия и время, мне можно задать несколько вопросов о моем текущем состоянии (как дела, что делаю) \
			 и я вам с радостью на них отвечу')


def get_weather(observations):
	info_weather = observations.weather
	temperature = round(info_weather.temperature('celsius')['temp'])
	if temperature % 10 == 1:
		ending = 'градус'
	elif temperature % 10 == 2 or 3 or 4:
		ending = "градуса"
	else:
		ending = "градусов"

	answer = "сейчас: " + str(temperature) + " " + ending + " по цельсию. облачность - " + str(
		info_weather.clouds) + ' процентов.'
	speak(answer)
	answer = ''

	if info_weather.detailed_status == "clear sky":
		answer = " небо чистое"
	elif info_weather.detailed_status == "cloud":
		answer = " облачно"
	speak(answer)


def open_notepad(program):
	speak("открываю блокнот")
	process = subprocess.Popen(program)


def close_notepad():
	os.system(r'TASKKILL /IM notepad.exe')
	speak("блокнот закрыт")


def open_browser():
	pass


def close_browser():
	pass


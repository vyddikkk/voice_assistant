import os
import time
from datetime import datetime
from fuzzywuzzy import fuzz
import pyowm
import pyttsx3
import speech_recognition as sr
import random

'''
каждый таск нужно открывать вторым потоком, не мешая веронике слушать задания на основном потоке.
тогда будут работать команды закрытия приложений.
'''


voice = pyttsx3.init()

owm = pyowm.OWM('ba2df49bc414f5681ed5ac043f1454f3')
mgr = owm.weather_manager()

observation = mgr.weather_at_place('Kherson,UA')

opts = {
	"alias": ('виталина', "вера", "вита", "лина", "верочка", "верунька",
	          "витачка", "вета", "веркин", "верка", "вероника", "вероничка", "вероня",
	          "ника"),
	"tbr": ("скажи", "расскажи", "мне", "нужно", "произнеси", "сколько", "который",
	        "+", "-", "*", "/", "умножить", "умнож", "плюс", "минус", "какая", 'назови', 'текущую',
	        "разделить", "поделить", "открой", "открывай", "включи", "пожалуйста", 'текущее', 'текущая'),
	"cmds": {
		'ctime': ('текущее время', 'сейчас времени', 'который час'),
		'weather': ('текущая погода', 'сколько градусов', 'погода на улице'),
		'hello': ("привет", "здравствуй", "здарова"),
		'goodbye': ("пока", "прощай"),
		'waud': ("что делаешь", "чем занята"),
		'hau': ('как дела', "как себя чувствуешь", "как самочувствие", "система в норме"),
		'about me': ('о себе', "что ты можешь")
	}
}

hello_answer = ["здравствуй, рада приветствовать. я готова к работе.",
                "приветик", "привет-привет", "здоровенькие были"]
goodbye_answer = ["до новых встреч", "удачи, приятного дня", "останусь на этом же месте ждать", "до свидания"]
hau_answer = ["все хорошо", "у меня отличный настрой", "чувствую себя замечательно",
              "немного опечалена бездействием, но это можно исправить"]
waud_answer = ["сейчас я жду ваших команд", "разсуждаю о смысле бытия", "считаю птичек"]


# Todo ------- разместить проект на гите. доделать функции, добавить условия в execute_cmd.


def listening():
	r = sr.Recognizer()
	with sr.Microphone() as source:
		print("[Log] Cлушаю команду: ")
		r.pause_threshold = 1
		r.adjust_for_ambient_noise(source, duration=1)
		audio = r.listen(source)
		try:
			task = r.recognize_google(audio, language="ru-RU").lower()
			print("[+] Распознанно: " + task)
		except:
			print('голос не распознан, пробую еще раз...')
			task = listening()

		cmd = recognize_cmd(task)
		execute_cmd(cmd['cmd'])


def recognize_cmd(cmd):
	RC = {'cmd': '', 'percent': 0}
	for c, v in opts['cmds'].items():

		for x in v:
			vrt = fuzz.ratio(cmd, x)
			if vrt > RC['percent']:
				RC['cmd'] = c
				RC['percent'] = vrt

	return RC


def execute_cmd(cmd):
	if cmd == 'waud':
		waud()
	elif cmd == 'hau':
		hau()
	elif cmd == 'ctime':
		ctime()
	elif cmd == 'weather':
		get_weather(observation)
	elif cmd == 'about me':
		about_me()
	elif cmd == 'hello':
		speak_hello()
	elif cmd == 'goodbye':
		speak_goodbye()
		quit()


def speak(text):
	voice.say(text)
	voice.runAndWait()


def ctime():
	now = datetime.now()
	current_time = now.strftime("%H:%M:%S")
	speak(f'сейчас: {current_time}')


def hau():
	answer = random.choice(hau_answer)
	print("[Log] Ответ сформулирован: " + answer)
	speak(answer)


def waud():
	answer = random.choice(waud_answer)
	print("[Log] Ответ сформулирован: " + answer)
	speak(answer)


def speak_hello():
	answer = random.choice(hello_answer)
	print("[Log] Ответ сформулирован: " + answer)
	speak(answer)


def speak_goodbye():
	answer = random.choice(goodbye_answer)
	print("[Log] Ответ сформулирован: " + answer)
	speak(answer)


def about_me():
	speak('я - Вероника. бета версия голосового ассистента. сейчас я умею не многое, но благодоря опытной команде разработчиков быстро пополняюсь новыми функциями.\
			 моя задача - как то облегчить жизнь простому пользователю. мои функции на текущий момент: могу отрыть блокнот, сказать текущие \
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


if __name__ == '__main__':
	while True:
		listening()

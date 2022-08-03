from fuzzywuzzy import fuzz
import pyowm
import pyttsx3
import speech_recognition as sr
from config import OWMTOKEN
import comands

voice = pyttsx3.init()

owm = pyowm.OWM(OWMTOKEN)
mgr = owm.weather_manager()

observation = mgr.weather_at_place('Kherson,UA')


opts = {
	"alias": ('виталина', "вера", "вита", "лина", "верочка", "верунька",
	          "витачка", "вета", "веркин", "верка", "вероника", "вероничка", "вероня",
	          "ника"),
	"cmds": {
		'ctime': ('текущее время', 'сейчас времени', 'который час'),
		'weather': ('текущая погода', 'сколько градусов', 'погода на улице'),
		'hello': ("привет", "здравствуй", "здарова"),
		'goodbye': ("пока", "прощай"),
		'waud': ("что делаешь", "чем занята"),
		'hau': ('как дела', "как себя чувствуешь", "как самочувствие", "система в норме"),
		'about me': ('о себе', "что ты можешь"),
		'open_notepad': ('открой блокнот',),
		'close_notepad': ('закрой блокнот',),

	}
}

hello_answer = ["здравствуй, рада приветствовать. я готова к работе.", "приветик", "привет-привет", "здоровенькие были"]
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
		comands.waud()
	elif cmd == 'hau':
		comands.hau()
	elif cmd == 'ctime':
		comands.ctime()
	elif cmd == 'weather':
		comands.get_weather(observation)
	elif cmd == 'about me':
		comands.about_me()
	elif cmd == 'hello':
		comands.speak_hello()
	elif cmd == 'goodbye':
		comands.speak_goodbye()
		quit()
	elif cmd == 'open_notepad':
		comands.open_notepad('notepad.exe')
	elif cmd == 'close_notepad':
		comands.close_notepad()


if __name__ == '__main__':
	while True:
		listening()

'''
в этом файле код для поиска нужного микрофона. и проверка библиотеки pyttsx3.
нет никакой связи с main файлом.
'''


import pyttsx3
import speech_recognition as sr

# список устройств подключеных к консоли, поиск нужного для звукозаписи
for index, name in enumerate(sr.Microphone.list_microphone_names()):
	print("Microphone with name \'{1}\' found for Microphone(device_index={0})".format(index, name))

# первый голос, проверка библиотеки
engine = pyttsx3.init()
engine.say("привет, мир")
engine.runAndWait()

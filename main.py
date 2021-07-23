import serial
import pyttsx3 as talk
from playsound import playsound as ps
import speech_recognition as sr

ser = serial.Serial('/dev/cu.usbmodem143301', baudrate=9600, timeout=1)
duck = talk.init()

sample_rate = 48000
chunk_size = 2048

r = sr.Recognizer()

mic_list = sr.Microphone.list_microphone_names()

mic_id = 0
for i in range(0, len(mic_list)):
    name = mic_list[i]
    if name == 'External Microphone':
        mic_id = i


def duck_talk(text):
    duck.say(text)
    duck.runAndWait()


def duck_debugging():
    speech = ''

    with sr.Microphone(device_index=mic_id, sample_rate=sample_rate,
                       chunk_size=chunk_size) as source:

        r.adjust_for_ambient_noise(source, duration=5)
        duck_talk("Don't worry, Agent Duck is here to safe the day. Please run through your code with Agent Duck")

        try:
            while 1:
                duck_talk("Go ahead, don't be shy")
                audio = r.listen(source)
                text = r.recognize_google(audio)
                duck_talk("you said: " + text)
                print(text)
                speech = speech + text

                duck_talk("Have you cracked the code? Reply: chocolate")
                audio = r.listen(source)
                reply = r.recognize_google(audio)
                print(reply)
                if 'chocolate' in reply:
                    print('continue')
                    continue
                else:
                    duck_talk("Good job! Agent Duck is glad.")
                    print('break')
                    break

        # error occurs when google could not understand what was said

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:
            print("Could not request results from GoogleSpeechRecognitionservice;{0}".format(e))


duck.say('this works o m g')
duck.runAndWait()

# def duck_programming():


while 1:

    data = (ser.readline()).decode('utf-8')
    print(data)

    if 'blue on' in data:
        ps('audio/BeeperEmergencyCall.mp3')
        duck_talk('blue light on, agent duck thinks you need help')
        duck_debugging()

    elif 'yellow on' in data:
        ps('audio/PhoneRinging.mp3')
        duck_talk('yellow light on, transferring you to our agent')
        duck_debugging()

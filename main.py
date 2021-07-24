from datetime import datetime
import json
import serial
import pyttsx3 as talk
from playsound import playsound as ps
import speech_recognition as sr
from googlesearch import search
import spacy
import webbrowser

record = {}

ser = serial.Serial("/dev/cu.usbmodem144301", baudrate=9600, timeout=1)
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

nlp = spacy.load("en_core_web_sm")
all_stopwords = nlp.Defaults.stop_words

word_list = ['I', 'this', 'that', 'part', 'the', 'try', 'write', 'suppose', 'work', 'this part', 'that part']

for word in word_list:
    all_stopwords.add(word)


def searcher(text):
    text = text.lower()
    doc = nlp(text)

    nouns = [chunk.text for chunk in doc.noun_chunks if chunk.text not in all_stopwords]
    verbs = [token.lemma_ for token in doc if token.pos_ == "VERB" if token.lemma_ not in all_stopwords]

    #remove duplicates
    nouns = list(dict.fromkeys(nouns))
    verbs = list(dict.fromkeys(verbs))

    allWords = (str(nouns + verbs)).replace('[', '').replace(']', '').replace("'", '').replace(',', '')

    return search(allWords, num_results=3)


def duck_talk(text):
    duck.say(text)
    duck.runAndWait()


def duck_debugging():
    speech = ''

    with sr.Microphone(device_index=mic_id, sample_rate=sample_rate,
                       chunk_size=chunk_size) as source:

        r.adjust_for_ambient_noise(source, duration=5)
        duck_talk("Don't worry, Agent Buck is here to safe the day. Please run through your code with Agent Buck")

        try:
            while 1:
                duck_talk("Go ahead, don't be shy")
                audio = r.listen(source)
                text = r.recognize_google(audio)
                duck_talk("you said: " + text)
                print(text)
                speech = speech + text

                duck_talk("Have you cracked the code? Reply: chocolate to continue or coffee to get help")
                audio = r.listen(source)
                reply = r.recognize_google(audio)
                print(reply)
                if 'chocolate' in reply:
                    print('continue')
                    continue
                elif 'coffee' in reply:
                    duck_talk("Don't worry! Agent Duck will redirect you external help, straight from your web "
                              "browser. "
                              "Before we proceed, log your details.")
                    desc = input("Give a short description: \n")
                    lang = input("Programming Language used: \n")

                    search_list = searcher(speech)

                    record[datetime.now().strftime('%Y-%m-%d %H:%M:%S')] = {
                        "Short Description": desc,
                        "Session Logs:": speech,
                        "Language used": lang,
                        "Useful references": search_list
                    }

                    webbrowser.open(search_list[0], new=2)
                    break

                else:
                    duck_talk("Good job! Agent Buck is glad. Log your details before moving on.")
                    desc = input("Give a short description: \n")
                    lang = input("Programming Language used: \n")
                    record[datetime.now().strftime('%Y-%m-%d %H:%M:%S')] = {
                        "Short Description": desc,
                        "Session Logs:": speech,
                        "Language used": lang,
                        "Useful references": searcher(speech)
                    }
                    print('break')
                    break

        # error occurs when google could not understand what was said

        except sr.UnknownValueError:
            duck_talk("I could not understand. Call again if you need help!")
            print("Google Speech Recognition could not understand audio")

        except sr.RequestError as e:
            print("Could not request results from GoogleSpeechRecognitionservice;{0}".format(e))


def save_json(temp):
    dict2 = json.load(file)
    dict2.update(temp)
    print(dict2)

    newfile = open('codeRecords/records.json', 'w')
    json.dump(dict2, newfile, sort_keys=True, indent=4)


duck_talk("Starting session.")

file = open('codeRecords/records.json', 'r')

while 1:

    try:
        data = (ser.readline()).decode('utf-8')
        print(data)

        if 'blue on' in data:
            ps('audio/BeeperEmergencyCall.mp3')
            duck_talk('blue light on, agent buck thinks you need help')
            duck_debugging()

        elif 'yellow on' in data:
            ps('audio/PhoneRinging.mp3')
            duck_talk('yellow light on, transferring you to our agent')
            duck_debugging()

    except KeyboardInterrupt:
        duck_talk("Thank you for using Agent Buck Services. Have a pleasant day.")
        save_json(record)

        exit()

import pyaudio
import pyttsx3
import speech_recognition as sr
from selenium import webdriver

#for accessing sites and manipulates using voice commands
from selenium.webdriver.common.keys import keys
from selenium.webdriver.common.by import By
import time


def input_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Interpreting....")
            query = r.recognize_google(audio, language="en-in")
            print(f"user said: {query}")
        except Exception as e:
            say("I did not get that what you are saying, can you say it again? ")
            return "none"
        return query


def say(text):
    print(f"Speaking: {text}")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def terminate(query):
    say("I am going to close this program. Thank you, sir.......")
    exit()


def set_Driver():
    driver = webdriver.Chrome()
    return driver




def main():
    say("hey boss how are you? , I am you personal assistant ")
    while True:
        print("Listening...")
        query = input_command()
        if query == 'none':
            continue
        if query == "terminate the program":
            terminate(query)


if __name__ == "__main__":
    main()

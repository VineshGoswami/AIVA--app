import pyaudio
import pyttsx3
import speech_recognition as sr


def input_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        audio = r.listen(source)
        try:
            print("Interpreting....")
            query = r.recognize_google(audio, language = "en-in")
            print(f"user said: {query}")
        except Exceptionn as e:
            print("I did not get that what you are saying, can you say it again? ")
            return "none"
        return query




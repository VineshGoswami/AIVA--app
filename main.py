import pyaudio
import pyttsx3
import speech_recognition as sr
import webbrowser
import pyautogui


def input_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Interpreting....")
            query = r.recognize_google(audio, language="en-in")
            print(f"user said: {query}")
        except Exception as e:
            say("I did not get that. Can you say it again?")
            return "none"
        return query


def say(text):
    print(f"Speaking: {text}")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def terminate():
    say("I am going to close this program. Thank you, sir.")
    exit()


def main():
    say("Hey boss, how are you? I am your personal assistant.")
    while True:
        query = input_command().lower()
        if query == 'none':
            continue
        if "terminate the program" in query:
            terminate()


if __name__ == "__main__":
    main()

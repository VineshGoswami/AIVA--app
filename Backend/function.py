import datetime
import pyttsx3


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


def show_time():
    strfTime = datetime.datetime.now().strftime("%H:%M:%S")
    say("The current time is display on screen sir...")
    print("Current time:", strfTime)


def show_date():
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    say("The current date is display on screen sir....")
    print("Current date:", current_date)

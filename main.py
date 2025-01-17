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


def main():
    say("hey vinesh how are you? , I am you personal assistant ")
    while True:
        print("Listening...")
        query = input_command()
        if query == 'none':
            continue


if __name__ == "__main__":
    main()

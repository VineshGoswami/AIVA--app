import keyboard
import pyaudio
import pyttsx3
import speech_recognition as sr
from wiki import wiki_search
from goog import goog_search
from open_App import open_app
from function import show_date, show_time
import pyautogui
import subprocess
import json


listening = False


def listen():
    global listening
    listening = True
    print("listening sir..")


def stop():
    global listening
    listening = False
    print("stopped listening")


keyboard.add_hotkey('ctrl+k', listen)
keyboard.add_hotkey('ctrl+p', stop)


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


def take_screenshot(query):
    im = pyautogui.screenshot()
    im.save("screenshot.jpg")


def terminate():
    say("I am going to close this program. Thank you, sir.")
    exit()


def main():
    say("Hey boss, how are you? I am your personal assistant.")
    while True:
        if listening:
            query = input_command().lower()
            if query == 'none':
                continue

            if "search wikipedia for " in query.lower():
                topic = query.replace("search wikipedia for ", "").strip()
                if topic:
                    result = wiki_search(topic)
                    say(result)
                    print(result)
                else:
                    say(f"sorry sir i can't search {query}")

            elif "google search for " in query:
                topic1 = query.replace("google search for ", "").strip()
                if topic1:
                    result = goog_search(topic1)
                    print(result)
                else:
                    say(f"sorry we cannot find this {result}")

            elif "screenshot" in query.lower():
                say("processing your command..")
                take_screenshot(query)

            elif "open app" in query:
                if query.strip() == "open app":
                    say("Which application would you like to open?")
                    app_name = input_command().lower().strip()
                    if app_name == "none" or app_name == "":
                        say("No application name provided.")
                    else:
                        open_app(app_name)

            elif "answer these questions" in query.lower():
                say("Sure, you can start asking me questions now. Say 'exit chat' to stop.")
                while True:
                    user_question = input_command().lower().strip()
                    if user_question in ["exit chat", "stop chat", "terminate chat"]:
                        say("Exiting chat mode, sir.")
                        break
                    if user_question == "none" or user_question == "":
                        say("No question detected. Please try again.")
                        continue
                    say("Processing your request, sir...")
                    print(f"Debug: Running bot.py with query - {user_question}")
                    result = subprocess.run(
                        ["python", "C:\\Users\\vines\\Aiva_project\\Backend\\bot.py", user_question],
                        capture_output=True, text=True)
                    print(f"Debug: bot.py output - {result.stdout}")
                    gemini_response = result.stdout.strip().replace("*", "")
                    if gemini_response and "i am sorry" not in gemini_response.lower():
                        say(gemini_response)

            elif "latest news" in query:
                say("Fetching the latest news for you, sir.")

                result = subprocess.run(
                    ["python", "C:\\Users\\vines\\Aiva_project\\Backend\\news.py"],
                    capture_output=True, text=True, encoding="utf-8"
                )

                output = result.stdout.strip()
                print(f"Debug: Raw output from news.py: {output}")

                try:
                    news_articles = json.loads(output)

                    if isinstance(news_articles, dict) and "error" in news_articles:
                        say(news_articles["error"])
                    elif news_articles:
                        say("Here are the top 5 news headlines.")
                        for news in news_articles:
                            say(news["title"])
                            print(f"Title: {news['title']}\nDescription: {news['description']}\n")
                    else:
                        say("I couldn't fetch any news at the moment.")
                except json.JSONDecodeError:
                    say("An error occurred while fetching the news. The response was not in the correct format.")
                    print("Error: Failed to parse JSON.")

            elif "show date and time " in query.lower():
                show_time()
                show_date()

            elif "terminate the program" in query:
                terminate()
                break


if __name__ == "__main__":
    main()

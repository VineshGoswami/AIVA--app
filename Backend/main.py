import keyboard
import pyaudio
import pyttsx3
import speech_recognition as sr
from wiki import wiki_search
from goog import goog_search
from open_App import open_app
from function import show_date, show_time, find_and_open, delete_item, save_item
from music import open_spotify, play_song, pause_song, resume_song, next_song, previous_song, create_playlist
from llm import generate_llm_response,get_factual_answer
from you import open_youtube
import pyautogui
import subprocess
import json
from database import savechat as save_chat
from authenticator import login, register

listening = False
username = None


def listen():
    global listening
    listening = True
    print("Listening sir..")


def stop():
    global listening
    listening = False
    print("Stopped listening")


keyboard.add_hotkey('ctrl+v', listen)
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
            print(f"User said: {query}")
        except Exception as e:
            say("I did not get that. Can you say it again?")
            return "none"
        return query


def say(text):
    print(f"Speaking: {text}")
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


def take_screenshot():
    im = pyautogui.screenshot()
    im.save("screenshot.jpg")
    say("Screenshot saved successfully.")


def terminate():
    say("I am going to close this program. Thank you, sir.")
    exit()


def authenticate_user():
    global username
    say("Welcome to AIVA Assistant!")

    while True:
        print("\n1. Register\n2. Login (Password)\n3. Login (Face Recognition)")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            username = input("Enter a new username: ").strip()
            password = input("Enter a new password: ").strip()
            face_image_path = input("Enter image path for face registration (optional, press Enter to skip): ").strip()

            message = register(username, password, face_image_path if face_image_path else None)
            say(message)
            if "successful" in message:
                break

        elif choice == "2":
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            message = login(username, password=password, use_face=False)
            print(message)
            if "successful" in message:
                break

        elif choice == "3":
            username = input("Enter username: ").strip()
            image_path = input("Enter image path for face authentication: ").strip()
            message = login(username, use_face=True, image_path=image_path)
            say(message)
            if "successful" in message:
                break

        else:
            say("Invalid choice. Try again.")


def main():
    say("Hey boss, how are you? I am your personal assistant.")

    while True:
        if listening:
            query = input_command().lower()
            if query == 'none':
                continue

            response = ""

            if "search wikipedia for " in query.lower():
                topic = query.replace("search wikipedia for ", "").strip()
                if topic:
                    response = wiki_search(topic)
                else:
                    response = f"Sorry sir, I can't search {query}"

            elif "google search for " in query:
                topic1 = query.replace("google search for ", "").strip()
                if topic1:
                    response = goog_search(topic1)
                else:
                    response = f"Sorry, we cannot find this {query}"

            elif "screenshot" in query.lower():
                take_screenshot()
                response = "Screenshot taken successfully."

            elif "open app" in query:
                if query.strip() == "open app":
                    say("Which application would you like to open?")
                    app_name = input_command().lower().strip()
                    if app_name == "none" or app_name == "":
                        response = "No application name provided."
                    else:
                        open_app(app_name)
                        response = f"Opening {app_name}."

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
                    result = subprocess.run(
                        ["python", "C:\\Users\\vines\\Aiva_project\\Backend\\bot.py", user_question],
                        capture_output=True, text=True)
                    gemini_response = result.stdout.strip().replace("*", "")
                    if gemini_response and "i am sorry" not in gemini_response.lower():
                        say(gemini_response)
                        save_chat(username, user_question, gemini_response)

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

            elif "show date and time" in query.lower():
                show_time()
                show_date()

            elif "system" in query.lower():
                say("name for searching an file or folder ")
                name = input_command().lower().strip()
                if name == "none" or name == "":
                    say("no file or folder exist in system")
                else:
                    find_and_open(name)

            elif "delete" in query:
                say("Which file or folder would you like to delete?")
                item_name = input_command().lower().strip()
                if item_name:
                    delete_item(item_name)

            elif "save" in query:
                say("Which file or folder would you like to rename?")
                item_name = input_command().lower().strip()
                if item_name:
                    say("What should be the new name?")
                    new_name = input_command().lower().strip()
                    if new_name:
                        save_item(item_name, new_name)

            elif "play video" in query.lower():
                open_youtube(query)
            elif "open spotify" in query:
                say("Opening Spotify for you, sir.")
                open_spotify()

            elif "play song" in query:
                say("Which song would you like to play?")
                song_name = input_command().lower().strip()
                if song_name:
                    say(f"Playing {song_name}.")
                    play_song(song_name)

            elif "pause song" in query:
                say("Pausing the song.")
                pause_song()

            elif "resume song" in query:
                say("Resuming playback.")
                resume_song()

            elif "next song" in query:
                say("Skipping to the next song.")
                next_song()

            elif "previous song" in query:
                say("Going back to the previous song.")
                previous_song()

            elif "create playlist" in query:
                say("What should be the name of the playlist?")
                playlist_name = input_command().lower().strip()
                if playlist_name:
                    message = create_playlist(playlist_name)
                    say(message)

            elif "hey what's up" in query:
                say("What would you like to ask the AI?")
                llm_prompt = input_command().lower().strip()
                if llm_prompt:
                    generative_response = generate_llm_response("Answer concisely: " + llm_prompt)

                    context = ("Narendra Modi is the Prime Minister of India, serving since 2014. "
                               "He leads the Bharatiya Janata Party and has been influential in Indian politics.")

                    factual_response = get_factual_answer(llm_prompt, context)
                    combined_response = ("Generative Response: " + generative_response +
                                         "\nFactual Response: " + factual_response)
                    say(combined_response)
                    print(combined_response)
                else:
                    say("No prompt detected for the LLM.")

            elif "terminate the program" in query:
                terminate()
                break

            save_chat(username, query, "Response processed.")


if __name__ == "__main__":
    authenticate_user()
    main()

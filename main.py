import pyaudio
import pyttsx3
import speech_recognition as sr
from youtubesearchpython import VideosSearch
import webbrowser
import pyautogui
import keyboard


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


listening = False


def start_listen():
    global listening
    listening = True
    print("listening to you sir")


def pause_listen():
    global listening
    listening = False
    print(" now pausing my self")


keyboard.add_hotkey("ctrl + alt + k", start_listen)
keyboard.add_hotkey("ctrl + alt + p", pause_listen)


def terminate():
    say("I am going to close this program. Thank you, sir.")
    exit()


def open_youtube(query):
    try:
        # Perform YouTube search
        videos_search = VideosSearch(query, limit=5)
        results = videos_search.result()['result']
        if results:
            say("Here are the top 5 results:")
            for i, video in enumerate(results, start=1):
                print(f"{i}. {video['title']} ({video['duration']}) - {video['link']}")
            say("Please say the number of the video you'd like to play, for example, 'play 1'.")
            choice = input_command().lower()
            if 'play' in choice:
                try:
                    video_number = int(choice.split()[-1]) - 1
                    if 0 <= video_number < len(results):
                        selected_video = results[video_number]
                        say(f"Playing: {selected_video['title']}")
                        return selected_video['link']
                    else:
                        say("Invalid choice. Playing the first video.")
                        return results[0]['link']
                except ValueError:
                    say("I couldn't understand the number. Playing the first video.")
                    return results[0]['link']
            else:
                say("Invalid input. Playing the first video.")
                return results[0]['link']
        else:
            say("No results found.")
            return None
    except Exception as e:
        say(f"Error during search: {e}")
        return None


def play_video(url):
    if url:
        webbrowser.open(url)
        say("Video opened in the browser.")
    else:
        say("Could not open the video.")


def close_youtube(query):
    try:
        pyautogui.hotkey('alt', 'f4')
        say("Closing YouTube, sir.")
    except Exception as e:
        say(f"Error closing YouTube: {e}")


def main():
    say("Hey boss, how are you? I am your personal assistant.")
    while True:
        if listening:
            query = input_command().lower()
            if query == 'none':
                continue
            if "terminate the program" in query:
                terminate()
            elif "open youtube" in query:
                say("What video would you like to search for?")
                search_query = input_command().lower()
                if search_query == 'none':
                    continue
                video_url = open_youtube(search_query)
                play_video(video_url)
            elif "close youtube" in query:
                close_youtube(query)

            else:
                say("I didn't understand that. Please say 'open youtube', 'close youtube', or 'terminate the program'.")


if __name__ == "__main__":
    main()

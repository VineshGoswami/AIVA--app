import subprocess
import os


def open_app(query):
    from main import say
    apps = {
        "notepad": "notepad",
        "calculator": "calc",
        "file explorer": "explorer",
        "task manager": "taskmgr",
        "command prompt": "start cmd",
        "powershell": "start powershell",
        "google chrome": "start chrome",
        "firefox": "start firefox",
        "microsoft edge": "start msedge",
        "spotify": "start spotify",
        "word": "start winword",
        "excel": "start excel",
        "powerpoint": "start powerpnt",
        "pycharm": r'C:\Program Files\JetBrains\PyCharm Community Edition 2024.1\bin\pycharm64.exe',
        "intellij idea": r'C:\Program Files\JetBrains\IntelliJ IDEA Community Edition 2024.1\bin\idea64.exe',

    }

    for key in apps:
        if key in query.lower():
            say(f"Opening {key}...")
            command = apps[key]
            try:
                if "start" in command or command.endswith(".exe"):
                    subprocess.Popen(command, shell=True)
                else:
                    subprocess.Popen(["cmd", "/c", "start", command], shell=True)
            except Exception as e:
                say(f"Sorry, I couldn't open {key}. Error: {str(e)}")
            return

    say("Sorry, I don't recognize this application.")



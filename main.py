import os
from bs4 import BeautifulSoup
import requests
from subprocess import Popen

header = """
    __  ___   ______       ____        __ 
   /  |/  /  / ____/      / __ )____  / /_
  / /|_/ /  / /          / __  / __ \/ __/
 / /  / /  / /___       / /_/ / /_/ / /_  
/_/  /_/   \____/      /_____/\____/\__/  
"""

colors = {
    'blue': '\033[94m',
    'pink': '\033[95m',
    'green': '\033[92m',
}


def colorize(string, color):
    if not color in colors: return string
    return colors[color] + string + '\033[0m'


def run():
    print(colorize("Running Bot...", 'green'))
    p = Popen(["python", "bot.py"])
    p.communicate()
    input("Press [Enter] to continue...")


def check_update():
    url = "https://raw.githubusercontent.com/xLeon-python/MCBot/master/bot.py"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    version = str(soup).split("\n")[0].split(": ")[1]

    file = open('bot.py').read().split("\n")[0].split(": ")[1]
    if int(version.replace(".", "")) > int(file.replace(".", "")):
        print(colorize("Update wurde gefunden", 'green'))
        print("Neue Version: " + version)
        print(colorize("[0] ", 'blue') + "Installieren")
        print(colorize("[1] ", 'blue') + "Später installieren")
        choice = input(">> ")
        if int(choice) == 0:
            print(colorize("\nInstalling...", "green"))
            file = open("bot.py", "w")
            file.write(str(soup))
            file.close()
            print(colorize("\nUpdate complete", "green"))
    else:
        print(colorize("Es wurde kein Update gefunden", 'green'))
    input("Press [Enter] to continue...")

menuItems = [
    {"Run bot": run},
    {"Check update": check_update},
    {"Exit": exit},
]

def main():
    while True:
        # Print some badass ascii art header here !
        print(colorize(header, 'pink'))
        version = open('bot.py').read().split("\n")[0].split(": ")[1]
        print(colorize("Version: " + version + '\n', 'green'))
        for item in menuItems:
            print(colorize("[" + str(menuItems.index(item)) + "] ", 'blue') + list(item.keys())[0])
        choice = input(">> ")
        try:
            if int(choice) < 0: raise ValueError
            # Call the matching function
            list(menuItems[int(choice)].values())[0]()
        except (ValueError, IndexError):
            pass


if __name__ == "__main__":
    main()
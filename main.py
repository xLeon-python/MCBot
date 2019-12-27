from pyfiglet import Figlet

f = Figlet(font='slant')
print(f.renderText('M C   Bot'))

print("\n")
from bs4 import BeautifulSoup
import requests

def check_update():
    url = "https://raw.githubusercontent.com/xLeon-python/MCBot/master/main.py"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    version = str(soup).split("\n")[0].split(": ")[1]

    file = open('bot.py').read().split("\n")[0].split(": ")[1]

    if version == file:
        return True
    else:
        return False

print(check_update())
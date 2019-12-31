#Version: 0.1.1

from __future__ import print_function

import sys, json, time
from datetime import datetime

import mojang_api
from minecraft import authentication
from minecraft.exceptions import YggdrasilError
from minecraft.networking.connection import Connection
from minecraft.networking.packets import Packet, clientbound, serverbound
from minecraft.compat import input
from minecraft.networking.packets.clientbound.play import ChatMessagePacket
from minecraft.networking.packets import PlayerPositionAndLookPacket
from minecraft.networking.packets import PositionAndLookPacket
from minecraft.networking.types import (
    Position, PositionAndLook, RelativeHand, BlockFace,
)

import random, time, sys, base64, json, asyncio, requests
import discord
import aiohttp
from bs4 import BeautifulSoup
import threading
import io
from urllib.request import urlopen
from urllib.parse import urlparse
from io import BytesIO

from PIL import Image
from discord import Webhook, AsyncWebhookAdapter

with open("config.json", encoding="utf-8") as json_file:
    config = json.load(json_file)
    TOKEN = config['token']
    CHANNEL = config['channelID']
    webhook_url = config['webhook']
    ACCOUNT = config["mcAcc"].split(":")
    admins = config["admins"]
    custom_answers = config["custom"]
auth_token = authentication.AuthenticationToken()
#auth_token.authenticate(ACCOUNT[0], ACCOUNT[1])
while 1:
    try:
        auth_token.authenticate(ACCOUNT[0], ACCOUNT[1])
        break
    except:
        print("waiting for mojang cooldown")
        time.sleep(10)

print("Logged in as %s..." % auth_token.username)
connection = Connection("gommehd.net", auth_token=auth_token)

#connection = Connection("localhost", 62139, username="checkerbot")

'''
def print_incoming(packet):
    if type(packet) is Packet:
        # This is a direct instance of the base Packet type, meaning
        # that it is a packet of unknown type, so we do not print it.
        return
    print('--&gt; %s' % packet, file=sys.stderr)


def print_outgoing(packet):
    print('&lt;-- %s' % packet, file=sys.stderr)


connection.register_packet_listener(print_incoming, Packet, early=True)
connection.register_packet_listener(print_outgoing, Packet, outgoing=True)
'''

def console_input():
    while 1:
        msg = input("")

        if msg == "exit()":
            print("exit...")
            #sys.exit()
            exit()

        avatar = "https://mc-heads.net/avatar/checkerbot"

        loop = asyncio.new_event_loop()
        loop.run_until_complete(write_chat("checkerbot", "CONSOLE: " + msg, avatar))
        loop.stop()

        send_chat("/cc CONSOLE: " + msg)

def handle_join_game(join_game_packet):
    print('Connected.')

connection.register_packet_listener(handle_join_game, clientbound.play.JoinGamePacket)

chat_msg = 0
get_bot_msg = False
get_all_msg = False
nh_counter = 0


def getScore(name):
    url = 'https://www.gommehd.net/player/index?playerName=' + name
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    gungame = soup.find("div", {"id": "gungame"})
    score = gungame.find('span', attrs={'class': 'score'})
    return score.text

def getNameHistory(nh):
    counter = 0
    content = ""
    global nh_counter
    global get_bot_msg
    get_bot_msg = True
    for i in nh:
        counter += 1
        if nh[0] == i:
            #send_chat("/cc " + str(counter) + ". " + nh[0]["name"])
            content = str(content) + str(counter) + ". " + nh[0]["name"] +"\n"
        else:
            while nh_counter == counter:
                print(".")
            dt = datetime.fromtimestamp(i["changedToAt"] / 1000)
            print(str(counter) + i["name"] + " (" + dt.strftime('%d/%m/%Y') + ")")
            #send_chat("/cc " + str(counter) + ". " + i["name"] + " (" + dt.strftime('%d/%m/%Y') + ")")

            content = str(content) + str(counter) + ". " + i["name"] + " (" + dt.strftime('%d/%m/%Y') + ")\n"



    get_bot_msg = False
    return content


async def write_chat(ignname, content, avatar):
    url = urlparse(avatar)
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook_url, adapter=AsyncWebhookAdapter(session))
        await webhook.send(content, username=ignname, avatar_url=url.geturl())

def send_chat(content):
    packet = serverbound.play.ChatPacket()
    packet.message = content
    connection.write_packet(packet)

def Freunde(chat_msg):

    global admins
    for i in admins:

        if str(chat_msg["extra"][3]["text"]) == str(i["name"]):
            #print(chat_msg["extra"][-1]["text"].split(" ", 1)[0])

            startswitch = chat_msg["extra"][-1]["text"].split(" ", 1)[0]
            if startswitch == "cmd":
                cmd = chat_msg["extra"][-1]["text"].split(" ", 1)[1]
                send_chat(str(cmd))
                print("executing command : " + cmd)

            elif startswitch == ".invite":
                cmd = "/clan invite " + chat_msg["extra"][-1]["text"].split(" ", 1)[1]
                send_chat(str(cmd))
                print("invite sent to " + chat_msg["extra"][-1]["text"].split(" ", 1)[1])

            elif startswitch == ".promote":
                cmd = "/clan promote " + chat_msg["extra"][-1]["text"].split(" ", 1)[1]
                send_chat(str(cmd))
                print(cmd)
                print("promoted " + chat_msg["extra"][-1]["text"].split(" ", 1)[1])

            elif startswitch == ".demote":
                cmd = "/clan demote " + chat_msg["extra"][-1]["text"].split(" ", 1)[1]
                send_chat(str(cmd))
                print(cmd)
                print("demoted " + chat_msg["extra"][-1]["text"].split(" ", 1)[1])

def print_chat(chat_packet):
    global chat_msg
    chat_msg = json.loads(chat_packet.json_data)

    try:

        if chat_msg["extra"][1]["text"] != "Clans" and chat_msg["extra"][1]["text"] != "Freunde":
            return

        if " " in chat_msg["extra"][3]["text"]:
            return
        if chat_msg["extra"][1]["text"] == "Freunde":
            Freunde(chat_msg)
            return
        global get_bot_msg
        if get_bot_msg == False:

            if chat_msg["extra"][3]["text"] == "checkerbot":
                return
        else:
            if chat_msg["extra"][3]["text"] == "checkerbot":
                global nh_counter
                nh_counter = int(chat_msg["extra"][5]["text"].split(". ")[0])
        # print("Message (%s): %s" % (chat_packet.field_string('position'), chat_packet.json_data))
        # print(chat_msg["extra"][5]["text"].split(": ")[1])
        # print(chat_msg["extra"][3]["text"])
        # print(chat_msg["extra"][3]["text"] + ": " + chat_msg["extra"][3]["text"].split(" ")[1])

        ignname = chat_msg["extra"][3]["text"]
        content = chat_msg["extra"][-1]["text"]

        print(ignname + ": " + content)

        avatar = "https://mc-heads.net/avatar/" + str(ignname)

        loop = asyncio.new_event_loop()
        loop.run_until_complete(write_chat(ignname, content, avatar))
        loop.stop()

        startswitch = chat_msg["extra"][5]["text"].split(" ")[0]

        if startswitch == ".kills":
            kills = getScore(chat_msg["extra"][5]["text"].split(" ")[1])
            send_chat("/cc Kills von " + chat_msg["extra"][5]["text"].split(" ")[1] + ": " + kills)

            ignname = "checkerbot"
            content = "Kills von " + chat_msg["extra"][5]["text"].split(" ")[1] + ": " + kills

        elif startswitch == ".nh":
            send_chat("/cc getting name history... " + chat_msg["extra"][5]["text"].split(" ")[1])
            nh = mojang_api.get_username_history(chat_msg["extra"][5]["text"].split(" ")[1])
            nh = json.dumps(nh)
            nh = json.loads(nh)
            content = getNameHistory(nh)
            for i in content.split("\n"):
                send_chat("/cc " + i)
                time.sleep(0.2)
            ignname = "checkerbot"

        elif startswitch == ".set":
            with open("config.json", encoding="utf-8") as json_file:
                config = json.load(json_file)
                custom_answers = config["custom"]
                skip = False
                for i in custom_answers:
                    if i["name"].lower() == chat_msg["extra"][5]["text"].split(" ", 2)[1].lower():
                        i["answer"] = [ chat_msg["extra"][5]["text"].split(" ", 2)[2] ]
                        skip = True
                if skip == False:
                    custom_answers.append({"name":chat_msg["extra"][5]["text"].split(" ", 2)[1], "answer":[ chat_msg["extra"][5]["text"].split(" ", 2)[2] ]})
                config["custom"] = custom_answers
            jsonFile = open("config.json", "w+")
            jsonFile.write(json.dumps(config))
            jsonFile.close()

            return

    except IndexError:

        ignname = chat_msg["extra"][3]["text"]
        content = chat_msg["extra"][-1]["text"]

        with open("config.json", encoding="utf-8") as json_file:
            config = json.load(json_file)
            custom_answers = config["custom"]

        for i in custom_answers:
            if str(i["name"]).lower() == str(content).lower():
                send_chat("/cc " + json.loads(json.dumps(i["answer"][0])))
                return

        if chat_msg["extra"][-1]["text"] == " Clan-Informationen ":
            get_all_msg = True
        avatar = "https://mc-heads.net/avatar/" + str(ignname)

        loop = asyncio.new_event_loop()
        loop.run_until_complete(write_chat(ignname, content, avatar))
        loop.stop()
    except KeyError:
        return
    except Exception as e:
        print(e)





connection.register_packet_listener(
    print_chat, clientbound.play.ChatMessagePacket)

connection.connect()

threading.Thread(target = console_input).start()

client = discord.Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.author.bot == True:
        return

    elif str(message.channel.id) == CHANNEL:

        author = message.author
        roles = author.roles
        content = message.content
        await message.delete()
        for i in roles:
            if i.colour == discord.Color.blue():
                ignname = i.name
        packet = serverbound.play.ChatPacket()
        packet.message = "/cc " + ignname + ": " + content
        connection.write_packet(packet)
        avatar = "https://mc-heads.net/avatar/"+str(ignname)
        await write_chat(ignname, content, avatar)
        print(ignname + ": " + content)
client.run(TOKEN)

'''
while True:
        try:
            text = input()
            if text == "/respawn":
                print("respawning...")
                packet = serverbound.play.ClientStatusPacket()
                packet.action_id = serverbound.play.ClientStatusPacket.RESPAWN
                connection.write_packet(packet)
            else:
                packet = serverbound.play.ChatPacket()
                packet.message = text
                connection.write_packet(packet)
        except KeyboardInterrupt:
            print("Bye!")
            sys.exit()
'''
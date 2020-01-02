from datetime import datetime
import discord, json, discord.ext.commands
from discord import Webhook, AsyncWebhookAdapter
from discord.ext.commands import Bot, check
import discord.ext.commands
import mojang_api
import aiohttp, requests, traceback, sys
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from time import sleep

with open("config.json", encoding="utf-8") as json_file:
    config = json.load(json_file)
    TOKEN = config['token']
    CHANNEL = config['channelID']
    webhook_url = config['webhook']
    custom_answers = config["custom"]

bot = Bot("-")

@bot.event
async def on_command_error(ctx, error):
    error = getattr(error, 'original', error)

    if isinstance(error, discord.ext.commands.errors.CheckFailure):
        return

    #print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
    traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

@bot.listen("on_message")
async def sync(message):
    if message.author.bot == True:
        return
    if message.author == bot.user:
        return
    if str(message.channel.id) == CHANNEL:

        author = message.author
        roles = author.roles
        content = message.content
        for i in roles:
            if i.colour == discord.Color.blue():
                ignname = i.name

        print(ignname + ": " + content)
        await message.delete()
        avatar = "https://mc-heads.net/avatar/"+str(ignname)
        await write_chat(ignname, content, avatar)

def check_channel(ctx):
    if str(ctx.message.channel.id) == CHANNEL:
        return False
    else:
        return True

@bot.command()
@check(check_channel)
async def verify(ctx, role_name, member: discord.Member):
    if ctx.message.author.guild_permissions.administrator:
        await discord.Guild.create_role(ctx.message.author.guild, name=role_name, colour=discord.Color.blue(),
                                        hoist=False, mentionable=False)
        # member = discord.utils.get(message.guild.members, name = message.content.split(" ")[2])

        role = discord.utils.get(member.guild.roles, name=role_name)

        await member.add_roles(role)

        await ctx.send(ctx.message.content.split(" ")[2] + " hat nun die Rolle '" + role_name + "'.")

    else:
        await ctx.send("Du hast nicht genug Rechte.")

@bot.command()
async def kills(ctx, ign):
    try:
        url = 'https://www.gommehd.net/player/index?playerName=' + ign
        response = requests.get(url)

        soup = BeautifulSoup(response.text, "html.parser")
        gungame = soup.find("div", {"id": "gungame"})
        score = gungame.find('span', attrs={'class': 'score'})

        await ctx.send("Kills von " + str(ign) + ": " + score.text)
        if str(ctx.message.channel.id) == CHANNEL:
            print("Kills von " + str(ign) + ": " + score.text)
    except Exception as e:
        await ctx.send("Etwas ist schief gelaufen :/")
        print(e)

@bot.command()
async def nh(ctx, ign):

    def check(m):
        return m.author.bot
    nh = mojang_api.get_username_history(ign)
    nh = json.dumps(nh)
    nh = json.loads(nh)

    counter = 0
    msg = ""

    for i in nh:
        counter += 1

        if nh[0] == i:
            msg += str(counter) + ". " +i["name"] + "\n"
        else:
            dt = datetime.fromtimestamp(i["changedToAt"] / 1000)
            msg += str(counter) + ". " + i["name"] + " (" + dt.strftime('%d/%m/%Y') + ")\n"

    if str(ctx.message.channel.id) == CHANNEL:
        await bot.wait_for("message", check=check)
    await ctx.send(msg)
    if str(ctx.message.channel.id) == CHANNEL:
        print(msg)

@bot.command()
async def set(ctx, trigger, answer):
    with open("config.json", encoding="utf-8") as json_file:
        config = json.load(json_file)
        custom_answers = config["custom"]
        skip = False
        for i in custom_answers:
            if i["name"].lower() == trigger.lower():
                i["answer"] = answer
                skip = True
        if skip == False:
            custom_answers.append({"name": trigger,
                                   "answer": answer})
        config["custom"] = custom_answers
    jsonFile = open("config.json", "w+")
    jsonFile.write(json.dumps(config))
    jsonFile.close()

async def write_chat(ignname, content, avatar):
    url = urlparse(avatar)
    async with aiohttp.ClientSession() as session:
        webhook = Webhook.from_url(webhook_url, adapter=AsyncWebhookAdapter(session))
        await webhook.send(content, username=ignname, avatar_url=url.geturl())

bot.run(TOKEN)
import os
import discord
from discord import Intents
from dotenv import load_dotenv
from time import time

banned_list = []
strikes_list = {}
max_strikes = 3
timeout = 1

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client(intents=Intents.all())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord')

@client.event
async def on_message(message: discord.Message):
    if message.author == client.user:
        return

    if '!words add' in message.content:
        words = message.content[10:].split()
        for word in words:
            banned_list.append(word)
            await message.channel.send(f'{word} added to banned words list')

    if message.content == '!words list':
        await message.channel.send(banned_list)

    if '!words set strikes' in message.content:
        max_strikes = (int)(message.content[17:])

    if '!actions' in message.content:
        if 'edit strikes' in message.content[8:]:
            pass
        if 'edit max strikes' in message.content[8:]:
            pass

    if message.content in banned_list:
        if message.author.name not in strikes_list:
            strikes_list[message.author.name] = 0
        strikes_list[message.author.name] += 1
        await message.channel.send(f'{message.author.name} has been given a strike')
        if strikes_list[message.author.name] < max_strikes:
            action = punishments['strikes']
            handle(action, message.author)
        elif strikes_list[message.author.name] == max_strikes:
            action = punishments['strikes_max']
            handle(action, message.author)
        await message.delete()

async def handle(action, member: discord.Member):
    action(member)

async def ban(member: discord.Member):
    await member.ban()

async def timeout(member: discord.Member):
    currTime = round(time() * 1000)
    await member.timeout(currTime + (timeout * 3600000))

punishments = {
    'strikes': timeout,
    'strikes_max': ban
}

client.run(TOKEN)

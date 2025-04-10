from dotenv import load_dotenv
import os
import discord
from discord import Intents

banned_list = []
strikes_list = {}

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client(intents=Intents.all())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if '!words add' in message.content:
        words = message.content[10:].split()
        for word in words:
            banned_list.append(word)
            await message.channel.send(f'{word} added to banned words list')

    if message.content == '!words list':
        await message.channel.send(banned_list)

    if message.content in banned_list:
        if message.author.name not in strikes_list:
            strikes_list[message.author.name] = 0
        strikes_list[message.author.name] += 1
        await message.channel.send(f'{message.author.name} has been given a strike')
        if strikes_list[message.author.name] < 3:
            pass
        elif strikes_list[message.author.name] == 3:
            ban(message.author)
        await message.delete()

async def ban(member : discord.Member):
    await member.ban()

client.run(TOKEN)

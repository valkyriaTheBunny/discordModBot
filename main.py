from dotenv import load_dotenv
import os
import discord
from discord import Intents

banned_list = []
punishments = {
    'strikes': 'timeout',
    'strikes_max': 'ban'
}
strikes_list = {}
max_strikes = 3

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

    if '!words set strikes' in message.content:
        max_strikes = (int)(message.content[17:])

    if '!actions' in message.content:
        pass

    if message.content in banned_list:
        if message.author.name not in strikes_list:
            strikes_list[message.author.name] = 0
        strikes_list[message.author.name] += 1
        await message.channel.send(f'{message.author.name} has been given a strike')
        if strikes_list[message.author.name] < max_strikes:
            pass
        elif strikes_list[message.author.name] == max_strikes:
            pass
        await message.delete()

async def ban(member : discord.Member):
    await member.ban()

client.run(TOKEN)

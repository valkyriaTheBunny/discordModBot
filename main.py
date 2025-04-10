import os
import discord
import datetime
from discord import Intents
from dotenv import load_dotenv

banned_list = []
strikes_list = {}
max_strikes = 3
time_out = 1

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
client = discord.Client(intents=Intents.all())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord')

@client.event
async def on_message(message: discord.Message):
    global max_strikes
    global time_out

    if message.author == client.user:
        return

    if message.content == '!myperms':
        perms = message.channel.guild.me.guild_permissions
        formatted = [f"✅ {name}" if value else f"❌ {name}" for name, value in perms]
        perm_list = "\n".join(formatted)

        embed = discord.Embed(
            title=f"Permissions for {client.user.name}",
            description=perm_list,
            color=discord.Color.blue())

        await message.channel.send(embed=embed)

    if '!words add ' in message.content:
        words = message.content[10:].split()
        for word in words:
            banned_list.append(word)
            await message.channel.send(f'{word} added to banned words list')

    if message.content == '!words list':
        await message.channel.send(banned_list)

    if '!words set strikes ' in message.content:
        max_strikes = (int)(message.content[17:])

    if '!actions ' in message.content:
        msg = message.content
        channel = message.channel
        if 'edit strikes ' in msg[8:] and 'edit max strikes ' not in msg[8:]:
            if 'days' in msg or 'day' in msg:
                end = msg.index('day')
                time_out = ((int)(msg[21: end])) * 24
            if 'hrs' in msg or 'hr' in msg:
                end = msg.index('hr')
                time_out = ((int)(msg[21: end]))
            if 'mins' in msg or 'min' in msg:
                end = msg.index('min')
                time_out = ((int)(msg[21: end])) / 60
            await channel.send(f'Timeout set to {msg[21:]}')
        if 'edit max strikes ' in msg[8:]:
            punishments['strikes_max'] = msg[25:]
            await channel.send(f'Max strike punishment set to {msg[25:]}')

    if message.content in banned_list:
        if message.author.name not in strikes_list:
            strikes_list[message.author.name] = 0
        strikes_list[message.author.name] += 1
        await message.channel.send(f'{message.author.name} has been given a strike')

        if strikes_list[message.author.name] == max_strikes:
            action = punishments['strikes_max']
            await handle(action, message.author)
        await message.delete()

async def handle(action, member: discord.Member):
    await action(member)

async def ban(member: discord.Member):
    await member.ban()

async def kick(member: discord.Member):
    await member.kick()

async def timeout(member: discord.Member):
    await member.timeout(datetime.timedelta(milliseconds=(time_out * 3600000)))

punishments = {
    'strikes': timeout,
    'strikes_max': ban
}

client.run(TOKEN)

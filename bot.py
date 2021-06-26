import os
import discord
from discord.ext import commands
from settings import token, bot_name, prefix
import asyncio
from datetime import datetime
import time
import random

intents = discord.Intents.default()
intents.members = True


client = commands.Bot(command_prefix=prefix, case_insensitive=True, intents=intents)
client.remove_command("help")


async def change_status():
    await client.wait_until_ready()
    print(f"[{bot_name}] All cogs loaded. Ready to use.")

    while client.is_ready():
        status = discord.Activity(name=f"time go by. | {prefix}help", type=discord.ActivityType.watching)
        await client.change_presence(activity=status)
        await asyncio.sleep(300)


def check_time():
    if datetime.now().minute == 0:
        return True
    return False


async def find_channels():
    for guild in client.guilds:
        active_voice_channels = []
        for voice_channel in guild.voice_channels:
            if len(voice_channel.members) > 0:
                active_voice_channels.append(voice_channel)

        if len(active_voice_channels) > 0:
            await play_sound(guild, random.choice(active_voice_channels))

    guilds_playing_audio = client.guilds

    while True:
        bot_is_playing_sound = False
        for guild in guilds_playing_audio:
            voice = discord.utils.get(client.voice_clients, guild=guild)

            if voice is not None:
                if voice.is_playing():
                    bot_is_playing_sound = True
                else:
                    await voice.disconnect()
                    guilds_playing_audio.remove(guild)

        if not bot_is_playing_sound:
            break
        time.sleep(3)


async def play_sound(guild, voice_channel):
    try:
        await voice_channel.connect()
        voice = discord.utils.get(client.voice_clients, guild=guild)

        if os.path.exists(f"sounds/{guild.id}.mp3"):
            sound_id = guild.id
        else:
            sound_id = 0

        voice.play(discord.FFmpegOpusAudio(f"sounds/{sound_id}.mp3"))
    except Exception:
        print(f"Error in {guild} in {voice_channel.name}")


async def big_ben():
    await client.wait_until_ready()
    while client.is_ready():
        if check_time():
            await find_channels()
            await asyncio.sleep(40)
        await asyncio.sleep(3)


for filename in os.listdir(f'./cogs'):
    if filename.endswith('.py'):
        print(f"[{bot_name}] cogs.{filename[:-3]}: OK")
        client.load_extension(f'cogs.{filename[:-3]}')

client.loop.create_task(change_status())
client.loop.create_task(big_ben())
client.run(token)

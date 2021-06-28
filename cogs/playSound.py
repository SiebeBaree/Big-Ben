import discord
from discord.ext import commands
import time
import os
from settings import embedcolor
from mutagen.mp3 import MP3
from errors import Error


class PlaySound(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="play-sound")
    @commands.cooldown(1, 60, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def play_sound(self, ctx):
        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if voice is not None:
            await ctx.send(":x: I am already in a voice channel.")
            return

        if ctx.author.voice is None:
            voice_channel = None
        else:
            voice_channel = ctx.author.voice.channel

        if voice_channel is None:
            await ctx.send(":x: You are not connected to a voice channel.")
            return

        voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if voice is None:
            await voice_channel.connect()
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)
        elif not voice.is_connected():
            await voice_channel.connect()
            voice = discord.utils.get(self.client.voice_clients, guild=ctx.guild)

        if os.path.exists(f"sounds/{ctx.guild.id}.mp3"):
            sound_id = ctx.guild.id
        else:
            sound_id = 0

        voice.play(discord.FFmpegOpusAudio(f"sounds/{sound_id}.mp3"))

        audio = MP3(f"sounds/{sound_id}.mp3")
        audio_length = audio.info.length

        if audio_length > 25:
            audio_length = 25

        time.sleep(audio_length + 0.5)  # to make sure the sound has ended

        await voice.disconnect()

    @play_sound.error
    async def play_sound_error(self, ctx, error):
        error_class = Error(ctx, error, self.client)
        await error_class.error_check()


def setup(client):
    client.add_cog(PlaySound(client))

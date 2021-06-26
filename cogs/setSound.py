from discord.ext import commands
import os
from mutagen.mp3 import MP3
import time
from settings import embedcolor
import discord


class SetSound(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def sound(self, ctx):
        if str(ctx.message.attachments) == "[]":
            await ctx.send(":x: You have to upload a file (.mp3) to this command.")
            ctx.command.reset_cooldown(ctx)
            return

        if ctx.message.attachments[0].size > 512000:
            await ctx.send(":x: The file is larger than 512kb, we do not allow files bigger than 512kb.")
            ctx.command.reset_cooldown(ctx)
            return
        split_filename = str(ctx.message.attachments).split("filename='")[1]
        bestandsnaam = str(split_filename).split("' ")[0]

        if bestandsnaam.lower().endswith(".mp3"):
            pass
        else:
            await ctx.send(":x: The file needs to have the extension `.mp3`. Other filetypes are not supported.")
            ctx.command.reset_cooldown(ctx)
            return

        await ctx.message.attachments[0].save(f"cache/{ctx.guild.id}.mp3")

        audio = MP3(f"cache/{ctx.guild.id}.mp3")
        audio_length = audio.info.length

        try:
            os.remove(f"cache/{ctx.guild.id}.mp3")
        except Exception:
            pass

        if audio_length > 25:
            await ctx.send(":x: Your audio file is too long. We currently only allow audio files of maximum 25 seconds.")
            return

        try:
            os.remove(f"sounds/{ctx.guild.id}.mp3")
        except Exception:
            pass

        await ctx.message.attachments[0].save(f"sounds/{ctx.guild.id}.mp3")

        await ctx.send(":white_check_mark: Sound succesfully saved.")

    @sound.error
    async def sound_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            error_time = error.retry_after

            if error_time >= 3600:
                error_time_left = time.strftime("%-Hu %-Mm %-Ss", time.gmtime(error_time))
            elif error_time >= 60:
                error_time_left = time.strftime("%-Mm %-Ss", time.gmtime(error_time))
            else:
                error_time_left = round(error_time, 1)

            embed = discord.Embed(
                description=f":x: You have to wait {round(error_time_left, 1)} seconds to use this command again.",
                color=embedcolor
            )
            await ctx.send(embed=embed)
        else:
            raise error


def setup(client):
    client.add_cog(SetSound(client))

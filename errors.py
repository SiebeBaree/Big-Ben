import discord
from discord.ext import commands
from settings import embedcolor
import time


class Error:

    def __init__(self, ctx=None, error=None, client=None):
        self.ctx = ctx
        self.error = error
        self.client = client

    async def error_check(self):
        if self.error is None:
            return
        elif self.ctx is None:
            raise self.error
        else:
            if isinstance(self.error, commands.CommandOnCooldown):
                await self.cooldown()
            elif isinstance(self.error, commands.MemberNotFound):
                await self.member_not_found()
            elif isinstance(self.error, commands.MissingRequiredArgument):
                await self.arguments()
            elif isinstance(self.error, commands.ChannelNotFound):
                await self.channel_not_found()
            elif isinstance(self.error, commands.RoleNotFound):
                await self.role_not_found()
            elif isinstance(self.error, commands.MissingPermissions):
                await self.no_perms("member")
            elif isinstance(self.error, commands.BotMissingPermissions) or isinstance(self.error, commands.CommandInvokeError):
                await self.no_perms()
            else:
                raise self.error

    async def cooldown(self):
        error_time = self.error.retry_after

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
        await self.ctx.send(embed=embed)

    async def arguments(self):
        await self.ctx.send(":x: Invalid Arguments.")

    async def no_perms(self, userclient="bot"):
        if userclient == "bot":
            await self.ctx.send(":x: I don't have enough permissions.")
        elif userclient == "member":
            await self.ctx.send(":x: You don't have enough permissions to execute this command.")

    async def member_not_found(self):
        await self.ctx.send(":x: Member not found.")

    async def channel_not_found(self):
        await self.ctx.send(":x: The channel was not found.")

    async def role_not_found(self):
        await self.ctx.send(":x: The role was not found.")

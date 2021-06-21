from discord.ext import commands
import settings


class OnGuildRemove(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        print(f"[{settings.bot_name}] The bot was removed from {guild}.")


def setup(client):
    client.add_cog(OnGuildRemove(client))

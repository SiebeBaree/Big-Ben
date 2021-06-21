from discord.ext import commands
import settings


class OnGuildJoin(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        print(f"[{settings.bot_name}] The bot was invited to {guild}.")


def setup(client):
    client.add_cog(OnGuildJoin(client))

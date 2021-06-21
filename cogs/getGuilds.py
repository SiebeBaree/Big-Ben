from discord.ext import commands


class GetGuilds(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="guilds")
    @commands.is_owner()
    async def guilds(self, ctx):
        await ctx.author.send(f"Guilds: {len(self.client.guilds)}\n"
                              f"Users: {len(self.client.users)}")


def setup(client):
    client.add_cog(GetGuilds(client))

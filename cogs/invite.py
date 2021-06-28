from discord.ext import commands


class InviteCmd(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def invite(self, ctx):
        await ctx.send(f":link: Invite me here: [Click Here](https://discord.com/api/oauth2/authorize?client_id=855874055077232661&permissions=3198016&redirect_uri=https%3A%2F%2Fdiscord.gg%2FY43Ydu446p&scope=bot)")


def setup(client):
    client.add_cog(InviteCmd(client))

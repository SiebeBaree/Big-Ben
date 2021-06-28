import discord
from discord.ext import commands
from settings import embedcolor, footer, bot_name


class GetHelp(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(name="help")
    async def help_cmd(self, ctx):
        embed = discord.Embed(
            title=f"{bot_name} Help Page",
            color=embedcolor
        )
        embed.add_field(name="About the bot", value="This bot is made for fun to let you know when an hour has passed.\n"
                                                    "Every hour the bot will join every active voice call en play a bell sound.", inline=False)
        embed.add_field(name="Admin Commands", value="`sound <sound-file>`\nUpload a `.mp3` file and use it as the sound every hour.\n\n__Some restrictions:__\n- Only `.mp3` is supported\n- 25 seconds maximum\n- 512KB Maximum filesize\n\n"
                                                     "`prefix <prefix>`\nChange the prefix of the bot in your server.\n\n"
                                                     "`play-sound`\nPlay the current sound to check if you like it.", inline=False)
        embed.add_field(name="General Commands", value=f"`help`\nGet the help message.\n\n"
                                                       f"`invite`\nGet an invite link to invite the bot.\n\n"
                                                       f"To check the prefix use: <@!{self.client.user.id}> prefix", inline=False)
        embed.set_footer(text=footer)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(GetHelp(client))

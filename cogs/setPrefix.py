import discord
from discord.ext import commands
from settings import host, user, passwd, database, embedcolor, footer
import mysql.connector
import re
from errors import Error


class SetPrefix(commands.Cog):
    max_lengte = 5

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, prefix=None):
        if prefix is not None:
            lengte_prefix = len(prefix)

            if lengte_prefix <= self.max_lengte:
                regex = re.sub(r'[^A-Za-z!~,.<>^/$%=+-]', '', prefix)

                if prefix == regex:
                    db = mysql.connector.connect(host=host, database=database, user=user, passwd=passwd)
                    cursor = db.cursor()

                    cursor.execute(f"SELECT * FROM guildSettings WHERE guild = %s", (message.guild.id,))
                    settings = cursor.fetchone()

                    if settings is None:
                        record = (ctx.guild.id, prefix)
                        cursor.execute("INSERT INTO guildSettings (guild, prefix) VALUES (%s, %s)", record)
                    else:
                        cursor.execute(f"UPDATE guildSettings SET prefix = %s WHERE guild = %s", (prefix, ctx.guild.id))
                    db.commit()

                    db.close()

                    embed = discord.Embed(
                        description=f"You've updated the prefix to `{regex}`",
                        color=embedcolor
                    )
                    embed.set_author(name=self.client.user.display_name, icon_url=self.client.user.avatar_url)
                    embed.set_footer(text=footer)
                    await ctx.send(embed=embed)
                else:
                    valid_chars = "`A-Z`, `a-z`, `!`, `<`, `>`, `~`, `.`, `,`, `^`, `-`, `$`, `/`, `%`, `+`, `=`"
                    await ctx.send(f"Prefix contains invalid characters.\nValid characters are:\n{valid_chars}")
            else:
                await ctx.send(f"The prefix is limited to a maximum of {self.max_lengte} characters.")
        else:
            await ctx.send("Invalid Arguments.")

    @prefix.error
    async def prefix_error(self, ctx, error):
        error_class = Error(ctx, error, self.client)
        await error_class.error_check()


def setup(client):
    client.add_cog(SetPrefix(client))

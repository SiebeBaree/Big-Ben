from discord.ext import commands
from settings import host, user, passwd, database, prefix
import mysql.connector


class GetPrefix(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            if message.content == f"<@!{self.client.user.id}> prefix":
                db = mysql.connector.connect(host=host, user=user, passwd=passwd, database=database)
                cursor = db.cursor()

                cursor.execute("SELECT prefix FROM guildSettings WHERE guild = %s", (message.guild.id,))
                prefix_tuple = cursor.fetchone()

                db.close()

                if prefix_tuple is None:
                    guild_prefix = prefix
                else:
                    guild_prefix = prefix_tuple[0]

                await message.channel.send(f"The prefix of this bot is `{guild_prefix}`\n"
                                           f"If you want to see all commands, please use `{guild_prefix}help`!")


def setup(client):
    client.add_cog(GetPrefix(client))

from discord import Embed
from discord.ext import commands

from notebooks import db

SERVER_QUERY = "insert into discord_server values (%s, %s, %s, %s) on conflict (server_cod)" \
               "do update set name = %s, img_url = %s, settings = %s where discord_server.server_cod=%s"
SERVER_SELECT = "select * from discord_server where server_cod=%s"
SERVER_DROP = "delete from discord_server where server_cod=%s;"

class ServerData(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        guild = message.guild
        if guild is None or message.author == self.client.user:
            return
        if message.content.startswith('$new_game'):
            db.make_query(SERVER_DROP, [guild.id])
            settings = " ".join(message.content.split()[1:])
            values = (guild.id, guild.name, str(guild.icon_url), settings, guild.name, str(guild.icon_url), settings, guild.id)
            db.make_query(SERVER_QUERY, values)
            await message.channel.send("It's time to D-D-D-D-D-D-D-D-D-D Duel")
            
        if message.content.startswith('$end_game'):
            db.make_query(SERVER_DROP, [guild.id])
            await message.channel.send("Oh no! Done!")
            
        if message.content.startswith('$game_status'):
            row = db.make_select(SERVER_SELECT, [guild.id])
            if len(row) == 0:
                await message.channel.send("No game running")
            else:
                row = row[0]
                embed = Embed(title='YGO Progression Game!', colour=0xFF0000)
                embed.add_field(name='Settings:', value=row['settings'])
                embed.set_author(name=row['name'], icon_url=row['img_url'])
                await message.channel.send(embed=embed)
            

def setup(bot):
    bot.add_cog(ServerData(bot))


if __name__ == "__main__":
    r = db.make_select(SERVER_SELECT, [1])
    print(r)
    # print(r[0]['name'])
import os

from discord import Embed
from discord.ext import commands

from notebooks.dao import discord_server_dao, player_dao


class ServerData(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author
        guild = message.guild
        if guild is None or message.author == self.client.user:
            return
        if user.guild_permissions.administrator:
            if message.content.startswith('$new_game'):
                discord_server_dao.insert_discord_server(guild.id, guild.name, str(guild.icon_url), '{}')
                await message.channel.send("It's time to D-D-D-D-D-D-D-D-D-D Duel")
                
            if message.content.startswith('$end_game'):
                print(guild.id)
                discord_server_dao.drop_discord_server(guild.id)
                await message.channel.send("Oh no! Done!")
                
            if message.content.startswith('$game_status'):
                server = discord_server_dao.get_discord_server(guild.id)
                if server is None:
                    await message.channel.send("No game running")
                else:
                    player_count = player_dao.get_player_count_by_server(guild.id)
                    embed = Embed(title='YGO Progression Game!', colour=0xFF0000)
                    embed.add_field(name='Players:', value=f"{player_count} / {os.environ['MAX_PLAYER_COUNT']}")
                    embed.add_field(name='Settings:', value=server.settings)
                    embed.set_author(name=server.name, icon_url=server.img_url)
                    await message.channel.send(embed=embed)
            

def setup(bot):
    bot.add_cog(ServerData(bot))

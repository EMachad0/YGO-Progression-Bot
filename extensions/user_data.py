import os

from discord import Embed
from discord.ext import commands

from notebooks.dao import discord_user_dao, player_dao, opening_dao

MAX_PLAYER_COUNT = int(os.environ['MAX_PLAYER_COUNT'])


class UserData(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author
        guild = message.guild
        if guild is None or message.author == self.client.user:
            return
        if message.content.startswith('$enter'):
            player_count = player_dao.get_player_count_by_server(guild.id)
            if player_count >= MAX_PLAYER_COUNT:
                await message.channel.send("Player limit reached!")
                return
            discord_user_dao.insert_discord_user(user.id, user.name, user.discriminator, str(user.avatar_url))
            player_dao.insert_player(user.id, guild.id)
            await message.add_reaction('✅')
                
        if message.content.startswith('$exit'):
            discord_user_dao.drop_discord_user(user.id)
            await message.add_reaction('✅')
        
        if message.content.startswith('$status'):
            discord_user = discord_user_dao.get_discord_user(user.id)
            player = player_dao.get_player_by_user_server(user.id, guild.id)
            if discord_user is None or player is None:
                await message.channel.send("Not a player")
            else:
                openings = opening_dao.get_player_available_openings(player.player_cod)
                to_open = "\n".join(f"{op.set_cod}: {op.quantity}" for op in openings) if len(openings) > 0 else "Nothing!"
                
                embed = Embed(colour=0xFF0000)
                embed.add_field(name='Packs to open:', value=to_open, inline=False)
                embed.add_field(name='Collection:', value=f"https://ygo-prog-web-front.herokuapp.com/#/collection/{guild.id}/{user.id}", inline=False)
                embed.set_author(name=discord_user.name, icon_url=discord_user.img_url)
                await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(UserData(bot))

import os

from discord import Embed
from discord.ext import commands

from notebooks.dao import discord_server_dao, player_dao


class ServerData(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def new_game(self, ctx):
        guild = ctx.guild
        discord_server_dao.insert_discord_server(guild.id, guild.name, str(guild.icon_url), '{}')
        await ctx.send("It's time to D-D-D-D-D-D-D-D-D-D Duel")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def end_game(self, ctx):
        discord_server_dao.drop_discord_server(ctx.guild.id)
        await ctx.send("Oh no! Done!")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def game_status(self, ctx):
        server = discord_server_dao.get_discord_server(ctx.guild.id)
        if server is None:
            await ctx.send("No game running")
        else:
            player_count = player_dao.get_player_count_by_server(ctx.guild.id)
            embed = Embed(title='YGO Progression Game!', colour=0xFF0000)
            embed.add_field(name='Players:', value=f"{player_count} / {os.environ['MAX_PLAYER_COUNT']}")
            embed.add_field(name='Settings:', value=server.settings)
            embed.set_author(name=server.name, icon_url=server.img_url)
            await ctx.send(embed=embed)

    @new_game.error
    @end_game.error
    @game_status.error
    async def server_data_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.message.add_reaction('❌')
        else:
            raise error


def setup(bot):
    bot.add_cog(ServerData(bot))

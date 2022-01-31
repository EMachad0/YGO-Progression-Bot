import os

from discord import Embed
from discord.ext import commands

from notebooks.dao import discord_user_dao, discord_server_dao, player_dao, opening_dao

MAX_PLAYER_COUNT = int(os.environ['MAX_PLAYER_COUNT'])


class UserData(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def enter(self, ctx):
        user = ctx.author
        guild = ctx.guild
        server = discord_server_dao.get_discord_server(ctx.guild.id)
        if server is None:
            await ctx.send("No game running")
            return
        player_count = player_dao.get_player_count_by_server(guild.id)
        if player_count >= MAX_PLAYER_COUNT:
            await ctx.send("Player limit reached!")
            return
        discord_user_dao.insert_discord_user(user.id, user.name, user.discriminator, str(user.avatar_url))
        player_dao.insert_player(user.id, guild.id)
        await ctx.message.add_reaction('✅')

    @commands.command()
    async def exit(self, ctx):
        discord_user_dao.drop_discord_user(ctx.author.id)
        await ctx.message.add_reaction('✅')

    @commands.command()
    async def status(self, ctx):
        user = ctx.author
        guild = ctx.guild
        discord_user = discord_user_dao.get_discord_user(user.id)
        player = player_dao.get_player_by_user_server(user.id, guild.id)
        if discord_user is None or player is None:
            await ctx.send("Not a player")
            return

        openings = opening_dao.get_player_available_openings(player.player_cod)
        to_open = "\n".join(f"{op.set_cod}: {op.quantity}" for op in openings) if len(openings) > 0 else "Nothing!"

        embed = Embed(colour=0xFF0000)
        embed.add_field(name='Packs to open:', value=to_open, inline=False)
        embed.add_field(name='Collection:',
                        value=f"https://ygo-prog-web-front.herokuapp.com/#/collection/{guild.id}/{user.id}",
                        inline=False)
        embed.set_author(name=discord_user.name, icon_url=discord_user.img_url)
        await ctx.send(embed=embed)

    @enter.error
    @exit.error
    @status.error
    async def server_data_error(self, ctx, error):
        print(error)
        await ctx.send("OH NO!!! Something broke pls tell @Machado on\n"
                       "https://discord.com/invite/ztj2kSk")


def setup(bot):
    bot.add_cog(UserData(bot))

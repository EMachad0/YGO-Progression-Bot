import discord
from discord.ext import commands
from discord.ext.commands.errors import *

from notebooks.dao import player_dao, set_dao, opening_dao


class Openings(commands.Cog):

    def __init__(self, client):
        self.client = client
        sets = set_dao.get_all_sets()
        self.__sets = set(s.set_cod for s in sets)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def give_pack(self, ctx, quantity: int, set_cod=None, *p_args: discord.Member):
        if set_cod is None:
            await ctx.send("No set_cod! ex = LOB")
            return
        if set_cod not in self.__sets:
            await ctx.send("Invalid set_cod! ex = LOB")
            return

        valid_players = player_dao.get_players_by_server(ctx.guild.id)
        if len(valid_players) == 0:
            await ctx.send("No player found!")
            return
        if len(p_args) != 0:
            users = {p.user_cod for p in valid_players}
            for user in p_args:
                if user.id not in users:
                    await ctx.send(f"{user.display_name} is not a player!")
                    return

        ids = {p.id for p in p_args}
        players = {p.player_cod for p in valid_players if len(ids) == 0 or p.user_cod in ids}

        values = [{'set_cod': set_cod, 'player_cod': p, 'quantity': quantity} for p in players]
        opening_dao.insert_opening(values, quantity)
        await ctx.message.add_reaction('✅')

    @give_pack.error
    async def openings_error(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument, MissingPermissions, MemberNotFound, BadArgument)):
            await ctx.message.add_reaction('❌')
        else:
            raise error


def setup(bot):
    bot.add_cog(Openings(bot))

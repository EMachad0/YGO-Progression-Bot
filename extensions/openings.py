from discord.ext import commands

from notebooks.dao import player_dao, set_dao, opening_dao


class UserData(commands.Cog):

    def __init__(self, client):
        self.client = client
        sets = set_dao.get_all_sets()
        self.__sets = set(s.set_cod for s in sets)

    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author
        guild = message.guild
        params = message.content.split()
        if guild is None or message.author == self.client.user:
            return
        if user.guild_permissions.administrator:
            if message.content.startswith('$give_pack'):
                set_cod, quantity = params[1:3]
                if set_cod is None:
                    await message.channel.send("No set_cod! ex = LOB")
                    return
                if set_cod not in self.__sets:
                    await message.channel.send("Invalid set_cod! ex = LOB")
                    return
                if quantity is None:
                    await message.channel.send("No quantity! ex = 36")
                    return

                players = player_dao.get_players_by_server(guild.id)
                players = {p.user_cod: p.player_cod for p in players}
                if len(params) > 3:
                    ids = [int(w[3:-1]) for w in params[3:] if w is not None]
                    players = [players[int(user_id)] for user_id in ids if int(user_id) in players]
                else:
                    players = [players[k] for k in players]
                if len(players) == 0:
                    await message.channel.send("No player found!")
                    return

                values = [{'set_cod': set_cod, 'player_cod': p, 'quantity': quantity} for p in players]
                opening_dao.insert_opening(values, quantity)
                await message.add_reaction('✅')

            if message.content.startswith('$give_card'):
                pass


def setup(bot):
    bot.add_cog(UserData(bot))

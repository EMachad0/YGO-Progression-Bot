from discord.ext import commands

from notebooks import db

PLAYER_SELECT = "select player_cod, user_cod from player where server_cod=%s"
SET_SELECT = "select set_cod from set;"
INSERT_OPENING = "insert into opening values (x) " \
                 "on conflict (set_cod, player_cod) do " \
                 "update set quantity=opening.quantity+%s;"


class UserData(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        sets = db.make_select(SET_SELECT, [])
        self.__sets = set(s['set_cod'] for s in sets)

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

                players = db.make_select(PLAYER_SELECT, [guild.id])
                players = {p["user_cod"]: p["player_cod"] for p in players}
                if len(params) > 3:
                    ids = [int(w[3:-1]) for w in params[3:] if w is not None]
                    players = [players[user_id] for user_id in ids if user_id in players]
                else:
                    players = [players[k] for k in players]
                if len(players) == 0:
                    await message.channel.send("No player found!")
                    return

                values = sum(([set_cod, p, quantity] for p in players), []) + [quantity]
                insert_opening = INSERT_OPENING.replace("(x)", ", ".join(["(default, %s, %s, %s)"] * len(players)))
                db.make_query(insert_opening, values)
                await message.add_reaction('✅')
                
            if message.content.startswith('$give_card'):
                pass
            


def setup(bot):
    bot.add_cog(UserData(bot))


if __name__ == "__main__":
    pass
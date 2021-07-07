from discord.ext import commands

from notebooks import db

PLAYER_SELECT = "select player_cod from player p join discord_user du on du.user_cod = p.user_cod where server_cod=%s"
INSERT_OPENING = "insert into opening values (x) " \
                 "on conflict (set_cod, player_cod) do " \
                 "update set quantity=opening.quantity+%s;"


class UserData(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author
        guild = message.guild
        params = message.content.split() + [None] * 5
        if guild is None or message.author == self.client.user:
            return
        if user.guild_permissions.administrator:
            if message.content.startswith('$give_pack'):
                set_cod, quantity = params[1:3]
                who = [(" ".join(i.split("#")[:-1]), i.split("#")[-1]) for i in params[3:] if i is not None]
                if set_cod is None:
                    await message.channel.send("No set_cod! ex = LOB")
                    return
                if quantity is None:
                    await message.channel.send("No quantity! ex = 36")
                    return
                values = [guild.id]
                player_select = PLAYER_SELECT
                if len(who) > 0:
                    values += sum(who, ())
                    player_select += " and (" + " or ".join(f"(name=%s and discriminator=%s)" for _ in who) + ");"
                # print(values, '\n', player_select)
                rows = db.make_select(player_select, values)        
                if len(rows) == 0:
                    await message.channel.send("No player found!")
                    return
                values = sum(([set_cod, p['player_cod'], quantity] for p in rows), []) + [quantity]
                insert_opening = INSERT_OPENING.replace("(x)", ", ".join(["(default, %s, %s, %s)"] * len(rows)))
                # print(values, '\n', insert_opening)
                db.make_query(insert_opening, values)
                await message.add_reaction('✅')
                
            if message.content.startswith('$give_card'):
                pass
            


def setup(bot):
    bot.add_cog(UserData(bot))


if __name__ == "__main__":
    pass
from discord import Embed
from discord.ext import commands
from psycopg2 import IntegrityError


from notebooks import db

USER_QUERY = "insert into discord_user values (%s, %s, %s, %s) on conflict (user_cod)" \
               "do update set name = %s, discriminator = %s, img_url = %s where discord_user.user_cod=%s"
PLAYER_QUERY = "insert into player values (default, %s, %s)"

PLAYER_SELECT = "select * from player p join discord_user du on du.user_cod = p.user_cod where p.user_cod=%s and server_cod=%s;"
PLAYER_DROP = "delete from player where user_cod=%s and server_cod=%s;"

class UserData(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author
        guild = message.guild
        if message.author == self.client.user:
            return
        if message.content.startswith('$enter'):
            values = (user.id, user.name, user.discriminator, str(user.avatar_url), user.name, user.discriminator, str(user.avatar_url), user.id)
            db.make_query(USER_QUERY, values)
            values = (user.id, guild.id)
            try:
                db.make_query(PLAYER_QUERY, values)
                await message.add_reaction('✅')
            except IntegrityError:
                await message.channel.send("Already in game!")
                
        if message.content.startswith('$exit'):
            db.make_query(PLAYER_DROP, (user.id, guild.id))
            await message.add_reaction('✅')
        
        if message.content.startswith('$status'):
            values = (user.id, guild.id)
            row = db.make_select(PLAYER_SELECT, values)
            if len(row) == 0:
                await message.channel.send("Not a player")
            else:
                row = row[0]
                embed = Embed(colour=0xFF0000)
                embed.add_field(name='Info:', value='To do :)')
                embed.set_author(name=row['name'], icon_url=row['img_url'])
                await message.channel.send(embed=embed)


def setup(bot):
    bot.add_cog(UserData(bot))


if __name__ == "__main__":
    pass
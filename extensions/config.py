from discord.ext import commands

from notebooks.dao import config_dao


class ServerData(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author
        guild = message.guild
        params = message.content.split()
        if guild is None or message.author == self.client.user:
            return
        if user.guild_permissions.administrator:
            if message.content.startswith('$config'):
                if len(params) < 3:
                    await message.add_reaction('❌')
                    return
                config = params[1]
                value = " ".join(params[2:])
                if config_dao.validate(config):
                    config_dao.set_config(guild.id, config, value)
                    await message.add_reaction('✅')
                else:
                    await message.add_reaction('❌')


def setup(bot):
    bot.add_cog(ServerData(bot))


if __name__ == "__main__":
    pass
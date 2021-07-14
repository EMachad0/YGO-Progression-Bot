from discord.ext import commands

from notebooks import config_utils


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
                if config_utils.validate(config):
                    config_utils.update_config(guild.id, config, value)
                    await message.add_reaction('✅')
                else:
                    await message.add_reaction('❌')


def setup(bot):
    bot.add_cog(ServerData(bot))

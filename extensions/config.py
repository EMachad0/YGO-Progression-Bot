from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument, MissingPermissions

from notebooks import config_utils


class ServerData(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def config(self, ctx, key, *, value):
        if config_utils.validate(key):
            config_utils.update_config(ctx.guild.id, key, value)
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')

    @config.error
    async def config_error(self, ctx, error):
        if isinstance(error, (MissingRequiredArgument, MissingPermissions)):
            await ctx.message.add_reaction('❌')
        else:
            raise error


def setup(bot):
    bot.add_cog(ServerData(bot))

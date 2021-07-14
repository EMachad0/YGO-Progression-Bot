from io import BytesIO

from discord import File
from discord.ext import commands
from discord.ext.commands.errors import BadArgument

from notebooks import pack_opener, images, config_utils
from notebooks.concat_images import concat_images
from notebooks.dao import player_dao, opening_dao, pull_dao, collection_dao

PACKS_PER_IMAGE = 5


async def send_pack_image(channel, pack):
    for card in pack:
        images.get_img(card['cod_img'])
        images.get_img_small(card['cod_img'])
    paths = [f"data/card_images_small/{card['cod_img']}.jpg" for card in pack]
    with BytesIO() as image_binary:
        concat_images(paths, shape=(len(paths) // 9, 9)).save(image_binary, 'JPEG')
        image_binary.seek(0)
        await channel.send(file=File(fp=image_binary, filename='image.jpg'))


class PackSimulator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pack(self, ctx, quantity: int = 1):
        player = player_dao.get_player_by_user_server(ctx.author.id, ctx.guild.id)
        if player is None:
            await ctx.send("You're Not a player")
            await ctx.message.add_reaction('❌')
            return
        channel = ctx if config_utils.get_config(ctx.guild.id, "private_pack") == "False" else ctx.author
        openings = opening_dao.get_player_available_openings(player.player_cod)

        soma = sum(op.quantity for op in openings)
        if soma == 0:
            await channel.send("You don't have any packs to open!")
            await ctx.message.add_reaction('❌')
            return
        if soma < quantity:
            await channel.send(f"Opening all available {soma} packs!")
        else:
            await channel.send("Opening...")

        collection_values = []
        cards = []
        for op in openings:
            if quantity == 0:
                break
            if op.quantity == 0:
                continue

            set_cards = pull_dao.get_pull_values(op.set_cod)
            card_pool = pack_opener.get_card_pool(set_cards)

            getting = min(quantity, op.quantity)
            opening_dao.update_opening(op.open_cod, {'quantity': op.quantity - getting})
            quantity -= getting

            for _ in range(getting):
                pack = pack_opener.get_random_pack(card_pool)
                collection_values += [{'player_cod': player.player_cod, 'pull_cod': c.pull_cod} for c in pack]
                if len(cards) < 9 * PACKS_PER_IMAGE:
                    cards += pack
                else:
                    await send_pack_image(channel, cards)
                    cards = pack
        if len(cards) > 0:
            await send_pack_image(channel, cards)

        collection_dao.insert_collection(collection_values)
        await ctx.message.add_reaction('✅')

    @pack.error
    async def config_error(self, ctx, error):
        if isinstance(error, BadArgument):
            await ctx.message.add_reaction('❌')
        else:
            raise error


def setup(bot):
    bot.add_cog(PackSimulator(bot))

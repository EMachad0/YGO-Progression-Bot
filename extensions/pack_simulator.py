import json
from io import BytesIO

from discord import File
from discord.ext import commands
from discord.ext.commands.errors import BadArgument

from notebooks import pack_opener, images, config_utils
from notebooks.concat_images import concat_images
from notebooks.dao import player_dao, opening_dao, pull_dao, collection_dao, set_type_dao

PACKS_PER_IMAGE = 5


async def send_pack_image(channel, cards, pack_size):
    for card in cards:
        images.get_img(card['cod_img'])
        images.get_img_small(card['cod_img'])
    paths = [f"data/card_images_small/{card['cod_img']}.jpg" for card in cards]
    with BytesIO() as image_binary:
        concat_images(paths, shape=(len(paths) // pack_size, pack_size)).save(image_binary, 'JPEG')
        image_binary.seek(0)
        await channel.send(file=File(fp=image_binary, filename='image.jpg'))


class PackSimulator(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pack(self, ctx, quantity: int = 1, set_cod=None):
        player = player_dao.get_player_by_user_server(ctx.author.id, ctx.guild.id)
        if player is None:
            await ctx.send("You're Not a player")
            await ctx.message.add_reaction('❌')
            return
        if set_cod is None:
            opening = opening_dao.get_openings_by_player(player.player_cod)
        else:
            opening = opening_dao.get_opening_by_set_player(set_cod, player.player_cod)
        if opening is None:
            await ctx.message.add_reaction('❌')
            await ctx.send("You have no packs available!\n"
                           "The admin must give you packs with the give_pack command first.")
            return
        set_cod = opening.set_cod

        channel = ctx if config_utils.get_config(ctx.guild.id, "private_pack") == "False" else ctx.author

        getting = min(quantity, opening.quantity)
        opening_dao.update_opening(opening.open_cod, {'quantity': opening.quantity - getting})
        await channel.send(f"Opening {getting} pack{'s' if getting == 1 else ''} from {set_cod}!")

        set_cards = pull_dao.get_pull_values(set_cod)
        card_pool = pack_opener.get_card_pool(set_cards)

        rarity_list = json.loads(opening.list)
        collection_values = []
        cards = []
        for _ in range(getting):
            pack = pack_opener.get_random_pack(card_pool, rarity_list)
            collection_values += [{'player_cod': player.player_cod, 'pull_cod': c.pull_cod} for c in pack]
            if len(cards) < opening.num_cards * PACKS_PER_IMAGE:
                cards += pack
            else:
                await send_pack_image(channel, cards, opening.num_cards)
                cards = pack
        if len(cards) > 0:
            await send_pack_image(channel, cards, opening.num_cards)
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

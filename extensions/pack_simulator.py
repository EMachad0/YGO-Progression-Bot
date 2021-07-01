from random import choices
from io import BytesIO

from discord import File
from discord.ext import commands

from notebooks import db
from notebooks.concat_images import concat_images

PACK_QUERY = "select * from card c join (select * from pull where set_cod=%s) p on c.card_cod = p.card_cod;"


async def send_pack_image(channel, pack):
    paths = [f"card_images_small/{card['cod_img']}.jpg" for card in pack]
    with BytesIO() as image_binary:
        concat_images(paths).save(image_binary, 'JPEG')
        image_binary.seek(0)
        await channel.send(file=File(fp=image_binary, filename='image.jpg'))


def get_rarity():
    rarity = ['Super Rare', 'Ultra Rare', 'Secret Rare']
    odds = [9, 2, 1]
    return choices(rarity, weights=odds, k=1)

class PackSimulator(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if message.content.startswith('$pack'):
            await message.channel.send("Opening...")
            rows = db.make_select(PACK_QUERY, ['LOB'])
            pack = choices(rows, k=9)
            await send_pack_image(message.channel, pack)


def setup(bot):
    bot.add_cog(PackSimulator(bot))
    
if __name__ == "__main__":
    rs = db.make_select(PACK_QUERY, ['LOB'])
    for r in rs:
        print(r['name'])
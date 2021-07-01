from io import BytesIO
from random import choices

from discord import File
from discord.ext import commands

from notebooks import db
from notebooks.concat_images import concat_images

PACK_QUERY = "select pull_cod, cod_img from " \
             "(select card_cod, cod_img from card) c join" \
             "(select card_cod, pull_cod from pull where set_cod=%s and rarity=%s) p on c.card_cod = p.card_cod;"
COLLECTION_INSERT = "insert into collection(player_cod, pull_cod) values" \
                    "(%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s), (%s, %s);"
PLAYER_SELECT = "select player_cod from player where user_cod=%s and server_cod=%s;"

async def send_pack_image(channel, pack):
    paths = [f"data/card_images_small/{card['cod_img']}.jpg" for card in pack]
    with BytesIO() as image_binary:
        concat_images(paths).save(image_binary, 'JPEG')
        image_binary.seek(0)
        await channel.send(file=File(fp=image_binary, filename='image.jpg'))


def get_random_rarity():
    rarity = ['Super Rare', 'Ultra Rare', 'Secret Rare']
    odds = [9, 2, 1]
    return choices(rarity, weights=odds, k=1)[0]

def get_random_pack(sett):
    com = db.make_select(PACK_QUERY, (sett, 'Common'))
    rar = db.make_select(PACK_QUERY, (sett, 'Rare'))
    foi = db.make_select(PACK_QUERY, (sett, get_random_rarity()))
    pack = choices(com, k=7) + choices(rar) + choices(foi)
    return pack

class PackSimulator(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        if message.content.startswith('$pack'):
            values = (message.author.id, message.guild.id)
            player = db.make_select(PLAYER_SELECT, values)
            if len(player) == 0:
                await message.channel.send("You're Not a player")
                return
            player = player[0]
            
            await message.channel.send("Opening...")
            pack = get_random_pack('LOB')
            await send_pack_image(message.channel, pack)
            values = sum(((player['player_cod'], c['pull_cod']) for c in pack), ())
            db.make_query(COLLECTION_INSERT, values)


def setup(bot):
    bot.add_cog(PackSimulator(bot))
    
if __name__ == "__main__":
    pk = get_random_pack('LOB')
    val = sum(((6, c['pull_cod']) for c in pk), ())
    db.make_query(COLLECTION_INSERT, val)
    db.make_query(COLLECTION_INSERT, val)

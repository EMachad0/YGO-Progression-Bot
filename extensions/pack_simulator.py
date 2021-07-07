from io import BytesIO

from discord import File
from discord.ext import commands

from notebooks import db, pack_opener
from notebooks.dao import config_dao
from notebooks.concat_images import concat_images

PACK_QUERY = "select pull_cod, cod_img, rarity from " \
             "(select card_cod, cod_img from card) c join" \
             "(select card_cod, pull_cod, rarity from pull where set_cod=%s) p on c.card_cod = p.card_cod;"
OPENING_SELECT = "select open_cod, set_cod, quantity from opening where player_cod=%s;"
OPENING_UPDATE = "update opening set quantity = %s where open_cod=%s;"
COLLECTION_INSERT = "insert into collection(player_cod, pull_cod) values (x);"
PLAYER_SELECT = "select player_cod from player where user_cod=%s and server_cod=%s;"

PACKS_PER_IMAGE = 5


async def send_pack_image(channel, pack):
    paths = [f"data/card_images_small/{card['cod_img']}.jpg" for card in pack]
    # print(paths)
    with BytesIO() as image_binary:
        concat_images(paths, shape=(len(paths)//9, 9)).save(image_binary, 'JPEG')
        image_binary.seek(0)
        await channel.send(file=File(fp=image_binary, filename='image.jpg'))


class PackSimulator(commands.Cog):
    def __init__(self, client):
        self.client = client
        
    @commands.Cog.listener()
    async def on_message(self, message):
        user = message.author
        guild = message.guild
        params = message.content.split() + [None] * 5
        if guild is None or message.author == self.client.user:
            return
        if message.content.startswith('$pack'):
            values = (user.id, guild.id)
            player = db.make_select(PLAYER_SELECT, values)
            if len(player) == 0:
                await message.channel.send("You're Not a player")
                await message.add_reaction('❌')
                return
            channel = message.channel if config_dao.get_config(guild.id, "private_pack") == "False" else user
            player = player[0]['player_cod']
            quantity = int(params[1]) if params[1] else 1
            openings = db.make_select(OPENING_SELECT, [player])
            
            soma = sum(op['quantity'] for op in openings)
            if soma == 0:
                await channel.send("You don't have any packs to open!")
                await message.add_reaction('❌')
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
                if op['quantity'] == 0:
                    continue
                    
                sett = op['set_cod']
                set_cards = db.make_select(PACK_QUERY, [sett])
                card_pool = pack_opener.get_card_pool(set_cards)
                
                getting = min(quantity, op['quantity'])
                db.make_query(OPENING_UPDATE, [op['quantity']-getting, op['open_cod']])
                quantity -= getting
                
                for _ in range(getting):
                    pack = pack_opener.get_random_pack(card_pool)
                    collection_values += sum(([player, c['pull_cod']] for c in pack), [])
                    if len(cards) < 9*PACKS_PER_IMAGE:
                        cards += pack
                    else:
                        await send_pack_image(channel, cards)
                        cards = pack
            if len(cards) > 0:
                await send_pack_image(channel, cards)
                
            collection_insert = COLLECTION_INSERT.replace("(x)", ", ".join(["(%s, %s)"] * (len(collection_values)//2)))
            db.make_query(collection_insert, collection_values)
            await message.add_reaction('✅')


def setup(bot):
    bot.add_cog(PackSimulator(bot))
    
if __name__ == "__main__":
    sc = db.make_select(PACK_QUERY, ['LOB'])
    cp = pack_opener.get_card_pool(sc)
    pk = pack_opener.get_random_pack(cp)
    val = sum(((6, c['pull_cod']) for c in pk), ())
    db.make_query(COLLECTION_INSERT, val)

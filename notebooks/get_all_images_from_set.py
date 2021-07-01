from notebooks import db

import requests
from PIL import Image

IMG_URL='https://storage.googleapis.com/ygoprodeck.com/pics/'
IMG_SMALL_URL='https://storage.googleapis.com/ygoprodeck.com/pics_small/'
PACK_QUERY = "select * from card join (select * from card_set where set_cod=%s) cs on card.card_cod = cs.card_cod;"

def get_img(cod):
    url = f"{IMG_URL}{cod}.jpg"
    image = Image.open(requests.get(url, stream=True).raw)
    image.save(f"data/card_images/{cod}.jpg", 'JPEG')
    
def get_img_small(cod):
    url = f"{IMG_SMALL_URL}{cod}.jpg"
    image = Image.open(requests.get(url, stream=True).raw)
    image.save(f"data/card_images_small/{cod}.jpg", 'JPEG')

def get_all_images_from_set(sets):
    rows = db.make_select(PACK_QUERY, sets)
    for card in rows:
        get_img(card['cod_img'])
        get_img_small(card['cod_img'])
    
if __name__ == '__main__':
    get_all_images_from_set(['LOB'])
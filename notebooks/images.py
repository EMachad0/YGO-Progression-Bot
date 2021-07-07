from os.path import isfile

from notebooks import db

import requests
from PIL import Image

IMG_URL='https://storage.googleapis.com/ygoprodeck.com/pics/'
IMG_SMALL_URL='https://storage.googleapis.com/ygoprodeck.com/pics_small/'
PACK_QUERY = "select cod_img from card join (select card_cod from pull where set_cod=%s) p using(card_cod);"

def get_img(cod, overwrite=False):
    if isfile(f"data/card_images/{cod}.jpg") and not overwrite:
        return
    url = f"{IMG_URL}{cod}.jpg"
    image = Image.open(requests.get(url, stream=True).raw)
    image.save(f"data/card_images/{cod}.jpg", 'JPEG')
    
def get_img_small(cod, overwrite=False):
    if isfile(f"data/card_images_small/{cod}.jpg") and not overwrite:
        return
    url = f"{IMG_SMALL_URL}{cod}.jpg"
    image = Image.open(requests.get(url, stream=True).raw)
    image.save(f"data/card_images_small/{cod}.jpg", 'JPEG')
    
    
def get_all_images_from_set(sett):
    rows = db.make_select(PACK_QUERY, [sett])
    for card in rows:
        get_img(card['cod_img'])
        get_img_small(card['cod_img'])
    
if __name__ == '__main__':
    pass
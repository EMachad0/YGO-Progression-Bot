from os.path import isfile

import requests
from PIL import Image

IMG_BIG_URL= 'https://storage.googleapis.com/ygoprodeck.com/pics/'
IMG_SMALL_URL='https://storage.googleapis.com/ygoprodeck.com/pics_small/'


def get_img(cod, overwrite=False):
    if isfile(f"data/card_images/{cod}.jpg") and not overwrite:
        return
    url = f"{IMG_BIG_URL}{cod}.jpg"
    image = Image.open(requests.get(url, stream=True).raw)
    image.save(f"data/card_images/{cod}.jpg", 'JPEG')

def get_img_small(cod, overwrite=False):
    if isfile(f"data/card_images_small/{cod}.jpg") and not overwrite:
        return
    url = f"{IMG_SMALL_URL}{cod}.jpg"
    image = Image.open(requests.get(url, stream=True).raw)
    image.save(f"data/card_images_small/{cod}.jpg", 'JPEG')

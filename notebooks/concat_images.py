from PIL import Image, ImageOps


def concat_images(paths, size=None, shape=None):
    # Open images and resize them
    images = [Image.open(path) for path in paths]
    width, height = size if size else images[0].size
    # images = [ImageOps.fit(image, size, Image.ANTIALIAS) for image in images]

    # Create canvas for the final image with total size
    shape = shape if shape else (1, len(images))
    image_size = (width * shape[1], height * shape[0])
    image = Image.new('RGB', image_size)

    # Paste images into final image
    for row in range(shape[0]):
        for col in range(shape[1]):
            offset = width * col, height * row
            idx = row * shape[1] + col
            image.paste(images[idx], offset)
    return image


if __name__ == '__main__':
    ids = ['75356564', '36304921', '50913601', '83464209', '37421579', '15025844', '85705804', '9293977', '53293545']
    pth = [f"data/card_images_small/{i}.jpg" for i in ids]
    img = concat_images(pth)
    img.save('image.jpg', 'JPEG')
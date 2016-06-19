"""Image manipulation."""
import collections
import StringIO

from PIL import Image


def data_to_pil(img_data):
    """Return PIL image from image data."""
    img = Image.open(StringIO.StringIO(img_data))
    return img.convert('RGBA')


def pil_to_data(pil_img, extension='PNG'):
    """Return image data from a PIL."""
    sio_out = StringIO.StringIO()
    pil_img.save(sio_out, extension)
    return sio_out.getvalue()


def trim(pil_img, top_px=0, right_px=0, bottom_px=0, left_px=0):
    """Trim pixels around pil image data."""
    width, height = pil_img.size
    box = (left_px, top_px, width - right_px, height - bottom_px)
    return pil_img.crop(box)


def overlay(background, foreground):
    """Does an overlay of PIL images."""
    return Image.alpha_composite(background, foreground)


def clouds(pil_img, size=16):
    """Returns cloud intensity per grid square in the original image.

    Assumes that the image is roughly square.
    """
    width, height = pil_img.size

    cloud_map = Image.new('RGBA', (size, size), None)

    value_map = collections.defaultdict(int)

    for x in range(width):
        for y in range(height):
            pixel = pil_img.getpixel((x, y))
            mapped_x = int((float(x) / width) * size)
            mapped_y = int((float(y) / height) * size)

            if pixel != (0, 0, 0, 0):
                value_map[(mapped_x, mapped_y)] += 1

    grid_size = (width / size) * (height / size)

    for (coord, value) in value_map.items():
        prop_val = int((float(value) / grid_size) * 255)
        cloud_map.putpixel(coord, (0, 0, prop_val))

    return cloud_map.resize(pil_img.size)

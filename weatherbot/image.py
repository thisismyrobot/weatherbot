"""Image manipulation."""
import collections
import StringIO

from PIL import Image


def data_to_pil(img_data):
    """Return PIL image from image data."""
    return Image.open(StringIO.StringIO(img_data))


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


def clouds(pil_img, size=8):
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
            mapped_y = int((float(y) / width) * size)

            if pixel != 31:
                value_map[(mapped_x, mapped_y)] += 1

    max_val = max(value_map.values())

    for (coord, value) in value_map.items():
        val = int((float(value)/max_val) * 255)
        cloud_map.putpixel(coord, (0, 0, val))

    return cloud_map.resize(pil_img.size)

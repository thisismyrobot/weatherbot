"""Image manipulation."""
import StringIO

from PIL import Image


def data_to_pil(img_data):
    """Return PIL image from image data."""
    return Image.open(StringIO.StringIO(img_data))


def pil_to_data(pil_img, extension='PNG'):
    sio_out = StringIO.StringIO()
    pil_img.save(sio_out, extension)
    return sio_out.getvalue()


def trim(pil_img, top_px=0, right_px=0, bottom_px=0, left_px=0):
    """Trim pixels around pil image data."""
    width, height = pil_img.size
    box = (left_px, top_px, width - right_px, height - bottom_px)
    return pil_img.crop(box)


def clouds(pil_img, size=51):
    """Returns cloud locations.

    This is initially done by down-sampling the image to a small size and
    finding non-transparent pixels.

    Assumes that the image is roughly square.
    """
    pil_img_sml = pil_img.resize((size, size), Image.LANCZOS)

    return pil_img_sml.resize(pil_img.size), [p == 31 for p in pil_img_sml.getdata()]

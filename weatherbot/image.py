"""Image manipulation."""
import StringIO

from PIL import Image


def trim(img, top_px=0, right_px=0, bottom_px=0, left_px=0, extension='PNG'):
    """Trim pixels around image data."""
    sio_in = StringIO.StringIO(img)
    img_in = Image.open(sio_in)

    width, height = img_in.size

    box = (
        left_px, top_px,
        width - right_px, height - bottom_px
    )

    print width, height, box

    img_out = img_in.crop(box)

    sio_out = StringIO.StringIO()

    img_out.save(sio_out, extension)

    return sio_out.getvalue()

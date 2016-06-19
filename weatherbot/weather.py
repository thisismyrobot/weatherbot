"""Download weather data from the BOM."""
import datetime
import requests
import urlparse

import image


CDN_ROOT = 'http://ws.cdn.bom.gov.au/radar/'
IMG_TEMPLATE = r'IDR763.T.{}.png'


def _download(filename):
    """Download an image from the CDN, by filename."""
    cdn_url = urlparse.urljoin(CDN_ROOT, filename)
    return requests.get(cdn_url).content


def _prepare_image(img_data):
    """Trim off non-image data."""
    pil_img = image.data_to_pil(img_data)
    pil_img_trimmed = image.trim(pil_img, top_px=16, bottom_px=14)
    return image.pil_to_data(pil_img_trimmed)


def _file_date(start=None, steps=0, step_size=6):
    """Return a file date back a number of steps (zero = most recent), from
    now or a chosen time. Steps are 6 minutes by default.
    """
    if start is None:
        start = datetime.datetime.utcnow()

    # Round minutes down to the nearest 6-minute interval
    start_rounded = start.replace(
        minute=int(start.minute / float(step_size)) * step_size,
        second=0,
        microsecond=0,
    )

    return start_rounded - datetime.timedelta(minutes=steps * step_size)


def filename(start=None):
    """Return the filename to download."""
    file_ts = _file_date(start=start)
    return IMG_TEMPLATE.format(file_ts.strftime('%Y%m%d%H%M'))


def get():
    """Customise to return a radar image of your location when get() is
    called.
    """
    img_filename = filename()
    img = _download(img_filename)
    return _prepare_image(img)

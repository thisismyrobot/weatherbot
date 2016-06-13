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


def _filename():
    """Return the filename to download."""
    utc_ts = datetime.datetime.utcnow()

    # We'd rather get a slightly older than keep missing them.
    utc_ts_old = utc_ts - datetime.timedelta(minutes=6)

    # The images are every 6 minutes
    minutes = int(utc_ts_old.minute / 6) * 6

    file_ts = utc_ts_old.replace(minute=minutes)

    return IMG_TEMPLATE.format(file_ts.strftime('%Y%m%d%H%M'))


def get():
    """Customise to return a radar image of your location when get() is
    called.
    """
    filename = _filename()
    img = _download(filename)
    return _prepare_image(img)

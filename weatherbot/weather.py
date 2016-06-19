"""Download weather data from the BOM."""
import datetime
import requests
import urlparse

import image


CDN_ROOT = 'http://ws.cdn.bom.gov.au/radar/'
IMG_TEMPLATE = r'IDR763.T.{}.png'


def download(filename):
    """Download an image from the BOM CDN, by filename."""
    cdn_url = urlparse.urljoin(CDN_ROOT, filename)
    return requests.get(cdn_url).content


def prepare_image(img_data):
    """Trim off non-image data."""
    pil_img = image.data_to_pil(img_data)
    pil_img_trimmed = image.trim(pil_img, top_px=16, bottom_px=14)
    return image.pil_to_data(pil_img_trimmed)


def file_date(start=None, steps=0, step_size=6):
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


def filename(date):
    """Return the filename to download based on a date."""
    return IMG_TEMPLATE.format(date.strftime('%Y%m%d%H%M'))


def get(steps_back):
    """Return historical radar images."""
    # It takes around 5 mins for the CDN to update so we go back a step to
    # ensure we get an image.
    adjusted_steps = steps_back + 1

    image_datetime = file_date(steps=adjusted_steps)
    image_filename = filename(image_datetime)
    image = download(image_filename)
    return prepare_image(image)

import ftplib
import re
import requests
import urlparse

import image


FTP_DOMAIN = 'ftp2.bom.gov.au'
CDN_ROOT = 'http://ws.cdn.bom.gov.au/radar/'
IMG_ROOT = 'anon/gen/radar/'
IMG_FILTER = r'(IDR763\.T\.(.*)\.png)'


def _download(filename):
    """Download an image from the CDN, by filename."""
    cdn_url = urlparse.urljoin(CDN_ROOT, filename)
    return requests.get(cdn_url).content


def _prepare_image(img_data):
    """Trim off non-image data."""
    pil_img = image.data_to_pil(img_data)
    pil_img_trimmed = image.trim(pil_img, top_px=16, bottom_px=14)
    return image.pil_to_data(pil_img_trimmed)


def get():
    """Customise to return a radar image of your location when get() is
    called.

    May use multiple images in a later iteration, hence the maps etc.
    """
    ftp = ftplib.FTP(FTP_DOMAIN)
    ftp.login()
    matches = filter(None, [re.search(IMG_FILTER, f)
                            for f
                            in ftp.nlst(IMG_ROOT)])

    filenames = [m.groups()[0]
                 for m
                 in sorted(matches, key=lambda m: int(m.groups()[1]))][-1:]

    images = map(_download, filenames)

    return map(_prepare_image, images)[0]

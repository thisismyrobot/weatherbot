import ftplib
import re
import requests
import urlparse


FTP_DOMAIN = 'ftp2.bom.gov.au'
CDN_ROOT = 'http://ws.cdn.bom.gov.au/radar/'
IMG_ROOT = 'anon/gen/radar/'
IMG_FILTER = r'(IDR763\.T\.(.*)\.png)'


def get():
    """Customise to return a radar image of your location when get() is
    called.
    """
    ftp = ftplib.FTP(FTP_DOMAIN)
    ftp.login()
    matches = filter(None, [re.search(IMG_FILTER, f)
                            for f
                            in ftp.nlst(IMG_ROOT)])

    newest_img = sorted(
        matches, key=lambda m: int(m.groups()[1]), reverse=True
    )[0].groups()[0]

    cdn_url = urlparse.urljoin(CDN_ROOT, newest_img)

    return requests.get(cdn_url).content

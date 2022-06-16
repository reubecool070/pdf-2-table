import os

image_url = 'https://www.apmterminals.com/los-angeles/-/media/americas/LA/daily-information/empty-receivables-6-15pm.jpg'
new_path = os.path.dirname(__file__)


def wget(url, download_path):
    return os.system('curl {} -O'.format( url))


wget(image_url, new_path + 'empty-1.jpg')
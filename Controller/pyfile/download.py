import os

image_url = "https://www.apmterminals.com/los-angeles/-/media/americas/LA/daily-information/empty-receivables-6-13.jpg"


# returns 0 if success
def wget(url, download_path):
    return os.system('wget -O {} {}'.format(download_path, url))


print(wget(image_url, 'images/empty-1.jpg'))
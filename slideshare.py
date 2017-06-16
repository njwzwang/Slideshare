# -*- coding: utf-8 -*-
import os
import re

import img2pdf
import requests

from os import listdir, walk
from os.path import isfile, join
from bs4 import BeautifulSoup

CURRENT = os.path.dirname(__file__)


def download_images(url):
    response = requests.get(url)
    print(response.status_code)
    html = response.text
    soup = BeautifulSoup(html)
    title = 'pdf_images'  # soup.title.string
    images = soup.findAll('img', {'class': 'slide_image'})

    for image in images:
        image_url = image.get('data-full').split('?')[0]
        command = 'wget --no-check-certificate %s -P %s' % (image_url, title)
        print(command)
        os.system(command)

    convert_pdf(title)


def sort_by_page(filenames):
    # print(re.findall(r"\d+-\d{4}", myString)[0][:-5])
    return float(re.findall(r"\d+-\d{4}", filenames)[0][:-5])  # return number part in string


def convert_pdf(url):
    f = []
    for (dirpath, dirnames, filenames) in walk(join(CURRENT, url)):
        f.extend(filenames)
        # print(f)
        break

    f.sort(key=sort_by_page)
    print(f)
    f = ["%s/%s" % (url, x) for x in f]

    pdf_bytes = img2pdf.convert(f, dpi=360, x=None, y=None)
    doc = open('result.pdf', 'wb')
    doc.write(pdf_bytes)
    doc.close()


if __name__ == "__main__":
    # url = input('Slideshare URL : ')
    url = 'https://www.slideshare.net/ENGMSHARI/wpa2'
    # url = 'https://www.slideshare.net/NetApp/it-in-healthcare-58990111'
    download_images(url)
    title = 'pdf_images'
    command = 'rmdir /s/q %s' % title
    os.system(command)

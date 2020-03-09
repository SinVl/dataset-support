
import argparse
import os

import numpy as np
import cv2
import requests
from flickrapi import FlickrAPI

key = ''  # Flickr API key https://www.flickr.com/services/apps/create/apply
secret = ''
flickr = FlickrAPI(key, secret, format='parsed-json')
photos = []


def search(search, num_image, num_page, size=None):
    photos = flickr.photos.search(text=search, per_page=num_image, page=num_page)
    images = []
    for i, photo in enumerate(photos["photos"]["photo"]):
        url = photo.get("url_o")
        if url is None:
            url = 'https://farm%s.staticflickr.com/%s/%s_%s_m.jpg' % \
                  (photo.get('farm'), photo.get('server'), photo.get('id'), photo.get('secret'))  # large size
        image_bytes = requests.get(url, stream=True).content
        image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)[:, :, ::-1]
        images.append(image)
    return images


def get_urls(search, num_image, num_page, size=None):
    photos = flickr.photos.search(text=search, per_page=num_image, page=num_page)
    urls = []
    for i, photo in enumerate(photos["photos"]["photo"]):
        url = None                # photo.get("url_o")
        if url is None:
            url = 'https://farm%s.staticflickr.com/%s/%s_%s_m.jpg' % \
                  (photo.get('farm'), photo.get('server'), photo.get('id'), photo.get('secret'))
        urls.append(url)
    return urls


def get_urls_p(search):
    global photos
    photos = flickr.walk(text=search,  # http://www.flickr.com/services/api/flickr.photos.search.html
                         extras='url_o',
                         per_page=100,
                         sort='relevance')


def get_image(search):
    while True:
        for i, photo in enumerate(photos):
            url = None#photo.get("url_o")
            if url is None:
                url = 'https://farm%s.staticflickr.com/%s/%s_%s_-.jpg' % \
                      (photo.get('farm'), photo.get('server'), photo.get('id'), photo.get('secret'))  # large size
            image_bytes = requests.get(url, stream=True).content
            image = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)[:, :, ::-1]
            yield image


def get_urls_t(search='honeybees on flowers', n=10, download=True):
    flickr = FlickrAPI(key, secret)
    photos = flickr.walk(text=search,  # http://www.flickr.com/services/api/flickr.photos.search.html
                         extras='url_o',
                         per_page=100,
                         sort='relevance')

    if download:
        dir = os.getcwd() + os.sep + 'images' + os.sep + search.replace(' ', '_') + os.sep  # save directory
        if not os.path.exists(dir):
            os.makedirs(dir)

    urls = []
    for i, photo in enumerate(photos):
        if i == n:
            break

        try:
            # construct url https://www.flickr.com/services/api/misc.urls.html
            url = photo.get('url_o')  # original size
            if url is None:
                url = 'https://farm%s.staticflickr.com/%s/%s_%s_b.jpg' % \
                      (photo.get('farm'), photo.get('server'), photo.get('id'), photo.get('secret'))  # large size

            # download
            if download:
                with open(dir + url.split('/')[-1], 'wb') as f:
                    f.write(requests.get(url, stream=True).content)

            urls.append(url)
            print('%g/%g %s' % (i, n, url))
        except:
            print('%g/%g error...' % (i, n))

    # import pandas as pd
    # urls = pd.Series(urls)
    # urls.to_csv(search + "_urls.csv")
    print('Done.' + ('\nAll images saved to %s' % dir if download else ''))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--search', type=str, default='honeybees on flowers', help='flickr search term')
    parser.add_argument('--n', type=int, default=10, help='number of images')
    parser.add_argument('--download', action='store_true', help='download images', default=False)
    opt = parser.parse_args()

    # get_urls(search=opt.search,  # search term
    #          n=opt.n,  # max number of images
    #          download=opt.download)  # download images

    # print(search("home", 1, 1))
    print(get_urls("thread", 10, 2))
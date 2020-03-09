from src.flickr import get_urls, get_image, search
from src.utils import image_from_buffer


class ImageProvider:
    def __init__(self):
        self.page = 1
        self.query = None

    def __iter__(self):
        for i in get_image("aggressive dog"):
            yield i

    def send_request(self, query):
        #print(get_urls(query))
        self.query = query

    def get_images(self, n):
        return search(self.query, n, self.page)

    def __getitem__(self, item):
        return get_image()

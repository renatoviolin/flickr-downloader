import flickrapi
import requests
import logging
import os
import csv
from PIL import Image
from io import BytesIO
from hashlib import sha256
import yaml
import numpy as np
import glob
logger = logging.getLogger('uvicorn.error')


class FlickrImageDownload:
    def __init__(self, flickr_id, flickr_secret, path, prefix='no_prefix', update_minutes=1, max_download_count=1000, scale_w=0, scale_h=0, license_allowed=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]):
        self.path = path
        self.prefix = prefix
        self.update_minutes = update_minutes
        self.max_download_count = max_download_count
        self.license_allowed = license_allowed
        self.scale_width = scale_w
        self.scale_height = scale_h
        self.flickr = flickrapi.FlickrAPI(flickr_id, flickr_secret, cache=True)

    def reset_counts(self):
        self.download_count = 0
        self.last_update = 0
        self.download_count = 0
        self.error_count = 0
        self.cached = 0
        self.sources = []

    def load_image(self, url):
        try:
            response = requests.get(url)
            h = sha256(response.content).hexdigest()
            img = Image.open(BytesIO(response.content))
            img.load()
            return img, h
        except:
            logger.warning(f"Unexpected exception while downloading image: {url}", exc_info=True)
            return None, None

    def obtain_photo(self, url):
        url = photo.get('url_c')
        license = photo.get('license')
        if int(license) in self.license_allowed and url:
            image, h = self.load_image(url)
            if image:
                return image
            else:
                self.error_count += 1
        return None

    def check_license(self, photo):
        url = photo.get('url_c')
        license = photo.get('license')
        if int(license) in self.license_allowed and url:
            return url
        return None

    def check_to_keep_photo(self, url, image):
        h = sha256(image.tobytes()).hexdigest()
        p = os.path.join(self.path, f"{self.prefix}-{h}.jpg")
        self.sources.append([url, os.path.basename(p)])
        if not os.path.exists(p):
            self.download_count += 1
            return p
        else:
            self.cached += 1
            return None

    def process_image(self, image, path, scale_w=0, scale_h=0):
        if image.mode not in ('RGB'):
            logger.debug(f"Grayscale to RGB: {path}")
            rgbimg = Image.new("RGB", image.size)
            rgbimg.paste(image)
            image = rgbimg

        if scale_w != 0 and scale_h != 0:
            image = image.resize((scale_w, scale_h))
        return image

    def track_progress(self):
        if self.download_count > self.max_download_count:
            logger.info("Reached max download count")
            return True
        return False

    def write_sources(self):
        logger.info("Writing sources file.")
        filename = os.path.join(self.path, self.prefix + '.csv')
        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(['url', 'file'])
            csvwriter.writerows(self.sources)

    def get_url(self, query, tags, max_download=10):
        tags = ','.join(tags.split(','))
        photos = self.flickr.walk(text=query, tag_mode='all', tags=tags, extras='url_c,license', per_page=100, sort='relevance')
        url_list = []
        for photo in photos:
            url = self.check_license(photo)
            logger.info(url)
            if url:
                url_list.append(url)
            if len(url_list) >= max_download:
                break

        return url_list

    def download_from_url(self, url_list, scale_w, scale_h):
        files = glob.glob(f'{self.path}/{self.prefix}*')
        for f in files:
            os.remove(f)
        self.reset_counts()

        for url in url_list:
            img, h = self.load_image(url)
            if img:
                path = self.check_to_keep_photo(url, img)
                if path:
                    img = self.process_image(img, path, scale_w, scale_h)
                    img.save(path)

            if self.track_progress():
                break

        self.write_sources()

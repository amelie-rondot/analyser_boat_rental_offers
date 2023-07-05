"""
This module defines a web scraper, using the Spider objects from scrapy package,
to get all boat images urls included in a boat rental offer web page,
and save the list of urls as dict in a json file when launching
scrapy `scrapy runspider boat_image_scraper.py -o tmp_images.json` command.
For example, from the web page https://www.clickandboat.com/location-bateau/marseille/semi-rigide/capelli-tempest600-w2bq5d
get these images urls :
- "https://static1.clickandboat.com/v1/p/hz27Zb3hnKrmkyalhZAFvdNOV1dCUiit.big.jpg"
- "https://static1.clickandboat.com/v1/p/QlXEqjdBRTNM8SCvv5b45winhDjFBqci.big.jpg"
- "https://static1.clickandboat.com/v1/p/D5W4eRNXhar51jzjl0AuSs75tLQtuYez.big.jpg"

"""
from scrapy import Spider

from utils import get_url_from_offers_file


class ClickAndBoatOfferImagesSpider(Spider):

    name = "images"

    # url of a boat rental offer
    start_urls = [
        get_url_from_offers_file(),
        #f"https://www.clickandboat.com/location-bateau/marseille/semi-rigide/capelli-tempest600-w2bq5d",
    ]

    def parse(self, response):
        """
        Implements native parse method, to yield a list of images urls of a Click&Boat web offer into a
        temporary json file "images.json"
        :param response:
        :return:
        """
        # <div class="productCover__img js-openGallery"
        # style="background-image: url(//static1.clickandboat.com/v1/p/hz27Zb3hnKrmkyalhZAFvdNOV1dCUiit.big.jpg);"
        #    >...</div>
        # autres photos -> class="productCover__img--small productCover__img--twoImages js-openGallery"

        images = response.css('div.productCover.js-imagesContainer').attrib['data-images']
        urls_images = images.split(";")
        for url_image in urls_images:
            yield {"url_image": f"https:{url_image}"}

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
from scrapy import Request, Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class ClickAndBoatOfferImagesSpider(Spider):

    name = "click_and_boat_images"

    custom_settings = {
        "FEEDS": {
            "tmp_click_and_boat_images.json": {"format": "json"},
        },
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": '2.7',
    }

    def start_requests(self):
        yield Request(f"{self.url}")

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


class SamBoatOfferImagesSpider(Spider):

    name = "sam_boat_images"

    custom_settings = {
        "FEEDS": {
            "tmp_sam_boat_images.json": {"format": "json"},
        },
        "REQUEST_FINGERPRINTER_IMPLEMENTATION": '2.7',
    }

    def start_requests(self):
        yield Request(f"{self.url}")

    def parse(self, response):
        """
        Implements native parse method, to yield a list of images urls of a Click&Boat web offer into a
        temporary json file "images.json"
        :param response:
        :return:
        """
        # <div id="announcement-gallery-modal"">
        #   ...
        #      ...
        #         <div id="announcement-gallery-modal" ...>
        #            ...
        #               <div class="row g-3" ...>
        #                   <div ...>
        #                      <a href="dummy_url_main_photo">
        #                           <img ... src="https://cdn.samboat.fr/announcements/dummy_photo1.jpg" ...>
        #                       </a>
        #                   </div>
        #                   <div ...>
        #                      <a href="dummy_url_main_photo">
        #                           <img ... src="https://cdn.samboat.fr/announcements/dummy_photo2.jpg" ...>
        #                       </a>
        #                   </div>
        #                   ...
        #               </div>
        #            ...
        #        </div>
        #      ...
        #   ...
        # </div>
        all_images_selector = response.css('div#announcement-gallery-modal')
        all_images_sub_selector = all_images_selector.css('div.row.g-3')
        all_images = all_images_sub_selector.css('div a::attr("href")')
        for image in all_images:
            url_image = image.get()
            url_images = {"url_image": f"{url_image}"}
            yield url_images


if __name__ == "__main__":
    from utils import get_url_from_offers_file

    settings = get_project_settings()
    process = CrawlerProcess(settings)
    cnb_offer_url = get_url_from_offers_file("tmp_click_and_boat_offers.json")[1]
    process.crawl(ClickAndBoatOfferImagesSpider, url=cnb_offer_url['url'])
    sb_offer_url = get_url_from_offers_file("tmp_sam_boat_offers.json")[1]
    process.crawl(SamBoatOfferImagesSpider, url=sb_offer_url['url'])
    process.start()

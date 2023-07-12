"""
This module is used as a script to run to save information related to a web rental boat offer such as:
- The url of the offer
- If the boat is rented with skipper services
- The urls of the images of the boat
- The immatriculation number of the boat if it is known
"""

from multiprocessing import Process, Queue

from scrapy import Spider
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

import utils
from boat_images_scraper import ClickAndBoatOfferImagesSpider
from boat_rental_offers_web_scraper import ClickAndBoatOfferSpider, SamBoatOfferSpider
from utils import get_url_from_offers_file


def run_spider(spider_class_name: Spider.__name__, spider_settings: Settings, url: str):
    """This method is used to run multiple spiders,
    see https://stackoverflow.com/questions/41495052/scrapy-reactor-not-restartable"""

    def f(queue: Queue):
        try:
            runner = CrawlerRunner(spider_settings)
            deferred = runner.crawl(spider_class_name, url=url)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            queue.put(None)
        except Exception as e:
            queue.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result


if __name__ == "__main__":

    # Get url offers -> listed in tmp_click_and_boat_offers.json and tmp_sam_boat_offers.json files
    settings = get_project_settings()
    print("Get click_and_boat offers url and stock them into tmp_click_and_boat_offers.json file .....")
    run_spider(ClickAndBoatOfferSpider, settings, '')

    print("Get sam_boat offers url and stock them into tmp_sam_boat_offers.json file .....")
    run_spider(SamBoatOfferSpider, settings, '')

    # For clickandboat (alias cnb)
    cnb_url_offers_list = get_url_from_offers_file("tmp_click_and_boat_offers.json")[4:5]

    for offer_url in cnb_url_offers_list:
        # Get images url for this offer
        print(f" For the offer {offer_url['url']}, get the boat images urls and stock them "
              "into tmp_click_and_boat_images.json file .....")
        run_spider(ClickAndBoatOfferImagesSpider, settings, offer_url['url'])

        images_path_file = "tmp_click_and_boat_images.json"
        images_urls = utils.get_urls_images_from_images_file(images_path_file)

        # TODO: fix adding new objects bug in json file to have a correct json format

        # # Treat images to get boat immatriculation number
        # utils.get_boat_immatriculation_number(images_urls)
        #
        # boat_immatriculation_number = ''
        #
        # # Create BoatRentalOffer object to save it in db
        # new_boat_rental_offer = BoatRentalOffer(boat_immatriculation_number, True, offer_url)

        # TODO: find a solution to save data in db, at first db could be a csv file

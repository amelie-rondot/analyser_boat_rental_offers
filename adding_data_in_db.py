"""
This module is used as a script to run to save information related to a web rental boat offer such as:
- The url of the offer
- If the boat is rented with skipper services
- The urls of the images of the boat
- The immatriculation number of the boat if it is known
"""
import json
from multiprocessing import Process, Queue

from scrapy import Spider
from scrapy.crawler import CrawlerRunner
from scrapy.settings import Settings
from scrapy.utils.project import get_project_settings
from twisted.internet import reactor

import utils
from boat_images_scraper import ClickAndBoatOfferImagesSpider, SamBoatOfferImagesSpider
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

    # # Remove tmp_*_offers.json content
    # utils.remove_lines_from_json_file("tmp_click_and_boat_offers.json")
    # utils.remove_lines_from_json_file("tmp_sam_boat_offers.json")

    settings = get_project_settings()
    # # Get url offers -> listed in tmp_click_and_boat_offers.json and tmp_sam_boat_offers.json files
    # print("Get click_and_boat offers url and stock them into tmp_click_and_boat_offers.json file .....")
    # run_spider(ClickAndBoatOfferSpider, settings, '')
    #
    # print("Get sam_boat offers url and stock them into tmp_sam_boat_offers.json file .....")
    # run_spider(SamBoatOfferSpider, settings, '')

    # For clickandboat (alias cnb)
    cnb_url_offers_list = get_url_from_offers_file("tmp_click_and_boat_offers.json")

    # For samboat (alias sb)
    sb_url_offers_list = get_url_from_offers_file("tmp_sam_boat_offers.json")

    offers_list = []

    for offer_url in sb_url_offers_list:
        # Remove tmp_*_images.json content
        utils.remove_lines_from_json_file("tmp_click_and_boat_images.json")
        utils.remove_lines_from_json_file("tmp_sam_boat_images.json")

        # Get images url for this offer
        print(f"\nFor the offer {offer_url['url']}, get the boat images urls and stock them "
              "into tmp_sam_boat_images.json file .....")
        run_spider(SamBoatOfferImagesSpider, settings, offer_url['url'])

        images_path_file = "tmp_sam_boat_images.json"
        images_urls = utils.get_urls_images_from_images_file(images_path_file)

        # Treat images to check if boat is nup or not
        nup_boat = utils.check_boat_nup_immatriculation_number(images_urls)

        offers_list.append({"offer_url": offer_url['url'], "NUP_identifie_par_OCR": nup_boat})

    print(offers_list)

    # TODO: find a solution to save data in db, at first db could be a csv or json file
    # Save a sample of some offers in a json file for the moment
    for item in offers_list:
        with open('offers.json', 'w') as f:
            json.dump(offers_list, f, indent=4)

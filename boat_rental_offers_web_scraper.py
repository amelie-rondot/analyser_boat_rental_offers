"""
This module defines a web scraper, using the Spider objects from scrapy package,
to get a list of boat rental internet offers urls from boat rental internet site such as
[Click&Boat](https://www.clickandboat.com/),
[SamBoat](https://www.samboat.fr/),...
"""
from scrapy import Spider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


class ClickAndBoatOfferSpider(Spider):
    name = "click_and_boat_offers"
    # request parameters:
    #   - _page = page number
    #   - limit = number of result per page
    #   - where = location
    #   - withCaptain = "With Captain" or "Without Captain" : avec ou sans skipper
    start_urls = [
        f"https://www.clickandboat.com/location-bateau/recherche?where=Marseille,%20France&ProduitTypeId=Motorboat;RIB;Without%20license&withCaptain=With%20captain",
    ]

    custom_settings = {
        "FEEDS": {
            "tmp_click_and_boat_offers.json": {"format": "json"},
        },
    }

    def parse(self, response):

        # Extract of HTML structure returned
        # <div class="searchPage__products"   ...
        #     <app-search-product class="searchPage__productAd"   ...
        #         <app-data-chaos ...
        #             <a ... href="dummy_url" .../>
        #         </app-data-chaos>
        #     </app-search-product>
        #     <app-search-product class="searchPage__productAd"   ...
        #         <app-data-chaos ...
        #             <a ... href="dummy_url_2" .../>
        #         </app-data-chaos>
        #     </app-search-product>
        #     ...
        # </div>

        for offer in response.css('app-search-product.searchPage__productAd'):
            url = offer.css('a::attr("href")').get()
            if not url is None and url.startswith("https://www.clickandboat.com/location-bateau/"):
                yield {"url": url}

        # <li class="pagination__item--next" ...
        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)


class SamBoatOfferSpider(Spider):
    name = "samboat_offers"
    # request parameters:
    #   - _page = page number
    #   - limit = number of result per page
    #   - destination_id = location, exemple "227863" for Marseille
    #   _ announcement = motorboat or voilier
    start_urls = [
        "https://www.samboat.fr/location-bateau?destination_id=227863&announcement={%22boat_type_id%22%3A[2%2C3%2C5%2C6]}",
    ]

    custom_settings = {
        "FEEDS": {
            "tmp_sam_boat_offers.json": {"format": "json"},
        },
    }

    def parse(self, response):

        # Extract of HTML structure returned
        # <div id="search-engine-announcements"   ...
        #     <div class="mb-4 col-12 col-md-6 col-xl-4 col-xxl-3 col-xxxl-3 col-xxxxl-2 col-12 col-md-6 col-xl-6 col-xxl-4 col-xxxl-4 col-xxxxl-3"   ...
        #         <a id="announcement-45366"... href="dummy_url" .../>
        #     </div>
        #     <div class="mb-4 col-12 col-md-6 col-xl-4 col-xxl-3 col-xxxl-3 col-xxxxl-2 col-12 col-md-6 col-xl-6 col-xxl-4 col-xxxl-4 col-xxxxl-3"   ...
        #         <a id="announcement-45367"... href="dummy_url_2" .../>
        #     </div>
        #     ...
        # </div>

        for offer in response.css('#search-engine-announcements div'):
            url = offer.css('a::attr("href")').get()
            if not url is None and url.startswith("https://www.samboat.fr/location-bateau/"):
                yield {"url": url}


if __name__ == "__main__":
    settings = get_project_settings()
    process = CrawlerProcess(settings)

    process.crawl(ClickAndBoatOfferSpider)
    process.crawl(SamBoatOfferSpider)
    process.start()

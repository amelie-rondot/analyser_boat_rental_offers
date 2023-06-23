"""
This module defines a web scraper, using the Spider objects from scrapy package,
to get a list of boat rental internet offers urls from boat rental internet site such as
[Click&Boat](https://www.clickandboat.com/),
[SamBoat](https://www.samboat.fr/),...
"""
from scrapy import Spider


class ClickAndBoatOfferSpider(Spider):

    name = "offers"
    # request parameters:
    #   - _page = page number
    #   - limit = number of result per page
    #   - where = location
    #   - withCaptain = "With Captain" or "Without Captain" : avec ou sans skipper
    start_urls = [
        f"https://www.clickandboat.com/location-bateau/recherche?where=Marseille,%20France&ProduitTypeId=Motorboat;RIB;Without%20license&withCaptain=With%20captain",
    ]

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
        #             <a ... href="dummy_url" .../>
        #         </app-data-chaos>
        #     </app-search-product>
        #     ...
        # </div>

        for offer in response.css('app-search-product.searchPage__productAd'):
            url = offer.css('a::attr("href")').get()
            print(url)
            yield {"url": url}

        # <li class="pagination__item--next" ...
        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

### Develop

Pour lancer le web scraping des url d'offres de location :

```scrapy runspider boat_rental_offers_web_scraper.py -o tmp_offers.json```


Pour lancer le web scraping des urls des images d'une offre de location
(nécessaire pour récupérer le numéro d'immatriculation du bateau) :

```scrapy runspider boat_images_scraper.py -o tmp_images.json```

Pour lancer la récupération du numéro d'immatriculation d'un bateau :

```python utils.py```
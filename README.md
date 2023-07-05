### Develop

Pour lancer le web scraping des url d'offres de location :

```python boat_rental_offers_web_scraper.py```

Cela enregistre les url des offres de location dans des fichiers json :
`tmp_click_and_boat_offers.json` et `tmp_sam_boat_offers.json`


Pour lancer le web scraping des urls des images d'une offre de location
(nécessaire pour récupérer le numéro d'immatriculation du bateau) :

```scrapy runspider boat_images_scraper.py -o tmp_images.json```

Pour lancer la récupération du numéro d'immatriculation d'un bateau :

```python utils.py```
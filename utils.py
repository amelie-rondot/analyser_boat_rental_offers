"""
This module defines utils functions used in this project.
"""
import json

import cv2
import easyocr
import pytesseract
import matplotlib.pyplot as plot
import torch


# path_file_offers = "./tmp_click_and_boat_offers.json" or "./tmp_sam_boat_offers.json"
def get_url_from_offers_file(path_file_offers: str) -> [str]:
    """
    From a json file such as tmp_click_and_boat_offers.json containing for example:
    "[
    {"url": "https://www.clickandboat.com/location-bateau/marseille/bateau-moteur/quicksilver-cruiser-755-b9vkp5"},
    {"url": "https://www.clickandboat.com/location-bateau/marseille/semi-rigide/thai-fiber-boat-katoy-650-open-6r44v"},
    ]",
    return the list of the urls contained in the file.

    :param: path_file_offers: str
    :return: [str] list of offers urls
    """
    f = open(path_file_offers)
    offers_urls_list = json.load(f)
    return offers_urls_list


# path_file_images = "./tmp_click_and_boat_images.json" or "./tmp_sam_boat_images.json"
def get_urls_images_from_images_file(path_file_images: str) -> [str]:
    """
    From a json file such as tmp_click_and_boat_images.json containing for example:
    "[
    {"url_image": "https://static1.clickandboat.com/v1/p/5umVhPqkiPp8Lqc1xZRUdLfaPEmmlORy.big.jpg"},
    {"url_image": "https://static1.clickandboat.com/v1/p/mhWJyuqLeydA1pfzOanjcykanHxGHLuU.big.jpg"},
    ]",
    return the list of the urls contained in the file.
    :param: path_file_images: str
    :return: [str] list of boat images urls
    """
    f = open(path_file_images)
    images_urls_list = []
    for image_url in json.load(f):
        images_urls_list.append(image_url['url_image'])
    return images_urls_list


def get_boat_immatriculation_number(images_url_list: [str]):
    """
    From a list of boat images urls, extract the boat immatriculation number with OCR technology.
    :param images_url_list: [str] list of boat images urls
    """
    print(f"cuda available = {torch.cuda.is_available()}")
    for image_path in images_url_list:
        # easyocr method
        reader = easyocr.Reader(['en'],  gpu=False)
        texts_with_easyocr = reader.readtext(image_path, detail=0, paragraph=True)
        print(set(texts_with_easyocr))
        print("\n")

        # pytesseract method
        # Work with local image -> needs t
        # image_path = "./data/boat_img1_AJB798544.jpg"
        # img_cv = cv2.imread(image_path)
        # text_with_pytesseract = pytesseract.pytesseract.image_to_string(img_cv, config='--psm 12')
        # # config='--psm 12' shows better results
        # print(text_with_pytesseract)


if __name__ == "__main__":
    path_file_images = "tmp_sam_boat_offers.json"
    # path_file_images = "tmp_click_and_boat_offers.json"
    images_url_list = get_urls_images_from_images_file(path_file_images)
    get_boat_immatriculation_number(images_url_list)

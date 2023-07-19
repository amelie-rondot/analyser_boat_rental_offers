"""
This module defines utils functions used in this project.
"""
import json
import re

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


def check_boat_nup_immatriculation_number(images_url_list: [str]) -> bool:
    """
    From a list of boat images urls, read textual information present in images with OCR technology.
    From this read information, return True if one of the textual information matches with N.U.P format
    (ie a series of 3 letters followed by 5 numbers, used for NUP boats, for example "TLF12345") else False
    :param images_url_list: [str] list of boat images urls
    :return: bool
    """
    nup_format = "[a-zA-Z]{2}\s[a-zA-Z]\s?[0-9]{5,}"
    nup = False

    for image_path in images_url_list:
        # easyocr method
        reader = easyocr.Reader(['en'], gpu=False)
        texts_with_easyocr = reader.readtext(image_path, detail=0, paragraph=True)
        for text in texts_with_easyocr:
            if re.match(nup_format, text):
                nup = True
                break
        if nup:
            break
    return nup


def remove_lines_from_json_file(json_file_path: str):
    with open(json_file_path, 'r+') as fp:
        fp.seek(0)
        fp.truncate()


if __name__ == "__main__":
    # path_file_images = "tmp_sam_boat_images.json"
    # # path_file_images = "tmp_click_and_boat_images.json"
    # images_url_list = get_urls_images_from_images_file(path_file_images)
    # check_boat_nup_immatriculation_number(images_url_list)

    remove_lines_from_json_file("tmp_click_and_boat_offers.json")
    remove_lines_from_json_file("tmp_sam_boat_offers.json")
    remove_lines_from_json_file("tmp_click_and_boat_images.json")
    remove_lines_from_json_file("tmp_sam_boat_images.json")

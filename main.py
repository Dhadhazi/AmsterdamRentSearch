from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time

GOOGLE_FORM_ADDRESS = "https://docs.google.com/forms/d/e/1FAIpQLSepzXqXgtlxjj8IFhzqSmvsCk3lCCeIaMcHYYFHlrEih8f9LQ/viewform?usp=sf_link"

# Add the link with search filtered in, don't put / at the end
PARARIUS_LINK = "https://www.pararius.com/apartments/amsterdam/1400-2000/radius-5"

# How many pages of data do you want to grab from the start
NUMBER_OF_PAGES_TO_GRAB = 5


def get_all_listing_from_page(page_link):
    response = requests.get(page_link)
    soup = BeautifulSoup(response.text, "html.parser")
    listings = soup.find_all(class_="search-list__item search-list__item--listing")
    findings_list = []

    for listing in listings:
        title_link = listing.find(class_="listing-search-item__link listing-search-item__link--title")
        price = listing.find(class_="listing-search-item__price")
        advertiser_box = listing.find(name="div", class_="listing-search-item__info")
        advertiser = advertiser_box.find(mame="a", class_="listing-search-item__link")

        advertisement = {
            "title": title_link.getText(),
            "link": title_link.get("href"),
            "price": price.getText().strip(),
            "advertiser": advertiser_box.getText().strip()
        }

        features = listing.find_all(name="li", class_="illustrated-features__item")
        for feature in features:
            name = feature.find(name="span", class_="illustrated-features__term").getText()
            description = feature.find(name="span", class_="illustrated-features__description").getText()
            advertisement[name] = description

        findings_list.append(advertisement)
    return findings_list


def get_max_pagination(page_link):
    response = requests.get(page_link)
    soup = BeautifulSoup(response.text, "html.parser")
    paginations = soup.find_all(name="a", class_="pagination__link")
    max_page = 1
    for item in paginations:
        page_number = int(item.get("data-pagination-page"))
        if max_page < page_number:
            max_page = page_number
    return max_page


max_page = get_max_pagination(PARARIUS_LINK)
if NUMBER_OF_PAGES_TO_GRAB > max_page:
    NUMBER_OF_PAGES_TO_GRAB = max_page

all_listings = []
for i in range(1, NUMBER_OF_PAGES_TO_GRAB+1):
    link = f"{PARARIUS_LINK}/page-{i}"
    all_listings.extend(get_all_listing_from_page(link))
    time.sleep(6)

print(len(all_listings))
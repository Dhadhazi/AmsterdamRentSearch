from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import time

GOOGLE_FORM_ADDRESS = "https://docs.google.com/forms/d/e/1FAIpQLSepzXqXgtlxjj8IFhzqSmvsCk3lCCeIaMcHYYFHlrEih8f9LQ/viewform?usp=sf_link"

# Add the link with search filtered in, don't put / at the end
PARARIUS_LINK = "https://www.pararius.com/apartments/amsterdam/1200-1750/radius-5"

# How many pages of data do you want to grab from the start
NUMBER_OF_PAGES_TO_GRAB = 4

# Selenium setup
chrome_driver_path = "/Users/dani/Documents/chromedriver"
driver = webdriver.Chrome(executable_path=chrome_driver_path)


# Grabs all listings from a page
def get_all_listing_from_page(page_link):
    response = requests.get(page_link)
    soup = BeautifulSoup(response.text, "html.parser")
    listings = soup.find_all(class_="search-list__item search-list__item--listing")
    findings_list = []

    for listing in listings:
        title_link = listing.find(class_="listing-search-item__link listing-search-item__link--title")
        price = listing.find(class_="listing-search-item__price")
        advertiser = listing.find(name="div", class_="listing-search-item__info")

        advertisement = {
            "title": title_link.getText(),
            "link": title_link.get("href"),
            "price": price.getText().strip(),
            "advertiser": advertiser.getText().strip()
        }

        features = listing.find_all(name="li", class_="illustrated-features__item")
        for feature in features:
            name = feature.find(name="span", class_="illustrated-features__term").getText()
            description = feature.find(name="span", class_="illustrated-features__description").getText()
            advertisement[name] = description

        findings_list.append(advertisement)
    return findings_list


# Gets the maximum pagination
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


# Opens and fills a google form page
def fill_a_page(ad):
    global driver
    driver.get(GOOGLE_FORM_ADDRESS)
    time.sleep(2)
    title = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    title.send_keys(ad["title"])

    price = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price.send_keys(ad["price"])
    if "Living area" in ad:
        size = driver.find_element_by_xpath(
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        size.send_keys(ad["Living area"])

    if "Rooms" in ad:
        rooms = driver.find_element_by_xpath(
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[4]/div/div/div[2]/div/div[1]/div/div[1]/input')
        rooms.send_keys(ad["Rooms"])

    if "Year of construction" in ad:
        yearofconstruction = driver.find_element_by_xpath(
            '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[5]/div/div/div[2]/div/div[1]/div/div[1]/input')
        yearofconstruction.send_keys(ad["Year of construction"])

    advertiser = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[6]/div/div/div[2]/div/div[1]/div/div[1]/input')
    advertiser.send_keys(ad["advertiser"])

    link = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[7]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link.send_keys(ad["link"])

    submit_button = driver.find_element_by_xpath('//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div/span')
    submit_button.click()


max_page = get_max_pagination(PARARIUS_LINK)
if NUMBER_OF_PAGES_TO_GRAB > max_page:
    NUMBER_OF_PAGES_TO_GRAB = max_page

all_listings = []
for i in range(1, NUMBER_OF_PAGES_TO_GRAB+1):
    link = f"{PARARIUS_LINK}/page-{i}"
    all_listings.extend(get_all_listing_from_page(link))
    time.sleep(5)

for ad in all_listings:
    fill_a_page(ad)

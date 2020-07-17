"""
Title: GifViewer For Giphy
Desc: A Gihpy Gif-Webscraper written in Python3
Author: Jonathan Bral

Funtionality: Grabs direct URLS from 'trending GIFS' gif posts,
https://giphy.com/trending-gifs
and each gif's corresponding tags, then outputs all data into url_data.json.
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from scrape.url_info import UrlData
import random

driver = webdriver.Firefox()
URL = "https://giphy.com/trending-gifs"
data = UrlData()


class ScrapeBot:
    def __init__(self):
        self.driver = driver
        self.driver.get(URL)  # Opens desired URL [https://giphy.com/trending-gifs]
        sleep(2)  # waits for page to load
        x_path = '/html/body/div[4]/div/div/div[5]/div/div[1]/a[1]'
        button = self.driver.find_element_by_xpath(x_path)  # Opens first GIF
        button.click()
        sleep(2)

        # Loops until terminated manually
        while True:
            self.exec_scrape()

    # Performs scrape process for each page
    def exec_scrape(self):
        self.start_scrape()

        # Performs hover and click for 'next arrow'
        action = ActionChains(self.driver)
        arrow_xpath = '/html/body/div[4]/div/div/div[4]/div/div[2]/div[1]/div[2]/div[1]/div/a[2]'
        try:
            arrow_path = self.driver.find_element_by_xpath(arrow_xpath)
        except NoSuchElementException:
            arrow_xpath = '/html/body/div[4]/div/div/div[4]/div/div[2]/div[1]/div[2]/div[1]/div/a'
            arrow_path = self.driver.find_element_by_xpath(arrow_xpath)

        action.move_to_element(arrow_path).perform()
        arrow_path.click()  # Selects 'next' arrow to load next gif.
        sleep(2)

    def check_exists_by_class_name(self, classname, item):
        try:
            item.find_element_by_class_name(classname)
        except NoSuchElementException:
            return False
        return True

    # Returns a list of the gifs tags
    def get_tags(self):
        # Store all the image tags in a list
        tags = []

        tagPath = '/html/body/div[4]/div/div/div[4]/div/div[2]/div[2]/div[1]/div'  # Path of div container for tags.
        try:
            html_list = self.driver.find_element_by_xpath(tagPath)
            items = html_list.find_elements_by_tag_name("a")
            for item in items:
                item_tag = item.find_element_by_tag_name('h3')
                tag = item_tag.text
                print("Here: ", end='')
                print(tag)
                if (not tag) or (tag == "..."):
                    pass
                else:
                    tags.append(tag)
        except NoSuchElementException:
            pass
        return tags

    # Starts scraping process for current page
    def start_scrape(self):
        copy_button_xpath = '/html/body/div[4]/div/div/div[4]/div/div[2]/div[1]/div[2]/div[2]/div[2]/span'
        button = self.driver.find_element_by_xpath(copy_button_xpath)  # Clicks the Copy link button
        button.click()

        link_xpath = '/html/body/div[4]/div/div/div[4]/div/div[2]/div[1]/div[1]/div/div/div[2]/div[2]/input'
        link = self.driver.find_element_by_xpath(link_xpath)  # Locates gif url

        tags = self.get_tags()
        data.add(link.get_attribute('value'), tags)  # Adds data to JSON file


if __name__ == "__main__":
    ScrapeBot()  # executes the web-scraper.

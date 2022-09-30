import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

EXTENSION_PATH = r'C:\Users\mirko\AppData\Local\Google\Chrome\User Data\Default\Extensions\cjpalhdlnbpafiamejdnhcphjbkeiagm\1.44.4_0'


class Scraper():
    def __init__(self):
        self.max_pages = 200
        self.category_pos = 0

        self.df = pd.DataFrame()

        chrome_options = Options()
        chrome_options.add_argument('load-extension=' + EXTENSION_PATH)

        self.driver = webdriver.Chrome('D:\Chrome Driver\chromedriver.exe', chrome_options=chrome_options)
        self.driver.create_options()

        self.headlines = []
        self.current_category = 'Placeholder'
        self.categories = []

    def start(self):
        self.driver.get('https://novini.bg/bylgariya?date=today')
        time.sleep(2)
        self.cookie_pass()

        for i in range(9):
            self.extract_content()

        self.export_csv()

    def cookie_pass(self):
        cookie_pass_button = self.driver.find_element(By.ID, 'onetrust-accept-btn-handler')
        cookie_pass_button.click()

    def get_buttons(self):
        buttons = self.driver.find_elements(By.CLASS_NAME, 'header-shortcuts__sublink')

        return buttons

    def extract_headlines(self):
        headlines_attributes = self.driver.find_elements(By.CLASS_NAME, 'g-grid__item-title')
        for headline in headlines_attributes:
            print(headline.text)
            self.headlines.append(headline.text)
            self.categories.append(self.current_category)

    def get_next_page(self):
        next_page_button = self.driver.find_element(By.CLASS_NAME, 'icn--page-next')
        next_page_button.click()

    def extract_content(self):
        buttons = self.get_buttons()
        pages = 0


        self.current_category = buttons[self.category_pos].text
        print(self.current_category)
        buttons[self.category_pos].click()
        self.extract_headlines()


        see_all_button = self.driver.find_element(By.CLASS_NAME, 'btn__seeAll')
        see_all_button.click()
        while pages < self.max_pages:
            self.extract_headlines()
            self.get_next_page()

            pages += 1

        self.category_pos += 1

    def export_csv(self):
        data = {
            'Headlines': self.headlines,
            'Category': self.categories
        }

        df = pd.DataFrame(data)
        df.to_csv('bg_news_headlines_data.csv')

scraper = Scraper()
scraper.start()



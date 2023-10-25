import datetime
import pickle
import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

FACEBOOK_URL = "https://www.facebook.com"
ALBUMS_URL = "https://www.facebook.com/penelco/photos_albums"
FORBIDDEN_ALBUM = -1

class Scraper:
    def __init__(self, cached_albums_file_name: str, cookies_file_name: str):
        self.driver = webdriver.Firefox()
        self.wait = WebDriverWait(self.driver, 30)

        self.cached_albums_file_name = cached_albums_file_name
        with open(self.cached_albums_file_name, 'rb') as f:
            self.albums = pickle.load(f)

        self.cookies_file_name = cookies_file_name
    
        self.num_items_regex = re.compile("(\d+) Item")

        # Only works until year 9999
        year = datetime.date.today().year
        self.all_interruptions_xpath = f"//span[contains(text(), '{year}')]/ancestor::div[4]"

    def __del__(self):
        if self.albums:
            with open(self.cached_albums_file_name, 'wb') as f:
                pickle.dump(self.albums, f)

            with open(self.cookies_file_name, 'wb') as f:
                pickle.dump(self.driver.get_cookies(), f)

    def login_to_facebook(self, username: str, password: str):
        self.driver.get(FACEBOOK_URL)
        with open(self.cookies_file_name, 'rb') as f:
            cookies = pickle.load(f)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

        try:
            email_input = self.wait.until(EC.visibility_of_element_located((By.ID, "email")))
            email_input.send_keys(username)
        except TimeoutException:
            # Most likely already logged-in
            return

        pass_input = self.driver.find_element_by_id("pass")
        pass_input.send_keys(password)

        login_button = self.driver.find_element_by_name("login")
        login_button.click()

    def navigate_to_penelco_albums(self):
        self.driver.get(ALBUMS_URL)

    def num_interruption_albums(self):
        return len(self.driver.find_elements_by_xpath(self.all_interruptions_xpath))

    def scrape_single_album(self, index: int):

        all_interruptions = self.driver.find_elements_by_xpath(self.all_interruptions_xpath)
        interruption = all_interruptions[index]

        title, num_items_str = interruption.text.split("\n")

        re_match = self.num_items_regex.match(num_items_str)
        if not re_match:
            return
        
        num_items = int(re_match.group(1))

        if "interruption" not in title.lower():
            self.albums[title] = FORBIDDEN_ALBUM

        if title in self.albums:
            if self.albums[title] == FORBIDDEN_ALBUM:
                return

            # Check if there are added images
            if self.albums[title] == num_items:
                return

        album = interruption.find_element_by_xpath(".//img")
        album.click()

        self.process_album()

        self.driver.back()

        self.albums[title] = num_items

    def process_album(self):
        pass
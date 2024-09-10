import time
import requests
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from typing import List, Tuple, Optional
from BookHak.utils.io import Review
from BookHak.utils.utils import fullwidth_to_halfwidth, halfwidth_to_fullwidth
from BookHak.utils.driver import ChromeDriverManager
from BookHak.utils.log import logger


class Books:
    def __init__(self, book_title: str):
        self.book_title = book_title
        self.driver = ChromeDriverManager().get_driver()

    def get_reviews_pipeline(self) -> Optional[List[Tuple]]:
        try:
            self.book_id = self._get_book_id()
            total_page = self._get_total_page()
            if total_page == 0:
                return []

            result_list = []
            for i in range(total_page):
                rows = self._get_reviews_by_page(i)
                result_list += rows

            return result_list
        except Exception as e:
            logger.error(f"An error occurred when crawling Books: {e} ")
        finally:
            self.driver.quit()

    def _get_book_id(self) -> str:
        self.driver.get("https://www.books.com.tw/?loc=tw_logo_001")

        ad_close = self.driver.find_element(By.ID, "close_top_banner")
        ad_close.click()
        time.sleep(3)

        type_select = self.driver.find_element(By.CLASS_NAME, "toggle_btn")
        type_select.click()
        type_item = self.driver.find_element(By.CSS_SELECTOR, "a[cat=BKA]")
        type_item.click()
        search_box = self.driver.find_element(By.CLASS_NAME, "search_key")
        search_box.send_keys(self.book_title)
        search_button = self.driver.find_element(By.CLASS_NAME, "search_btn")
        search_button.click()
        link_element = self._get_link_element()
        link_href = link_element.get_attribute("href")
        match = re.search(r'/item/(\d+)/', link_href)
        if match:
            book_id = match.group(1)
            logger.info(f"book_id: {book_id}")
            return book_id
        else:
            logger.info("未找到 book_id")
            return None

    def _get_reviews_by_page(self, page: int):
        _page = page + 1
        soup = self._req(_page)
        items = soup.find_all('div', class_='box-item type-02')
        result_list = []
        for item in items:
            title = item.find('div', class_='title').find('a').get_text() if item.find('div', class_='title').find('a') else ""
            content = item.find('span', calss='comment-content').get_text()
            rating = item.find('span', class_="bui-star")["title"].removesuffix("顆星")
            row = Review(title=title, content=content, rating=rating, source="books").__dict__
            result_list.append(row)

        return result_list

    def _get_total_page(self) -> int:
        soup = self._req(1)
        em_element = soup.find('em')
        if em_element is None:
            return 0

        total_page = em_element.get_text()
        return int(total_page)

    def _get_link_element(self):
        # 全形或半形都有可能出現
        try:
            title_trans = fullwidth_to_halfwidth(self.book_title)
            link_element = self.driver.find_element(By.CSS_SELECTOR, f"a[title='{title_trans}']")

            return link_element
        except NoSuchElementException:
            try:
                title_trans = halfwidth_to_fullwidth(self.book_title)
                link_element = self.driver.find_element(By.CSS_SELECTOR, f"a[title='{title_trans}']")

                return link_element
            except NoSuchElementException:
                return None

    def _req(self, page: int):
        reqUrl = "https://www.books.com.tw/booksComment/ajaxCommemtFilter"
        headersList = {
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8"
        }
        payload = {
            "type": "getCommemt",
            "stars[]": "all",
            "daterange": "all",
            "num": page,
            "item": self.book_id
        }
        resp = requests.request("POST", reqUrl, data=payload,  headers=headersList)
        response = resp.json()
        soup = BeautifulSoup(response["htmlData"], 'html.parser')

        return soup

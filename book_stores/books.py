import time
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import Dict, List, Tuple
from utils.io import store_reviews, Review


options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)  # 不自动关闭浏览器
options.add_argument("--disable-notifications")  # 禁用通知
options.add_argument("--disable-popup-blocking")  # 禁用弹出窗口拦截
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)


def test(book_title: str) -> List[Tuple]:
    try:
        # driver.get("https://www.books.com.tw/")
        driver.get("https://www.books.com.tw/?loc=tw_logo_001")

        ad_close = driver.find_element(By.ID, "close_top_banner")
        ad_close.click()
        time.sleep(3)

        type_select = driver.find_element(By.CLASS_NAME, "toggle_btn")
        type_select.click()
        type_item = driver.find_element(By.CSS_SELECTOR, "a[cat=BKA]")
        type_item.click()
        search_box = driver.find_element(By.CLASS_NAME, "search_key")
        search_box.send_keys(book_title)
        search_button = driver.find_element(By.CLASS_NAME, "search_btn")
        search_button.click()
        link_element = driver.find_element(By.CSS_SELECTOR, f"a[title={book_title}]")
        link_href = link_element.get_attribute("href")
        match = re.search(r'/item/(\d+)/', link_href)
        if match:
            book_id = match.group(1)
            print(f"ID: {book_id}")
        else:
            print("未找到 ID")

        reqUrl = "https://www.books.com.tw/booksComment/ajaxCommemtFilter"
        headersList = {
          "Accept": "*/*",
          "User-Agent": "Thunder Client (https://www.thunderclient.com)",
          "Content-Type": "multipart/form-data; boundary=kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A"
        }
        payload = f"--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A\r\nContent-Disposition: form-data; name=\"type\"\r\n\r\ngetCommemt\r\n--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A\r\nContent-Disposition: form-data; name=\"stars[]\"\r\n\r\nall\r\n--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A\r\nContent-Disposition: form-data; name=\"daterange\"\r\n\r\nall\r\n--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A\r\nContent-Disposition: form-data; name=\"num\"\r\n\r\n1\r\n--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A\r\nContent-Disposition: form-data; name=\"item\"\r\n\r\n0010919211\r\n--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A--\r\n"
        response = requests.request("POST", reqUrl, data=payload,  headers=headersList)
        print(response.text)
    finally:
        driver.quit()


def get_all_reviews(all_reviews: List, resp_reviews: List[Dict]):
    for review in resp_reviews:
        row = Review(
            title=review["title"],
            content=review["content"],
            rating=review["reading"]["rating"],
            source="readmoo"
        ).to_row()

        all_reviews.append(row)

    return all_reviews

import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from typing import Dict, List, Tuple
from utils.io import Review


options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)  # 不自动关闭浏览器
options.add_argument("--disable-notifications")  # 禁用通知
options.add_argument("--disable-popup-blocking")  # 禁用弹出窗口拦截
driver = webdriver.Chrome(options=options)
driver.implicitly_wait(10)


def test(book_title: str) -> List[Tuple]:
    try:
        driver.get("https://readmoo.com/")

        search_box = driver.find_element(By.NAME, "search_term_string")
        search_box.send_keys(book_title)
        time.sleep(3)
        search_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='搜尋']")
        search_button.click()
        link_element = driver.find_element(By.CSS_SELECTOR, f"a[aria-label={book_title}]")
        book_id = link_element.get_attribute('data-readmoo-id')

        COUNT = 10
        reqUrl = f"https://readmoo.com/api/reviews?readmoo_id={book_id}&page%5Bcount%5D={COUNT}&page%5Boffset%5D=0"
        resp = requests.request("GET", reqUrl)
        response = resp.json()
        result_list = get_all_reviews([], response["reviews"])

        if int(response["total"]) > COUNT:
            RESIDUAL_COUNT = int(response["total"]) - COUNT
            reqUrl = f"https://readmoo.com/api/reviews?readmoo_id={book_id}&page%5Bcount%5D={RESIDUAL_COUNT}&page%5Boffset%5D={COUNT}"
            resp = requests.request("GET", reqUrl)
            response = resp.json()
            result_list = get_all_reviews(result_list, response["reviews"])

        return result_list
    finally:
        time.sleep(10)
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

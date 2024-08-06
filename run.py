from book_stores import Books, readmoo
from utils.io import store_reviews

book_title = "高成長思維"
book_title = "底層邏輯：看清這個世界的底牌"


def get_reviews_pipeline(book_title: str):
    content = []
    rows = readmoo(book_title)
    content += rows
    rows = Books(book_title).get_reviews_pipeline()
    content += rows

    store_reviews(book_title, content)


get_reviews_pipeline(book_title=book_title)

from book_stores import books, readmoo
from utils.io import store_reviews, Review

book_title = "高成長思維"
book_title = "底層邏輯：看清這個世界的底牌"


def get_reviews_pipeline(book_title: str):
    # rows = readmoo(book_title)
    rows = books(book_title)
    # store_reviews(rows)


get_reviews_pipeline(book_title=book_title)

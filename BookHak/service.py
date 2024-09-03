from BookHak.crawler import Books, Readmoo
from BookHak.utils.io import store_reviews


def get_reviews_pipeline(book_title: str):
    content = []
    rows = Readmoo(book_title).get_reviews_pipeline()
    content += rows
    rows = Books(book_title).get_reviews_pipeline()
    content += rows

    store_reviews(book_title, content)

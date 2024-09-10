from BookHak.crawler import Books, Readmoo
from BookHak.crud import find_book_by_title, create_book
from BookHak.utils.log import logger


def get_reviews_by_title(book_title: str):
    logger.info(f"Start to get reviews of book 『{book_title}』")
    try:
        book = find_book_by_title(book_title)
        if book:
            return book["reviews"]

        reviews = []
        reviews_in_readmoo = Readmoo(book_title).get_reviews_pipeline()
        logger.info("Get reviews in Readmoo succeed!")
        reviews += reviews_in_readmoo

        reviews_in_books = Books(book_title).get_reviews_pipeline()
        logger.info("Get reviews in Books succeed!")
        reviews += reviews_in_books

        create_book(book_title, reviews)

        return reviews
    except Exception as e:
        logger.error(f"Fail to get reviews: {e}")

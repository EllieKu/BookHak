from BookHak.crawler import Books, Readmoo
from BookHak.crud import find_book_by_title, create_book


def get_reviews_by_title(book_title: str):
    book = find_book_by_title(book_title)
    if book:
        return book["reviews"]

    reviews = Readmoo(book_title).get_reviews_pipeline()
    reviews += Books(book_title).get_reviews_pipeline()

    create_book(book_title, reviews)

    return reviews

from datetime import datetime
from BookHak.database import db
from BookHak.utils.utils import generate_md5_from_title

collection_ref = db.collection("books")


def create_book(title: str, reviews: list[dict] = []):
    doc_id = generate_md5_from_title(title)

    collection_ref.document(doc_id).set({
        "title": title,
        "update_time": datetime.now(),
        "reviews": reviews
    })


def find_book_by_title(title: str):
    doc_id = generate_md5_from_title(title)
    book = collection_ref.document(doc_id).get()

    if book.exists:
        return book.to_dict()
    else:
        print("No such document!")

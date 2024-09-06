from fastapi import FastAPI
from BookHak.service import get_reviews_by_title

app = FastAPI()


@app.get("/reviews")
def book_reviews(title: str):
    re = get_reviews_by_title(title)

    return re

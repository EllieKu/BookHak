import csv
from dataclasses import dataclass


def writer_csv(filename: str, content: list[str]):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(("title", "content", "rating", "source"))

        for row in content:
            writer.writerow(row)


def store_reviews(filename: str, data: list[str]):
    filepath = f"./output/{filename}.csv"
    writer_csv(filepath, data)

    print(f"Reviews has been written to {filepath}")


@dataclass
class Review:
    title: str
    content: str
    rating: int
    source: str

    def to_row(self):
        return (self.title, self.content, self.rating, self.source)

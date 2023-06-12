import json
from os import path

from models import Author, Quote
from connect import connection, PATH_TO_LIB


def add_authors_from_json():
    with open(path.join(PATH_TO_LIB, 'authors.json'), encoding="utf-8") as authors_json:
        authors = json.load(authors_json)

    for author in authors:
        new_author = Author(fullname=author['fullname'])
        new_author.born_date = author['born_date']
        new_author.born_location = author['born_location']
        new_author.description = author['description']
        new_author.save()


def add_quotes_from_json():
    with open(path.join(PATH_TO_LIB, 'quotes.json'), encoding="utf-8") as quotes_json:
        quotes = json.load(quotes_json)

    for quote in quotes:
        author_fullname = quote['author']
        author = Author.objects(fullname=author_fullname).first()
        new_quote = Quote(author=author)
        new_quote.tags = quote['tags']
        new_quote.quote = quote['quote']
        new_quote.save()


Author.objects.delete()
add_authors_from_json()

Quote.objects.delete()
add_quotes_from_json()

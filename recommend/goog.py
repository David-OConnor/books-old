from collections import namedtuple
import datetime as dt

import requests

from books.auth import goog_key as key


Book = namedtuple('Book', ['title', 'authors', 'isbn_10', 'isbn_13', 'publication_date'])

base_url = 'https://www.googleapis.com/books/v1/'


def search_title(title):
    url = base_url + 'volumes'
    payload = {'q': 'intitle:"{}"'.format(title),
               'printType': 'books',
               'projection': 'full'}

    result = requests.get(url, params=payload)

    result = result.json()
    result = [book['volumeInfo'] for book in result['items']]

    return _trim_results(result)


def search_author(author):
    url = base_url + 'volumes'
    payload = {'q': 'inauthor:"{}"'.format(author),
               'printType': 'books'}

    result = requests.get(url, params=payload)

    result = result.json()
    result = [book['volumeInfo'] for book in result['items']]

    return _trim_results(result)


def search(title='', author=''):
    url = base_url + 'volumes'
    payload = {'q': 'intitle:{}+inauthor:{}'.format(title, author),
               'printType': 'books'}

    result = requests.get(url, params=payload)

    result = result.json()
    result = [book['volumeInfo'] for book in result['items']]
    # return result
    trimmed = _trim_results(result)

    return _filter_results(trimmed)


def _trim_results(raw_data):
    result = []
    for book in raw_data:
        try:
            pub_date = dt.datetime.strptime(book['publishedDate'],
                                            '%Y-%m-%d').date()
        except ValueError:
            pub_date = book['publishedDate']
        except KeyError:
            pub_date = 'Missing pub date'

        isbn_10 = ''
        isbn_13 = ''
        try:
            isbn_raw = book['industryIdentifiers']

            for num in isbn_raw:
                if num['type'] == 'ISBN_13':
                    isbn_13 = num['identifier']
                elif num['type'] == 'ISBN_10':
                    isbn_10 = num['identifier']

        # This keyerror means 'industryIdentifiers' is missing entirely; if
        # it's present, but doens't have 'isbn_13/10' subkeys, it doesn't
        # come up.
        except KeyError:
            pass
        result.append(
            Book(book['title'], book['authors'], isbn_10, isbn_13, pub_date)
        )
    return result


def _filter_results(result):
    has_isbn = lambda x: x.isbn_10 or x.isbn_13
    return list(filter(has_isbn, result))

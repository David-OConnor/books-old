from recommend.models import Work, ISBN
from recommend import goog


def query(title: str, author: str):
    result = Work.objects.filter(title=title, author=author)
    if not result:
        save_from_api(title, author)

    return result


def save_from_api(title: str, author: str) -> None:
    api_data = goog.search(title, author)
    print(api_data)

    found = False
    for book in api_data:

        if book.title == title and author in book.authors:
            work = Work(title=title, author=author)
            isbn = ISBN(isbn_10=book.isbn_10,
                        isbn_13=book.isbn_13,
                        publication_date=book.publication_date,
                        work=work)
            work.save()
            isbn.save()
            print("Saved {} by {}".format(title, author))
            found = True
    if not found:
        print("Nope, not here: {}, by {}".format(title, author))

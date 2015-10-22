from django.db.models import Q

from itertools import combinations
from typing import List

from recommend.models import Relationship, Work


def submit(books: List[Work]):
    # todo this is a crude way of doing it that won't provide good results.
    candidates = {}
    for book in books:
        rships = Relationship.objects.filter(Q(book1=book) | Q(book2=book))
        for rship in rships:
            # Determine which book is one we queried for; the other's the
            # potential recommendation.
            candidate = rship.book1 if rship.book2 == book else rship.book2

            try:
                candidates[candidate] += rship.weight
            except KeyError:
                candidates[candidate] = rship.weight

    new_relationship(books)

    # todo you want a ranked order; not just the top
    best = max(candidates, key=lambda x: x['weight'])
    return best


def new_relationship(books):
    # todo run after / async with book submission
    for book1, book2 in combinations(books, 2):

        # todo do it both orders, or force an alphabetic etc hierarchy
        existing_relationship = Work.objects.filter(book1=book1)
        # Using get here raises MultipleObjectsReturned if more than one relationship
        # exists for this combination, as it should.
        try:
            existing_relationship = existing_relationship.get(book2=book2)
        except Work.DoesNotExist:
            relationship = Relationship(book1=book1, book2=book2)
            relationship.save()
        else:
            existing_relationship.weight += 1

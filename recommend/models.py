from django.db import models
#
#
# class Book(models.Model):
#     """For now, each Book has a unique ISBN; multiple Books may be associated.
#     An alternative way would be to have multiple ISBNs for each Book."""
#     # Store isbns as a JSON list?
#     # isbn 13 format.
#     isbn10 = models.TextField(unique=True)
#     isbn13 = models.TextField(unique=True)
#     title = models.CharField(max_length=255)
#     author = models.CharField(max_length=255)
#     publication_date = models.DateField()
#     # Media can be 'print', 'ebook' etc.
#     # Consider turning media into an enum-style choice later.
#     # media = models.CharField(max_length=255)
#     # same_work = models.ManyToManyField(self)
#
#     def __str__(self):
#         return "{}, by {}".format(self.title, self.author)
#
#     class Meta:
#         ordering = ('author', 'title')
#
#
# class Relationship(models.Model):
#     book1 = models.ForeignKey(Book, related_name='book1')
#     book2 = models.ForeignKey(Book, related_name='book2')


# todo suuport multiple authors
# lower vs mixed case?
class Work(models.Model):
    # Store title and author as all lowercase.
    # todo multiple authors; for now use only one.
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)

    def __str__(self):
        return "{}, by {}".format(self.title, self.author)

    class Meta:
        ordering = ('author', 'title')
        unique_together = ('author', 'title')


class ISBN(models.Model):
    isbn_10 = models.TextField(unique=True)
    isbn_13 = models.TextField(unique=True)
    publication_date = models.DateField(null=True)
    work = models.ForeignKey(Work, related_name='isbns')


class Relationship(models.Model):
    """Defines a relationship between two books.  For example, if someone lists
    liking three books, a relatinship would be created for book1-2, 1-3, and 2-3.
    If any of these exist, their count would increase."""
    book1 = models.ForeignKey(Work, related_name='book1')
    book2 = models.ForeignKey(Work, related_name='book2')
    weight = models.IntegerField(default=0)

    def __str__(self):
        return "Relationship. Book1: {}, Book2: {}".format(self.book1, self.book2)

    class Meta:
        # todo this may allow duplicates of opposite order.  Investigate.
        unique_together = ('book1', 'book2')


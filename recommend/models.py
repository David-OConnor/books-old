from django.db import models


class Book(models.Model):
    isbn = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    publication_date = models.DateField()

from datetime import date
from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    summary = models.TextField()
    genre = models.CharField(max_length=100)

    def __str__(self):
        return self.title
   

class BookInstance(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    due_date = models.DateField(null=True, blank=True)
    is_available = models.BooleanField(default=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.book} - {self.due_date}"
    
    @property
    def is_due_date_expired(self):
        if self.due_date:
            return self.due_date < date.today()
        return False




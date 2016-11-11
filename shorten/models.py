from django.db import models

from shortly import settings

class User(models.Model):
    username = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=64)
    date_joined = models.DateTimeField()

    def __str__(self):
        return "{} {} {}".format(self.first, self.last_name, self.username)

class Url(models.Model):
    original_url = models.CharField(max_length=2000)
    shortened_url = models.CharField(max_length=settings.SHORT_URL_MAX_LEN)
    user = models.ForeignKey(User)

    def __str__(self):
        return "{} => {}".format(self.original_url, self.shortened_url)
